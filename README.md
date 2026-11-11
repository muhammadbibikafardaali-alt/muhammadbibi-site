# muhammadbibi-site

Personal portfolio and CV of Muhammad Bibi, live at https://muhammadbibi.vercel.app

Plain HTML and CSS. No framework, no build step, no JavaScript.

## Where things are

| Page | File |
|---|---|
| Home | `index.html` |
| Experience | `experience/index.html` |
| Projects | `projects/index.html` |
| DDoS case study | `projects/ddos-aws/index.html` |
| Contact (+ form) | `contact/index.html`, `contact/thanks/index.html` |
| CV (prints to one A4 page) | `cv/index.html` |
| All styling and animations | `assets/style.css` |
| Photos and icon | `assets/` |

## How to edit

1. Open the page file and change the text between the tags.
2. Commit and push to `main`. Vercel deploys it automatically.

To add a project, copy one `<li class="entry ...">` block in `projects/index.html`
and change the ID, date, status and text. Status classes: `is-delivered` + `status delivered`,
or `is-progress` + `status progress`.

Colours and fonts are CSS variables at the top of `assets/style.css`.

## Contact form

The form posts to FormSubmit (formsubmit.co), which emails messages to the address in
`contact/index.html`. The first message triggers a one-time confirmation email.
