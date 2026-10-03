# Fitbuddy-AI Fitness plan Generator

**Team ID:** 17  
**Department:** Computer Technology  
**Institution:** Madras Institute Of Technology  
**University:** Anna University  
**Academic Year:** 3  
**Semester:** 5  
**Section:** Batch A  
**Faculty Mentor / Guide:** Jayachitra V P  
**Team Leader:** Bharath Jeyakkumar S

## Team

| Member | Register No. | Role |
|---|---|---|
| Abdul Wahith M | 2024503559 | Team Leader / Backend & AI Integration |
| Kamalesh T | 2024503539 | UI / Frontend Development |
| Bilu Besto H | 2024503569 | Validation, Feedback & Reliability |
| Bharath Jeyakkumar S | 2024503013 | Testing & Quality Assurance |
| Prasannavelan K | 2024503053 | Database, Documentation & Demo Support |

The repository follows the same eight-phase academic documentation layout as the reference project. Editable Markdown sources are in `docs-src/`; final deliverables are PDFs in the eight numbered folders.

## Run

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000`. For offline/demo mode, set `FITBUDDY_MOCK_AI=true`.

# FitBuddy – AI Fitness Plan Generator

> An AI-powered fitness planning web application that generates personalized workout plans based on user fitness information and continuously improves plans using user feedback.

---

## 📌 Project Information

| Field | Details |
|---|---|
| **Project Name** | Fitbuddy-AI Fitness plan Generator |
| **Team ID** | 17 |
| **Department** | Computer Technology |
| **Institution** | Madras Institute Of Technology |
| **University** | Anna University |
| **Academic Year** | 3 |
| **Semester** | 5 |
| **Class / Section** | Batch A |
| **Faculty Mentor / Guide** | Jayachitra V P |
| **Team Leader** | Bharath Jeyakkumar S |
| **Demo Date** | 03 October 2026 |
| **Demo Location** | College / Hostel |
| **Demo Platform** | Visual Studio Code with Uvicorn |
| **Deployment** | Local development |
| **Application URL** | http://localhost:8000 |

---

# 📖 Table of Contents

- [About the Project](#-about-the-project)
- [Problem Statement](#-problem-statement)
- [Proposed Solution](#-proposed-solution)
- [Objectives](#-objectives)
- [Key Features](#-key-features)
- [How FitBuddy Works](#-how-fitbuddy-works)
- [System Architecture](#-system-architecture)
- [Data Flow](#-data-flow)
- [Technology Stack](#-technology-stack)
- [AI Integration](#-ai-integration)
- [Database](#-database)
- [Application Workflow](#-application-workflow)
- [API Endpoints](#-api-endpoints)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Environment Configuration](#-environment-configuration)
- [Running the Application](#-running-the-application)
- [Testing](#-testing)
- [Screenshots](#-screenshots)
- [Documentation](#-documentation)
- [Team Members](#-team-members)
- [Sprint Plan](#-sprint-plan)
- [Future Enhancements](#-future-enhancements)
- [Limitations](#-limitations)
- [Security and Privacy](#-security-and-privacy)
- [Demo](#-demo)
- [License](#-license)

---

# 🎯 About the Project

**FitBuddy** is an AI-powered fitness plan generation system designed to help users create personalized workout plans based on their individual fitness information.

The application collects user information such as:

- Fitness goal
- Age
- Weight
- Workout intensity
- Other fitness-related information

The collected information is processed by the backend and supplied to the **Google Gemini AI model**, which generates a structured workout plan.

The system also supports a feedback-driven workflow. Users can provide feedback on a generated plan, after which FitBuddy uses the feedback and previous plan information to generate an improved version.

In addition to workout planning, the application provides nutrition and recovery recommendations.

---

# ❗ Problem Statement

Creating an appropriate workout plan manually can be difficult because users have different:

- Fitness goals
- Body characteristics
- Experience levels
- Workout preferences
- Training intensities
- Feedback and changing requirements

A static workout plan may therefore not remain suitable as the user's requirements change.

FitBuddy addresses this problem by providing an AI-assisted system capable of generating and revising personalized workout plans.

---

# 💡 Proposed Solution

FitBuddy provides a web-based AI fitness planning system consisting of:

1. A user interface for entering fitness information.
2. A FastAPI backend for request processing.
3. Google Gemini integration for AI-generated plans.
4. SQLite storage for users, plans and feedback-related information.
5. A feedback mechanism for revising generated plans.
6. Nutrition and recovery recommendations.
7. User management and viewing functionality.
8. Automated tests for application reliability.

---

# 🎯 Objectives

The main objectives of FitBuddy are:

- Generate personalized fitness plans using AI.
- Reduce the effort required to manually create workout schedules.
- Allow users to provide feedback on generated plans.
- Improve plans based on user feedback.
- Provide nutrition and recovery tips.
- Store user and workout information.
- Provide a simple and accessible web interface.
- Maintain a modular and testable backend architecture.

---

# ⭐ Key Features

## 1. AI Workout Plan Generation

Users enter their fitness information and request a workout plan.

FitBuddy sends the relevant information to the Gemini AI model and generates a personalized plan.

The generated plan can include:

- Workout schedule
- Exercises
- Sets
- Repetitions
- Training guidance
- Recovery recommendations
- Nutrition-related suggestions

---

## 2. Personalized Fitness Planning

The generated plan is based on the information provided by the user rather than being a fixed predefined workout.

The system can consider factors such as:

- Fitness goal
- Age
- Weight
- Workout intensity
- User requirements

---

## 3. Feedback-Based Plan Revision

Users can provide feedback on their generated workout plan.

The feedback workflow allows FitBuddy to use:

- Previous workout plan
- User feedback
- User information

to generate a revised plan.

This creates an iterative workflow:

```text
User Information
       ↓
Initial AI Workout Plan
       ↓
User Reviews Plan
       ↓
User Feedback
       ↓
AI Processes Feedback
       ↓
Updated Workout Plan
