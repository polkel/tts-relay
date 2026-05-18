from piper import PiperVoice, SynthesisConfig
from util.choose_voice import get_random_voice
import os
import wave


# Returns the path to the created speech file
def create_speech(speech: str, voice_file: str | None = None) -> str:
    voice = ""

    if voice_file is None:
        voice = get_random_voice()
    else:
        voice = voice_file
    sythesizer = PiperVoice.load(voice)

    curr_dir = os.path.dirname(__file__)
    temporary_voice_file = os.path.join(curr_dir, "../tmp.wav")

    config = SynthesisConfig(volume=1.5, length_scale=1.5, normalize_audio=False)
    with wave.open(temporary_voice_file, "wb") as wav_file:
        sythesizer.synthesize_wav(speech, wav_file, syn_config=config)

    return temporary_voice_file
