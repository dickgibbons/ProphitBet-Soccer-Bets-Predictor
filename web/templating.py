from fastapi.templating import Jinja2Templates

from web.config import PROJECT_ROOT, ROOT_PATH

templates = Jinja2Templates(directory=str(PROJECT_ROOT / "web" / "templates"))
templates.env.globals["bp"] = ROOT_PATH
