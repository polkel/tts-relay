from piper import PiperVoice, SynthesisConfig
from util.choose_voice import get_random_voice
import os
import wave


# Returns the path to the created speech file
def create_speech(speech: str, piper_voice: PiperVoice | None = None) -> str:
    synthesizer = piper_voice
    if synthesizer is None:
        voice = get_random_voice()
        synthesizer = PiperVoice.load(voice)

    curr_dir = os.path.dirname(__file__)
    temporary_voice_file = os.path.join(curr_dir, "../tmp.wav")

    config = SynthesisConfig(volume=1.5, length_scale=1.5, normalize_audio=False)
    with wave.open(temporary_voice_file, "wb") as wav_file:
        synthesizer.synthesize_wav(speech, wav_file, syn_config=config)

    return temporary_voice_file
