# whisper_transcribe.py
import os
import sys
import whisper

def transcribe(audio_file):
    model = whisper.load_model("base", device="cpu")
    result = model.transcribe(audio_file)
    print(result["text"])
    export_vtt(result, audio_file)

def export_vtt(result, audio_file):
    segments = result.get("segments", [])
    if not segments:
        print("No transcription segments found.")
        return

    vtt_lines = ["WEBVTT\n"]
    for segment in segments:
        start = format_timestamp(segment["start"])
        end = format_timestamp(segment["end"])
        text = segment["text"]
        vtt_lines.append(f"{start} --> {end}\n{text}\n")

    base_name = os.path.basename(audio_file)
    file_name_without_extension = os.path.splitext(base_name)[0]
    vtt_file = f"D:/STT/export_file/{file_name_without_extension}_whisper.vtt"

    with open(vtt_file, "w", encoding="utf-8") as f:
        f.writelines(vtt_lines)

    print(f"Exported VTT to {vtt_file}")


def format_timestamp(seconds):
    millis = int((seconds % 1) * 1000)
    seconds = int(seconds)
    mins, secs = divmod(seconds, 60)
    hrs, mins = divmod(mins, 60)
    return f"{hrs:02}:{mins:02}:{secs:02}.{millis:03}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python whisper_transcribe.py <audio_file>")
        sys.exit(1)

    audio_file = sys.argv[1]
    print("Processing audio file:", audio_file)
    transcribe(audio_file)
