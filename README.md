# muhammadbibi-site

Personal portfolio and CV of Muhammad Bibi: https://muhammadbibi.vercel.app

A static site built with **Python + Jinja2**. The only JavaScript is `static/site.js` (theme button and project filter); the site works without it.
All the text lives in `data/*.yaml`, the layout in `templates/`, and `build.py` puts them together.

## Run it on your computer

```bash
pip install -r requirements.txt     # Jinja2 and PyYAML
python3 build.py --serve            # builds into public/ and opens a preview at http://localhost:8000
```

## Where things are

| What | File |
|---|---|
| Contact details, menu | `data/site.yaml` |
| Jobs (Experience page and CV) | `data/experience.yaml` |
| Projects (list, project pages, Home, CV) | `data/projects.yaml` |
| Skills, languages, education (Skills page and CV) | `data/skills.yaml` |
| Page layouts | `templates/*.html` (all extend `templates/base.html`) |
| Styling and animations | `static/style.css` |
| Photos, screenshots, fonts | `static/img/`, `static/fonts/` |
| The build script (with comments) | `build.py` |

## Common edits

- **Change text:** edit the YAML file, run `python3 build.py`, check, commit, push.
- **Add a project:** copy one block in `data/projects.yaml`, give it a new `slug` and `id`,
  set `status` to `done`, `progress` or `learning`. It gets its own page at `/projects/<slug>/` automatically.
  Put screenshots in `static/img/projects/`.
- **Tip:** in YAML, put text in "quotes" when it contains a comma or a colon.

## CV PDF

The **Download PDF** button links to `static/cv/Muhammad-Bibi-CV.pdf`. After changing CV content, make a new PDF:

```bash
pip install -r requirements-pdf.txt   # WeasyPrint (one time)
python3 build.py --pdf
```

then commit the new PDF. (Vercel cannot run WeasyPrint, so the PDF is made on your computer.)

## Deploy

Vercel installs `requirements.txt` by itself, then runs `python3 build.py` and publishes `public/`
(see `vercel.json`). Push to `main` and the site updates.

## Contact form

The form posts to FormSubmit (formsubmit.co), which emails messages to the address in `data/site.yaml`.
