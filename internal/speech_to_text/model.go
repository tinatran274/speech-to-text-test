package speech_to_text

type SpeechToText interface {
	TranscribeByWhisper(audioFilePath string) (string, error)
}
