import sys
from pathlib import Path

if str(Path(__file__).parent.parent) not in sys.path:
    sys.path.append(str(Path(__file__).parent.parent))


from router import log, video

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [ '*' ]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],)


@app.get('/')
async def get_root():
    return "우리는 귀여운 곰돌이 팀!"

app.include_router(log.router)
app.include_router(video.router)

