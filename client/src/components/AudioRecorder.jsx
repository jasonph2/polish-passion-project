import { AudioRecorder, useAudioRecorder } from 'react-audio-voice-recorder';
import * as React from 'react'
import { setToChange } from '../redux/reducer';
import { useDispatch, useSelector } from 'react-redux';
import { useState } from 'react'

export function AudioElement() {
  const dispatch = useDispatch();
  const change = useSelector((state) => state.some.toChange);
  const [showChoice, setShowChoice] = useState(false);
  const [name, setName] = useState("");

  const addAudioElement = (blob) => {
    const url = URL.createObjectURL(blob);
    const audio = document.createElement('audio');
    audio.src = url;
    audio.controls = true;

    // Create a download link
    const downloadLink = document.createElement('a');
    downloadLink.href = url;
    downloadLink.download = name + ".webm";

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

  const handleUpdate = () => {
    dispatch(setToChange(change + 1));
    setShowChoice(false);
  }

  const handleNo = () => {
    setShowChoice(false);
  }

  const handleNameChange = (event) => {
    setName(event.target.value);
  }

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
        downloadOnSavePress={false}
        downloadFileExtension="webm"
        mediaRecorderOptions={{
          audioBitsPerSecond: 128000,
        }}
        showVisualizer={true}
      />
      <br />
      <input 
        type='text'
        id='textInput'
        value={name}
        onChange={handleNameChange}
        placeholder='Word to Learn'
      />
      {showChoice ? (
        <div>
          did you download the file?
          <button onClick={handleUpdate}>YES</button>
          <button onClick={handleNo}>NO</button>
        </div>
      ) : (
        <></>
      )}
    </div>
  );
}