# Notes app — Session 14 starting point (Python + FastAPI)

This is the end state of **Lab 4**: the Lab 3 app, two tests, a linter and the finished
CI/CD workflow. Use it only if your team did not finish Lab 3 or Lab 4.

It is the starting point for Session 14, **not** a solution to it: there is no
`db/schema.sql`, no `db/seed.sql`, and the database code is still the simple
one-connection-per-request version that Task D replaces.

## What is in the folder

| File | Purpose |
|------|---------|
| `app/main.py` | The app: `/`, `/health` (platform health check), `/health/db` (counts the notes) |
| `Dockerfile` | Reads `PORT` (`${PORT:-8000}`), binds `0.0.0.0`, `exec` for clean shutdown |
| `requirements.txt` / `requirements-dev.txt` | Runtime deps (in the image) / + pytest, httpx2, ruff (CI) |
| `pyproject.toml` | Configuration for `ruff` and `pytest` |
| `tests/` | `conftest.py` sets a dummy `DATABASE_URL`; two real tests |
| `.github/workflows/ci-cd.yml` | Lab 4 pipeline: `check` (lint + test) then `deploy` (Render hook) |
| `compose.yml`, `db/init.sql` | Local stack with its own PostgreSQL (Session 14, Task B3 changes this) |
| `.env.example` | Lists `DB_PASSWORD` (for `.env`) and `DATABASE_URL` (for `.env.cloud`) |

## 1. Put it in your team repository

Copy every file in this folder into the **root** of your team repository — including the
hidden files and folders `.github/`, `.dockerignore`, `.gitignore`, `.env.example`.
In Git Bash, from the folder where you unzipped the starter:

    cp -r python-fastapi/. /c/path/to/your-repo/     # the "/." copies hidden files too
    cd /c/path/to/your-repo
    git switch -c week7-starter
    git add .
    git commit -m "Session 14: start from the Week 7 starter"
    git push -u origin week7-starter
    # open a pull request on GitHub; the "check" job runs; merge it when green

## 2. Check it works on your machine

    python -m venv .venv
    source .venv/Scripts/activate      # Git Bash on Windows (macOS/Linux: .venv/bin/activate)
    pip install -r requirements-dev.txt
    ruff check .                       # expect: All checks passed!
    pytest -q                          # expect: 2 passed

    cp .env.example .env               # then put any password after DB_PASSWORD=
    podman compose up -d --build
    curl -s http://localhost:3000/health/db     # {"db":"ok","notes":1}
    podman compose down

## 3. Render and GitHub settings (if you have no live service yet)

Follow **Appendix B** of the Session 14 handout: create the Render web service (Docker,
region Singapore, health check path `/health`, placeholder `DATABASE_URL`), then make
`check` required, add the `RENDER_DEPLOY_HOOK` secret and turn Render Auto-Deploy off.

## 4. Then follow the Session 14 handout from Task A

| Handout says | In this starter |
|--------------|-----------------|
| Task B — schema files | create `db/schema.sql` and `db/seed.sql` (the handout gives both) |
| Task B3 — local stack | edit the `volumes:` of `db` in `compose.yml`, delete `db/init.sql` |
| Task C — local test against Supabase | create `.env.cloud` (already ignored by git) |
| Task D — resilience | replace `app/main.py` as shown; `psycopg[binary,pool]` in `requirements.txt` |
| Task D — visible change | `APP_VERSION` becomes `1.3.0` |

Never commit `.env` or `.env.cloud`. Both are already listed in `.gitignore` and `.dockerignore`.
