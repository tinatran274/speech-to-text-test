import sys
import wave
import json
from vosk import Model, KaldiRecognizer

MODEL_PATH = "./vosk-model-small-en-us-0.15"

def transcribe(audio_path):
    try:
        # Load the Vosk model
        print(f"Loading model from {MODEL_PATH}...")
        model = Model(MODEL_PATH)

        # Open the WAV file
        print(f"Opening audio file: {audio_path}")
        wf = wave.open(audio_path, "rb")

        # Validate audio format
        if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() not in (8000, 16000):
            raise ValueError("Audio file must be WAV format mono PCM with a sample rate of 8000 or 16000 Hz")

        # Initialize recognizer
        rec = KaldiRecognizer(model, wf.getframerate())

        # Process audio frames
        print("Transcribing audio...")
        results = []
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                results.append(json.loads(rec.Result()))

        # Process final transcription
        final_result = json.loads(rec.FinalResult())
        results.append(final_result)

        # Combine all results into a single transcription
        transcription = " ".join([result.get("text", "") for result in results])
        return transcription
    except Exception as e:
        print(f"Error during transcription: {e}")
        return ""

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python transcribe.py <audio_file_path>")
        sys.exit(1)

    audio_file = sys.argv[1]
    print("Transcription Result:")
    print(transcribe(audio_file))
