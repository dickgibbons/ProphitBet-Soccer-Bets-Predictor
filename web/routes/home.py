import html
import re

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from web import db
from web.auth import require_auth
from web.config import PROJECT_ROOT
from web.services.leagues import list_created_leagues
from web.templating import templates

router = APIRouter()


def _md_to_html(text: str) -> str:
    """Minimal Markdown → HTML for the user guide (no extra dependency)."""
    lines = text.splitlines()
    out: list[str] = []
    in_table = False
    in_list = False

    def close_list():
        nonlocal in_list
        if in_list:
            out.append("</ul>")
            in_list = False

    def close_table():
        nonlocal in_table
        if in_table:
            out.append("</tbody></table>")
            in_table = False

    def inline(s: str) -> str:
        s = html.escape(s)
        s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2" target="_blank" rel="noopener">\1</a>', s)
        s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
        s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
        return s

    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if stripped.startswith("|") and "|" in stripped[1:]:
            close_list()
            cells = [c.strip() for c in stripped.strip("|").split("|")]
            is_sep = all(re.fullmatch(r":?-{3,}:?", c.replace(" ", "")) for c in cells)
            if not in_table:
                out.append("<table><thead><tr>" + "".join(f"<th>{inline(c)}</th>" for c in cells) + "</tr></thead><tbody>")
                in_table = True
            elif is_sep:
                pass
            else:
                out.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in cells) + "</tr>")
            i += 1
            continue
        else:
            close_table()

        if stripped.startswith("- "):
            if not in_list:
                out.append("<ul>")
                in_list = True
            out.append(f"<li>{inline(stripped[2:])}</li>")
            i += 1
            continue
        else:
            close_list()

        if stripped == "---":
            out.append("<hr>")
        elif stripped.startswith("# "):
            out.append(f"<h1>{inline(stripped[2:])}</h1>")
        elif stripped.startswith("## "):
            out.append(f"<h2>{inline(stripped[3:])}</h2>")
        elif stripped.startswith("### "):
            out.append(f"<h3>{inline(stripped[4:])}</h3>")
        elif stripped.startswith("#### "):
            out.append(f"<h4>{inline(stripped[5:])}</h4>")
        elif stripped == "":
            out.append("")
        else:
            out.append(f"<p>{inline(stripped)}</p>")
        i += 1

    close_list()
    close_table()
    return "\n".join(out)


@router.get("/", response_class=HTMLResponse)
def home(request: Request, user: str = Depends(require_auth)):
    leagues = list_created_leagues()
    jobs = db.list_jobs(limit=10)
    return templates.TemplateResponse(
        "home.html",
        {
            "request": request,
            "user": user,
            "leagues": leagues,
            "jobs": jobs,
        },
    )


@router.get("/guide", response_class=HTMLResponse)
def user_guide(request: Request, user: str = Depends(require_auth)):
    path = PROJECT_ROOT / "USER_GUIDE.md"
    raw = path.read_text(encoding="utf-8") if path.exists() else "# Guide missing\n\nUSER_GUIDE.md was not found."
    return templates.TemplateResponse(
        "guide.html",
        {
            "request": request,
            "user": user,
            "content": _md_to_html(raw),
        },
    )
