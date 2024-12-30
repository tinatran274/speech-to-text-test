package speech_to_text

import (
	"bytes"
	"fmt"
	"os"
	"os/exec"
)

func WhisperTranscribe(audioFilePath string) (string, error) {
	if _, err := os.Stat(audioFilePath); os.IsNotExist(err) {
		return "", fmt.Errorf("audio file does not exist: %v", err)
	}
	cmd := exec.Command("python", "D:/STT/internal/speech_to_text/whisper_model.py", audioFilePath)

	var out, stderr bytes.Buffer
	cmd.Stdout = &out
	cmd.Stderr = &stderr
	err := cmd.Run()
	if err != nil {
		return "", fmt.Errorf("failed to run Python script: %v, stderr: %v", err, stderr.String())
	}
	return out.String(), nil
}
