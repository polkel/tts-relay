import os
from dotenv import load_dotenv
from util.speaker import Speaker
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
from auth import validate_user

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()

speaker_mac = os.getenv("SPEAKER_MAC")
secret_password = os.getenv("API_KEY")

if speaker_mac is None:
    raise ValueError("Must define SPEAKER_MAC in .env")

if secret_password is None:
    raise ValueError("Must define API_KEY in .env")

speaker = Speaker(speaker_mac)


class SpeechReq(BaseModel):
    speech: str


class LoginReq(BaseModel):
    password: str


@app.get("/")
async def hello_world() -> dict[str, str]:
    return {"message": "Hello World"}


@app.post("/login")
async def login(req: LoginReq) -> str:
    if req.password == secret_password:
        return req.password
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password."
    )


@app.post("/speech", status_code=status.HTTP_204_NO_CONTENT)
async def queue_speech(req: SpeechReq, auth: None = Depends(validate_user)):
    asyncio.create_task(speaker.queue_speech(req.speech))
    return None
