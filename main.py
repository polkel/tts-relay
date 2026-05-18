from util.generate_voice import create_speech
import sys


def main():
    speech = sys.argv[1].strip()

    if speech == "":
        raise ValueError("Must pass in a speech argument.")

    create_speech(speech)


main()
