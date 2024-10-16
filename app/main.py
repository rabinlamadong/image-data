import uvicorn
from fastapi import FastAPI

from app.api.v1.image_api import router

from app.db.session import create_session_manager
from app.settings import Settings, settings


def create_app(_settings: Settings) -> FastAPI:
    _app = FastAPI()

    session_manager = create_session_manager(_settings)
    _app.state.session_manager = session_manager

    _app.include_router(prefix="/api/v1", router=router)

    return _app


app = create_app(settings)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9002, log_level="info")
