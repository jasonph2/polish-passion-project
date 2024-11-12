import { AudioRecorder } from 'react-audio-voice-recorder';
import * as React from 'react';
import { setToChange } from '../redux/reducer';
import { useDispatch, useSelector } from 'react-redux';
import { useState } from 'react';
import { Form } from 'react-bootstrap';
import { uploadGrammarAudio } from '../api';

export function AudioElement() {
  const dispatch = useDispatch();
  const change = useSelector((state) => state.some.toChange);
  const [blob, setBlob] = useState(null);
  const [audioURL, setAudioURL] = useState(null); 
  const [showSaveButton, setShowSaveButton] = useState(false); 
  const [description, setDescription] = useState("");

  const addAudioElement = (blob, arg) => {
    const url = URL.createObjectURL(blob);
    setBlob(blob);
    setAudioURL(url); // Store the audio URL in state
    setShowSaveButton(true); // Show save/discard options when recording completes
  };

  const handleSaveAudio = () => {
    
    const fetching = async () => {
      const data = await uploadGrammarAudio({description: description, blob: blob});
      console.log(data);
      dispatch(setToChange(change + 1));
    }
    fetching();
    setShowSaveButton(false);
    setAudioURL(null); 
    setBlob(null);
  };

  const handleDiscardAudio = () => {
    setAudioURL(null);
    setShowSaveButton(false);
    setBlob(null);
  };

  const handleDescriptionChange = (event) => {
    setDescription(event.target.value);
  }

  return (
    <div>
      <div>
        <Form.Group controlId="textInput">
            <Form.Control 
                type='text'
                value={description}
                onChange={handleDescriptionChange}
                placeholder='grammar lesson you are seeking to learn'
            />
        </Form.Group>
        <AudioRecorder
          onRecordingComplete={(blob) => addAudioElement(blob, "")}
          audioTrackConstraints={{
            noiseSuppression: true,
            echoCancellation: true,
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

      {/* Display the audio, save, and discard options next to the recorder icon */}
      {audioURL && (
        <div style={{ marginTop: '10px' }}>
          <audio controls src={audioURL} />
          {showSaveButton && (
            <div style={{ display: 'flex', gap: '10px', marginTop: '5px' }}>
              <button onClick={handleSaveAudio}>Save</button>
              <button onClick={handleDiscardAudio}>
                Discard
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
