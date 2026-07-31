from fastapi import APIRouter

from web.routes import analysis, explain, home, jobs, leagues, models, predict, research

api_router = APIRouter()
api_router.include_router(home.router)
api_router.include_router(leagues.router)
api_router.include_router(models.router)
api_router.include_router(predict.router)
api_router.include_router(jobs.router)
api_router.include_router(research.router)
api_router.include_router(analysis.router)
api_router.include_router(explain.router)
