from fastapi import APIRouter

from app.api.v1 import projects, sprints, team_members, tasks, costs, auth, statistics, activities

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
api_router.include_router(sprints.router, prefix="/sprints", tags=["sprints"])
api_router.include_router(team_members.router, prefix="/team-members", tags=["team-members"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
api_router.include_router(costs.router, prefix="/costs", tags=["costs"])
api_router.include_router(statistics.router, prefix="/statistics", tags=["statistics"])
api_router.include_router(activities.router, prefix="/activities", tags=["activities"]) 