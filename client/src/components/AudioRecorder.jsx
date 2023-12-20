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
    } else {
      const adjusted = name.replace(/ /g, "_");
      const tempStr = adjusted + "-" + generateRandomString(15) + ".webm"
      setPolishFileName(tempStr);
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

  const handleUpdate = (name) => {
    const fetching = async () => {
      const data = await addEntry({name: name, polish_file_name: polishFileName, familiarity: 1, english_file_name: englishFileName, translated_word: translatedWord});
      console.log(data);
      dispatch(setToChange(change + 1));
    }
    fetching();
    setShowChoice(false);
    setName("");
  }

  const handleNo = () => {
    setShowChoice(false);
  }

  const handleNameChange = (event) => {
    setName(event.target.value);
  }

  const handleTranslatedWordChange = (event) => {
    setTranslatedWord(event.target.value);
  }

  return (
    <div>
      <div>
        Polish Recorder
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
      <div>
        English Recorder
        <AudioRecorder
          onRecordingComplete={(blob) => addAudioElement(blob, "English")}
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
      <br />
      <input 
        type='text'
        id='textInput'
        value={name}
        onChange={handleNameChange}
        placeholder='Word to Learn'
      />
      <input 
        type='text'
        id='textInput'
        value={translatedWord}
        onChange={handleTranslatedWordChange}
        placeholder='Word to Learn'
      />
      {showChoice ? (
        <div>
          did you download both of the files?
          <button onClick={() => handleUpdate(name)}>YES</button>
          <button onClick={handleNo}>NO</button>
        </div>
      ) : (
        <></>
      )}
    </div>
  );
}