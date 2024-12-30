package speech_to_text

import (
	"context"
	"fmt"
	"log"

	speech "cloud.google.com/go/speech/apiv1"
	"cloud.google.com/go/speech/apiv1/speechpb"
	"google.golang.org/api/option"
)

func GGCloudTranscribe(audioFilePath string) (string, error) {
	ctx := context.Background()
	credentialsFile := "D:/STT/glass-memento-446101-p7-6ecebbd67d9b.json"

	client, err := speech.NewClient(ctx, option.WithCredentialsFile(credentialsFile))
	if err != nil {
		log.Fatalf("Failed to create client: %v", err)
		return "", fmt.Errorf("Failed to create client: %v", err)
	}
	defer client.Close()
	fileURI := "gs://cloud-samples-data/speech/brooklyn_bridge.raw"

	resp, err := client.Recognize(ctx, &speechpb.RecognizeRequest{
		Config: &speechpb.RecognitionConfig{
			Encoding:        speechpb.RecognitionConfig_LINEAR16,
			SampleRateHertz: 16000,
			LanguageCode:    "en-US",
		},
		Audio: &speechpb.RecognitionAudio{
			AudioSource: &speechpb.RecognitionAudio_Uri{Uri: fileURI},
		},
	})
	if err != nil {
		log.Fatalf("Failed to recognize: %v", err)
		return "", fmt.Errorf("Failed to recognize: %v", err)
	}

	if len(resp.Results) > 0 {
		transcription := resp.Results[0].Alternatives[0].Transcript
		return transcription, nil
	}

	return "", fmt.Errorf("no transcription results found")
}
