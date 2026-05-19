from collections import deque
import time
import subprocess
from util.generate_voice import create_speech
import os


class Speaker:
    """An interface for the TTS to the bluetooth speaker."""

    def __init__(self, speaker_mac: str) -> None:
        self.speech_queue: deque[str] = deque()
        self.is_running: bool = False
        self.speaker_mac: str = speaker_mac

    def queue_speech(self, speech: str):
        self.speech_queue.appendleft(speech)

        # Check if speech box is already running,
        # If not we need to start it
        if not self.is_running:
            self.is_running = True
            try:
                self.talk()
            except:
                # Improve error logging here
                print("Something went wrong with the speech")
            finally:
                self.is_running = False

    def talk(self):
        initial_commands: list[tuple[list[str], bool]] = [
            (["pulseaudio", "--start"], False),
            (["bluetoothctl", "power", "on"], False),
            (["bluetoothctl", "connect", self.speaker_mac], True),
            (["pactl", "set-sink-volume", "@DEFAULT_SINK@", "100%"], True),
        ]

        for command, timer_pause in initial_commands:
            self._run_subprocess(command, timer_pause, True)

        voice_file = ""

        while len(self.speech_queue) != 0:
            speech = self.speech_queue.pop()
            voice_file = create_speech(speech)
            self._run_subprocess(["paplay", voice_file], True)

        os.remove(voice_file)
        self._run_subprocess(["bluetoothctl", "power", "off"])

    def _run_subprocess(
        self, commands: list[str], pause: bool = False, throw: bool = False
    ):
        result = subprocess.run(commands, capture_output=True, text=True)

        if result.returncode != 0:
            # Improve logging here
            print(f"Ran into an error with {' '.join(commands)}")
            print(result.stdout)
            print(result.stderr)
            if throw:
                raise RuntimeError("Something went wrong with the speaker.")

        if pause:
            time.sleep(1)
