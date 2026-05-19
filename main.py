import os
from dotenv import load_dotenv
from util.speaker import Speaker
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()

speaker_mac = os.getenv("SPEAKER_MAC")

if speaker_mac is None:
    raise ValueError("Must define SPEAKER_MAC in .env")

speaker = Speaker(speaker_mac)


class SpeechReq(BaseModel):
    speech: str


@app.get("/")
async def hello_world() -> dict[str, str]:
    return {"message": "Hello World"}


@app.post("/speech", status_code=status.HTTP_204_NO_CONTENT)
async def queue_speech(req: SpeechReq):
    asyncio.create_task(speaker.queue_speech(req.speech))
    return None
