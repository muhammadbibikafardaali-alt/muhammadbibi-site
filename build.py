"""
build.py: builds the website from the templates and the data files.

    python3 build.py          # build the site into public/
    python3 build.py --pdf    # also make the CV PDF (needs WeasyPrint, see README)
    python3 build.py --serve  # build, then preview at http://localhost:8000

How it works, in four steps:
  1. Read the content from data/*.yaml (projects, experience, skills, site settings).
  2. Copy static/ (CSS, fonts, images) into public/.
  3. Fill each Jinja2 template in templates/ with that content and write the HTML into public/.
  4. Optionally turn the CV page into a PDF.
"""

import shutil
import sys
from pathlib import Path

import yaml                                        # reads the .yaml data files
from jinja2 import Environment, FileSystemLoader, StrictUndefined

ROOT = Path(__file__).parent        # the folder this script is in
DATA = ROOT / "data"
STATIC = ROOT / "static"
TEMPLATES = ROOT / "templates"
OUT = ROOT / "public"               # the finished website ends up here

# The three status values a project can have. Anything else is a typo.
VALID_STATUS = {"done", "progress", "learning"}


def load(name):
    """Read one YAML file from data/ and return it as Python lists/dicts."""
    with open(DATA / f"{name}.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)


# Optional project fields and their value when a project leaves them out.
PROJECT_DEFAULTS = {"custom_page": False, "featured": False, "screenshots": [], "learned": [],
                    "built": [], "stages": [], "stage_now": 0, "next": "", "who": "", "role": "", "how": "", "cv": ""}
LINK_DEFAULTS = {"live": "", "github": "", "private": ""}
JOB_DEFAULTS = {"current": False, "team": "", "outcome_link": None, "tags": []}


def check_projects(projects):
    """Fill in optional fields, then stop with a clear message if a project entry is broken."""
    slugs = set()
    for p in projects:
        for key, value in PROJECT_DEFAULTS.items():
            p.setdefault(key, value)
        p["links"] = {**LINK_DEFAULTS, **(p.get("links") or {})}
        if p["status"] not in VALID_STATUS:
            sys.exit(f"Project '{p['slug']}': status must be one of {VALID_STATUS}, not '{p['status']}'")
        if p["slug"] in slugs:
            sys.exit(f"Project slug '{p['slug']}' is used twice")
        slugs.add(p["slug"])
        for shot in p.get("screenshots", []):
            image = STATIC / shot["src"].lstrip("/")
            if not image.exists():
                sys.exit(f"Project '{p['slug']}': screenshot not found: {image}")


def write_page(env, template, url, **context):
    """Render one template and save it as public/<url>/index.html.

    url "/"            -> public/index.html
    url "/projects/"   -> public/projects/index.html
    """
    html = env.get_template(template).render(**context)
    target = OUT / url.strip("/") / "index.html"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(html, encoding="utf-8")
    print(f"  {url:28} <- templates/{template}")


def build():
    # 1. Content
    site = load("site")
    projects = load("projects")
    experience = load("experience")
    skills = load("skills")
    check_projects(projects)
    for job in experience:                       # optional fields for each job
        for key, value in JOB_DEFAULTS.items():
            job.setdefault(key, value)

    # 2. Start from an empty public/ folder and copy the static files in
    if OUT.exists():
        shutil.rmtree(OUT)
    shutil.copytree(STATIC, OUT)

    # 3. Pages. StrictUndefined makes a typo in a template fail loudly instead of printing nothing.
    env = Environment(loader=FileSystemLoader(TEMPLATES), undefined=StrictUndefined,
                      trim_blocks=True, lstrip_blocks=True)
    shared = dict(site=site, projects=projects, experience=experience, skills=skills)

    print("Building pages:")
    write_page(env, "home.html", "/", page="home", **shared)
    write_page(env, "experience.html", "/experience/", page="experience", **shared)
    write_page(env, "projects.html", "/projects/", page="projects", **shared)
    write_page(env, "skills.html", "/skills/", page="skills", **shared)
    write_page(env, "contact.html", "/contact/", page="contact", **shared)
    write_page(env, "thanks.html", "/contact/thanks/", page="contact", **shared)
    write_page(env, "cv.html", "/cv/", page="cv", **shared)

    # One page per project. "next_p" is the project after it in the list, for the "Next" link.
    for i, p in enumerate(projects):
        next_p = projects[i + 1] if i + 1 < len(projects) else projects[0]
        template = f"case_{p['slug'].split('-')[0]}.html" if p.get("custom_page") else "project.html"
        write_page(env, template, f"/projects/{p['slug']}/", page="projects", p=p, next_p=next_p, **shared)

    # Keep the PDF that was made earlier (it lives in static/cv/ so it was copied above).
    print(f"Done: {sum(1 for _ in OUT.rglob('*.html'))} pages in {OUT.name}/")


def make_pdf():
    """Turn the built CV page into an A4 PDF with WeasyPrint (it uses the print styles in style.css)."""
    try:
        from weasyprint import HTML
    except ImportError:
        sys.exit("WeasyPrint is not installed. Run: pip install -r requirements-pdf.txt")

    # The site uses links like "/style.css". On a web server "/" is the site root, but for WeasyPrint
    # on disk "/" is the root of the computer, so we point those links at the public/ folder instead.
    root = OUT.resolve().as_uri() + "/"                 # e.g. file:///home/me/site/public/
    html = (OUT / "cv" / "index.html").read_text(encoding="utf-8")
    html = html.replace('href="/', f'href="{root}').replace('src="/', f'src="{root}')
    css = (OUT / "style.css").read_text(encoding="utf-8").replace('url("/', f'url("{root}')
    (OUT / "_print.css").write_text(css, encoding="utf-8")
    html = html.replace(f'href="{root}style.css"', f'href="{root}_print.css"')

    pdf_path = STATIC / "cv" / "Muhammad-Bibi-CV.pdf"   # saved in static/ so it is kept in Git and published
    pdf_path.parent.mkdir(exist_ok=True)
    HTML(string=html, base_url=str(OUT)).write_pdf(str(pdf_path))
    (OUT / "_print.css").unlink()                       # temporary file, not part of the site
    shutil.copy(pdf_path, OUT / "cv" / pdf_path.name)
    print(f"PDF: {pdf_path.relative_to(ROOT)}")


def serve():
    """Preview the built site locally."""
    import functools
    import http.server
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(OUT))
    print("Preview: http://localhost:8000  (Ctrl+C to stop)")
    http.server.ThreadingHTTPServer(("localhost", 8000), handler).serve_forever()


if __name__ == "__main__":
    build()
    if "--pdf" in sys.argv:
        make_pdf()
    if "--serve" in sys.argv:
        serve()
