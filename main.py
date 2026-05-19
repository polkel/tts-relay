from util.generate_voice import create_speech
import sys
import os
import subprocess
import time
from dotenv import load_dotenv


def main():
    load_dotenv()

    speech = sys.argv[1].strip()

    speaker_mac = os.getenv("SPEAKER_MAC")

    if speaker_mac is None:
        raise ValueError("Must have SPEAKER_MAC defined in .env")

    if speech == "":
        raise ValueError("Must pass in a speech argument.")

    voice_file = create_speech(speech)

    commands: list[tuple[list[str], bool]] = [
        (["pulseaudio", "-k"], False),
        (["pulseaudio", "--start"], False),
        (["bluetoothctl", "power", "on"], False),
        (["bluetoothctl", "connect", speaker_mac], True),
        (["pactl", "set-sink-volume", "@DEFAULT_SINK@", "100%"], False),
        (["paplay", voice_file], False),
        (["pulseaudio", "-k"], False),
        (["bluetoothctl", "power", "off"], False),
    ]

    for command, timer_pause in commands:
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Ran into an error with {' '.join(command)}")
            print(result.stdout)
            print(result.stderr)

        if timer_pause:
            time.sleep(3)

    os.remove(voice_file)


main()
