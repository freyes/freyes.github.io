# freyes.github.io

Source for [tty.cl](http://tty.cl) — Felipe Reyes' personal blog. Built with [Pelican](http://getpelican.com/) and a custom theme, automatically deployed to GitHub Pages via GitHub Actions.

## Setup

```bash
# Clone the repo
git clone https://github.com/freyes/freyes.github.io
cd freyes.github.io

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Local Development

Run the development server with auto-reload:

```bash
pelican -r -s pelicanconf.py
```

Or using tox:

```bash
tox -e serve
```

The site will be available at `http://localhost:8000`.

To generate the static output without serving:

```bash
pelican -s pelicanconf.py       # development (relative URLs)
pelican -s publishconf.py       # production (absolute URLs)
```

## Project Structure

```
├── content/              # Source content (Markdown/reST)
│   ├── articles/         # Blog posts
│   ├── pages/            # Static pages (about, contact)
│   └── images/           # Site images
├── tty-theme/            # Custom Pelican theme
│   ├── templates/        # Jinja2 templates
│   └── static/           # CSS, images
├── pelicanconf.py        # Development config
├── publishconf.py        # Production config (extends pelicanconf)
├── requirements.txt      # Python dependencies
├── tox.ini               # Tox configuration
└── .github/workflows/    # CI/CD
    └── publish.yaml      # Auto-deploy on push to `src`
```

## Publishing

Pushing to the `src` branch triggers the GitHub Actions workflow, which:

1. Checks out the repository
2. Sets up Python 3.10
3. Installs dependencies via tox
4. Generates the static site with `tox -e publish`
5. Deploys the `output/` directory to the `master` branch (GitHub Pages)

Manual publish:

```bash
pelican -s publishconf.py
ghp-import output -b master
git push origin master
```

## Theme

The `tty-theme` is a custom Pelican theme included as a subdirectory. It uses Bootstrap and provides templates for articles, pages, categories, tags, and archives.

## License

Content and theme copyright Felipe Reyes.