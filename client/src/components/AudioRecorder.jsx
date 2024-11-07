import { AudioRecorder, useAudioRecorder } from 'react-audio-voice-recorder';
import * as React from 'react'
import { setToChange } from '../redux/reducer';
import { useDispatch, useSelector } from 'react-redux';
import { useState } from 'react'
// import { addEntry } from '../api';
import { generateRandomString } from '../utilities/randomstring';

export function AudioElement() {
  const dispatch = useDispatch();
  const change = useSelector((state) => state.some.toChange);
  const [showChoice, setShowChoice] = useState(false);
  const [name, setName] = useState("");
  const [polishFileName, setPolishFileName] = useState("");
  const [englishFileName, setEnglishFileName] = useState("");
  const [randomString, setRandomString] = useState("");
  const [translatedWord, setTranslatedWord] = useState("");


  const addAudioElement = (blob, arg) => {
    const url = URL.createObjectURL(blob);
    const audio = document.createElement('audio');
    audio.src = url;
    audio.controls = true;

    // Create a download link
    const downloadLink = document.createElement('a');
    downloadLink.href = url;
    if (arg != "") {
      const adjusted = name.replace(/ /g, "_");
      const tempStr = adjusted + "-" + arg + "-" + generateRandomString(15) + ".webm"
      setEnglishFileName(tempStr);
      downloadLink.download = tempStr;
    }   

    // Append the audio element and download link to the document
    document.body.appendChild(audio);
    document.body.appendChild(downloadLink);

    // Simulate a click on the download link to initiate the download
    downloadLink.click();

    // Remove the elements from the document
    document.body.removeChild(audio);
    document.body.removeChild(downloadLink);


    // document.body.appendChild(audio);
    setShowChoice(true);
  };

  return (
    <div>
      <div>
        <AudioRecorder
          onRecordingComplete={(blob) => addAudioElement(blob, "")}
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
          downloadOnSavePress={false}
          downloadFileExtension="webm"
          mediaRecorderOptions={{
            audioBitsPerSecond: 128000,
          }}
          showVisualizer={true}
        />
      </div>
    </div>
  );
}