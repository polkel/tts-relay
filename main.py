from util.generate_voice import create_speech
import sys
import os
import subprocess
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

    result = subprocess.run(["pulseaudio", "-k"], capture_output=True, text=True)
    print(result.returncode)
    result = subprocess.run(["pulseaudio", "--start"], capture_output=True, text=True)
    print(result.returncode)
    result = subprocess.run(
        ["bluetoothctl", "power", "on"], capture_output=True, text=True
    )
    print(result.returncode)
    result = subprocess.run(
        ["bluetoothctl", "connect", speaker_mac], capture_output=True, text=True
    )
    print(result.returncode)
    result = subprocess.run(
        ["pulseaudio", "set-sink-volume", "@DEFAULT_SINK@", "100%"],
        capture_output=True,
        text=True,
    )
    print(result.returncode)
    result = subprocess.run(["paplay", voice_file], capture_output=True, text=True)
    print(result.returncode)


main()
