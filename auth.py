from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
import os
from dotenv import load_dotenv

load_dotenv()

api_key_header = APIKeyHeader(name="x-voice-key")

secret_key = os.getenv("API_KEY")

if secret_key is None:
    raise ValueError("Must have API_KEY set in .env")


def validate_user(api_key: str = Security(api_key_header)):
    if api_key == secret_key:
        return
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password."
    )
