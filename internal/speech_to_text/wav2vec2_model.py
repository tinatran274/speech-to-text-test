import os
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
import torch
import soundfile as sf
import sys
import torchaudio

processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-base-960h")
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")

SAMPLING_RATE = 16000

def transcribe_audio(audio_path):
    waveform, sample_rate = torchaudio.load(audio_path)
    if sample_rate != SAMPLING_RATE:
        resampler = torchaudio.transforms.Resample(orig_freq=sample_rate, new_freq=SAMPLING_RATE)
        waveform = resampler(waveform)
    input_values = processor(waveform.squeeze().numpy(), return_tensors="pt", sampling_rate=SAMPLING_RATE).input_values
    
    with torch.no_grad():
        logits = model(input_values).logits
    predicted_ids = torch.argmax(logits, dim=-1)
    transcription = processor.decode(predicted_ids[0])
    
    return transcription

def export_vtt(transcription, audio_file):
    segment_length = 5
    vtt_lines = ["WEBVTT\n"]
    
    start_time = 0
    end_time = segment_length

    words = transcription.split()
    text_chunk = []
    for i, word in enumerate(words):
        text_chunk.append(word)
        if (i + 1) % (segment_length * 2) == 0 or i == len(words) - 1:
            start_timestamp = format_timestamp(start_time)
            end_timestamp = format_timestamp(end_time)
            text = " ".join(text_chunk).lower()
            text = text.capitalize() 

            vtt_lines.append(f"{start_timestamp} --> {end_timestamp}\n{text}\n")
            start_time = end_time
            end_time += segment_length
            text_chunk = []
    
    base_name = os.path.basename(audio_file)
    file_name_without_extension = os.path.splitext(base_name)[0]
    vtt_file = f"D:/STT/export_file/{file_name_without_extension}_wav2vec.vtt"

    with open(vtt_file, "w", encoding="utf-8") as f:
        f.writelines(vtt_lines)
    print(f"Exported VTT to {vtt_file}")

def format_timestamp(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    milliseconds = int((seconds % 1) * 1000)
    return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}.{milliseconds:03}"

if __name__ == "__main__":
    audio_file = sys.argv[1]
    print("Processing audio file:", audio_file)
    transcription = transcribe_audio(audio_file)
    print(transcription)
    export_vtt(transcription, audio_file)
