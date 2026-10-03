"""SQLite persistence via SQLAlchemy ORM."""
from datetime import datetime, timezone
from typing import Dict, Iterator, List, Optional

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship, sessionmaker

from .config import settings
from .schemas import UserInput

_connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}
engine = create_engine(settings.database_url, connect_args=_connect_args)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def _now() -> datetime:
    return datetime.now(timezone.utc)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    user_id: Mapped[str] = mapped_column(String(50), primary_key=True)
    username: Mapped[str] = mapped_column(String(50))
    age: Mapped[int] = mapped_column(Integer)
    weight: Mapped[float] = mapped_column(Float)
    goal: Mapped[str] = mapped_column(String(60))
    intensity: Mapped[str] = mapped_column(String(10))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)

    plan: Mapped[Optional["Plan"]] = relationship(
        back_populates="user", uselist=False, cascade="all, delete-orphan"
    )


class Plan(Base):
    __tablename__ = "plans"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.user_id"), unique=True)
    original_plan: Mapped[str] = mapped_column(Text)
    updated_plan: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    feedback: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    nutrition_tip: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now, onupdate=_now)

    user: Mapped[User] = relationship(back_populates="plan")


def init_db() -> None:
    Base.metadata.create_all(bind=engine)


def get_db() -> Iterator[Session]:
    """FastAPI dependency: one session per request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------- user helpers ----------
def save_user(db: Session, data: UserInput) -> User:
    """Create the user, or update their details if the user_id already exists."""
    user = db.get(User, data.user_id)
    if user is None:
        user = User(user_id=data.user_id)
        db.add(user)
    user.username = data.username
    user.age = data.age
    user.weight = data.weight
    user.goal = data.goal
    user.intensity = data.intensity
    db.commit()
    return user


def get_user(db: Session, user_id: str) -> Optional[User]:
    return db.get(User, user_id)


def get_all_users(db: Session) -> List[User]:
    return list(db.scalars(select(User).order_by(User.created_at.desc())))


def delete_user(db: Session, user_id: str) -> bool:
    user = db.get(User, user_id)
    if user is None:
        return False
    db.delete(user)  # cascades to the plan
    db.commit()
    return True


# ---------- plan helpers ----------
def save_plan(db: Session, user_id: str, workout_plan: str, nutrition_tip: Optional[str]) -> Plan:
    """Store a freshly generated plan. Replaces any previous plan for this user."""
    plan = db.scalars(select(Plan).where(Plan.user_id == user_id)).first()
    if plan is None:
        plan = Plan(user_id=user_id, original_plan=workout_plan, nutrition_tip=nutrition_tip)
        db.add(plan)
    else:
        plan.original_plan = workout_plan
        plan.nutrition_tip = nutrition_tip
        plan.updated_plan = None
        plan.feedback = None
    db.commit()
    return plan


def get_plan(db: Session, user_id: str) -> Optional[Plan]:
    return db.scalars(select(Plan).where(Plan.user_id == user_id)).first()


def get_original_plan(db: Session, user_id: str) -> Optional[str]:
    plan = get_plan(db, user_id)
    return plan.original_plan if plan else None


def update_plan(
    db: Session, user_id: str, updated_plan: str, feedback: str, nutrition_tip: Optional[str] = None
) -> Optional[Plan]:
    """Save the feedback-revised plan next to the original (the original is never overwritten)."""
    plan = get_plan(db, user_id)
    if plan is None:
        return None
    plan.updated_plan = updated_plan
    plan.feedback = feedback
    if nutrition_tip:
        plan.nutrition_tip = nutrition_tip
    db.commit()
    return plan


def update_tip(db: Session, user_id: str, nutrition_tip: str) -> Optional[Plan]:
    plan = get_plan(db, user_id)
    if plan is None:
        return None
    plan.nutrition_tip = nutrition_tip
    db.commit()
    return plan


def get_all_plans(db: Session) -> Dict[str, Plan]:
    """Return {user_id: Plan} for every stored plan."""
    return {p.user_id: p for p in db.scalars(select(Plan))}
