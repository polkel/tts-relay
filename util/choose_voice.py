import os
import random
import math

VOICE_EXTENSION = ".onnx"


def get_voices() -> list[str]:
    curr_dir = os.path.dirname(__file__)
    path_to_voices = os.path.join(curr_dir, "../voices")

    if not os.path.isdir(path_to_voices):
        raise FileNotFoundError("Voices directory needs to exist.")

    items = os.listdir(path_to_voices)

    res: list[str] = []

    for item in items:
        root, ext = os.path.splitext(item)
        if ext == VOICE_EXTENSION:
            full_path = os.path.join(path_to_voices, item)
            res.append(full_path)

    return res


def get_random_voice() -> str:
    voices = get_voices()
    if len(voices) == 0:
        raise FileNotFoundError("There are no voices in the voice directory.")

    return voices[math.floor(random.random() * len(voices))]
