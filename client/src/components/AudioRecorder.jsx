import { AudioRecorder, useAudioRecorder } from 'react-audio-voice-recorder';
import * as React from 'react'

export function AudioElement() {
  const addAudioElement = (blob) => {
    const url = URL.createObjectURL(blob);
    const audio = document.createElement('audio');
    audio.src = url;
    audio.controls = true;
    document.body.appendChild(audio);
  };

  return (
    <div>
      <AudioRecorder
        onRecordingComplete={addAudioElement}
        audioTrackConstraints={{
          noiseSuppression: true,
          echoCancellation: true,
          // autoGainControl,
          // channelCount,
          // deviceId,
          // groupId,
          // sampleRate,
          // sampleSize,
        }}
        onNotAllowedOrFound={(err) => console.table(err)}
        downloadOnSavePress={true}
        downloadFileExtension="webm"
        mediaRecorderOptions={{
          audioBitsPerSecond: 128000,
        }}
        showVisualizer={true}
      />
      <br />
    </div>
  );
}