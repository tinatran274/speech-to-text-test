package main

import (
	"fmt"
	"log"
	"whisper-integration/internal/speech_to_text"
)

func main() {
	audioFile := "D:/STT/OSR_us_000_0010_8k.wav"

	// whisper_transcription, err := speech_to_text.WhisperTranscribe(audioFile)
	// if err != nil {
	// 	log.Printf("Error running Whisper: %v\n", err)
	// 	return
	// }
	// fmt.Println("Transcription by Whisper: ", whisper_transcription)

	// wav2vec_transcription, err := speech_to_text.Wav2VecTranscribe(audioFile)
	// if err != nil {
	// 	log.Printf("Error running Wav2Vec: %v\n", err)
	// 	return
	// }
	// fmt.Println("Transcription by Wav2Vec 2.0: ", wav2vec_transcription)

	vosk_transcription, err := speech_to_text.VoskTranscribe(audioFile)
	if err != nil {
		log.Printf("Error running Vosk: %v\n", err)
		return
	}
	fmt.Println("Transcription by Vosk: ", vosk_transcription)
}
