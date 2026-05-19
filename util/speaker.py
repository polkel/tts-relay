from collections import deque
from util.generate_voice import create_speech
import os
import asyncio
from piper import PiperVoice
from util.choose_voice import get_voices
import math
import random


class Speaker:
    """An interface for the TTS to the bluetooth speaker."""

    def __init__(self, speaker_mac: str) -> None:
        self.speech_queue: deque[str] = deque()
        self.is_running: bool = False
        self.speaker_mac: str = speaker_mac
        self.voice_models: list[PiperVoice] = []
        voices = get_voices()
        for voice in voices:
            self.voice_models.append(PiperVoice.load(voice))

    async def queue_speech(self, speech: str):
        self.speech_queue.appendleft(speech)

        # Check if speech is already running,
        # If not we need to start it
        if not self.is_running:
            self.is_running = True
            try:
                await self.talk()
            except Exception as e:
                print(f"Something went wrong with speech: {e}")
            finally:
                self.is_running = False

    async def talk(self):
        initial_commands: list[tuple[list[str], bool]] = [
            (["pulseaudio", "--start"], False),
            (["bluetoothctl", "power", "on"], False),
            (["bluetoothctl", "connect", self.speaker_mac], True),
            (["pactl", "set-sink-volume", "@DEFAULT_SINK@", "100%"], True),
        ]

        for command, timer_pause in initial_commands:
            await self._run_subprocess(command, timer_pause, True)

        voice_file = ""

        while len(self.speech_queue) != 0:
            speech = self.speech_queue.pop()

            # Randomly select a voice to use
            if len(self.voice_models) == 0:
                raise ValueError(
                    "There must be at least one voice model in the directory."
                )
            voice_index = math.floor(random.random() * len(self.voice_models))
            voice_file = await asyncio.to_thread(
                create_speech, speech, self.voice_models[voice_index]
            )
            await self._run_subprocess(["paplay", voice_file], True)

        await asyncio.to_thread(os.remove, voice_file)
        await self._run_subprocess(["bluetoothctl", "power", "off"])

    async def _run_subprocess(
        self, commands: list[str], pause: bool = False, throw: bool = False
    ):
        process = await asyncio.create_subprocess_exec(
            *commands, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await process.communicate()

        if process.returncode != 0:
            # Improve logging here
            print(f"Ran into an error with {' '.join(commands)}")
            print(stdout.decode())
            print(stderr.decode())
            if throw:
                raise RuntimeError("Something went wrong with the speaker.")

        if pause:
            await asyncio.sleep(1.5)
