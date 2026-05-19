from util.generate_voice import create_speech
import os
from dotenv import load_dotenv
from util.speaker import Speaker
from fastapi import FastAPI, status
from pydantic import BaseModel

app = FastAPI()

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
def queue_speech(req: SpeechReq):
    speaker.queue_speech(req.speech)
    return None
