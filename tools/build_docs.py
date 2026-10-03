"""Render docs-src/**/*.md into the eight numbered PDF folders."""
import json, os, re, subprocess
from pathlib import Path
from weasyprint import HTML
ROOT=Path(__file__).resolve().parent.parent
SRC=ROOT/"docs-src"
CSS="""body{font-family:Georgia,'Times New Roman',serif;font-size:11pt;line-height:1.45;color:#111;max-width:100%}h1{font-size:20pt;text-align:center;margin:0 0 10pt}h2{font-size:14pt;margin:16pt 0 6pt;border-bottom:1px solid #999}h3{font-size:12pt;margin:12pt 0 4pt}table{border-collapse:collapse;width:100%;margin:6pt 0 10pt;font-size:9.5pt}tr{page-break-inside:avoid}th,td{border:1px solid #555;padding:4pt 6pt;vertical-align:top;text-align:left}th{background:#e8e8e8}pre{background:#f4f4f4;border:1px solid #bbb;padding:8pt;font-size:8.2pt;line-height:1.25;white-space:pre;overflow:hidden}code{font-family:Consolas,monospace;font-size:9pt}img{max-width:100%;border:1px solid #bbb;margin:4pt 0}.hdr td:first-child{width:28%;font-weight:bold;background:#f0f0f0}"""
def header(marks):
    return """<table class='hdr'>
<tr><td>Date</td><td>{{date}}</td></tr>
<tr><td>Team ID</td><td>{{team_id}}</td></tr>
<tr><td>Project Name</td><td>{{project_name}}</td></tr>
<tr><td>Department</td><td>{{department}}</td></tr>
<tr><td>Institution / University</td><td>{{institution}} / {{university}}</td></tr>
<tr><td>Academic Year / Semester / Section</td><td>{{academic_year}} / {{semester}} / {{section}}</td></tr>
<tr><td>Faculty Mentor / Guide</td><td>{{mentor}}</td></tr>
<tr><td>Team Leader</td><td>{{team_leader}}</td></tr>
<tr><td>Sprint 1 Start / End</td><td>{{s1_start}} / {{s1_end}}</td></tr>
<tr><td>Sprint 2 Start / End</td><td>{{s2_start}} / {{s2_end}}</td></tr>
<tr><td>Sprint 3 Start / End</td><td>{{s3_start}} / {{s3_end}}</td></tr>
<tr><td>Team Roles</td><td>Abdul Wahith M — Backend &amp; AI Integration; Kamalesh T — UI / Frontend Development; Bilu Besto H — Validation, Feedback &amp; Reliability; Bharath Jeyakkumar S — Team Leader / Testing &amp; Quality Assurance; Prasannavelan K — Database, Documentation &amp; Demo Support</td></tr>
<tr><td>Maximum Marks</td><td>__MARKS__</td></tr>
</table>""".replace("__MARKS__", str(marks))

def main():
    v=json.loads((SRC/'project.json').read_text())
    for md in sorted(SRC.rglob('*.md')):
            if md.name.startswith('_'): continue
            txt=md.read_text()
            txt=re.sub(r'\{\{HEADER:(.+?)\}\}',lambda m:header(m.group(1)),txt)
            for k,val in v.items(): txt=txt.replace('{{'+k+'}}',str(val))
            tmp=SRC/'_tmp.md'; tmp.write_text(txt)
            htmltmp=SRC/'_tmp.html'
            subprocess.run(['pandoc',str(tmp),'-f','markdown','-t','html5','-o',str(htmltmp),'--standalone'],check=True)
            raw=htmltmp.read_text()
            raw=raw.replace('</head>',f'<style>{CSS}</style></head>')
            htmltmp.write_text(raw)
            out=ROOT/md.relative_to(SRC).with_suffix('.pdf')
            out.parent.mkdir(parents=True,exist_ok=True)
            HTML(filename=str(htmltmp),base_url=str(SRC)).write_pdf(str(out))
    for p in [SRC/'_tmp.md',SRC/'_tmp.html']:
        p.unlink(missing_ok=True)
if __name__=='__main__': main()
