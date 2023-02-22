from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.routing import Route
from starlette.templating import Jinja2Templates


templates = Jinja2Templates(directory='view', autoescape=False, auto_reload=True)

async def index(request):
    return templates.TemplateResponse("index.html.j2", {'request': request})


routes = [
    Route("/", endpoint=index)
]