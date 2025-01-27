import { AudioRecorder } from 'react-audio-voice-recorder';
import * as React from 'react';
import { setToChange } from '../redux/reducer';
import { useDispatch, useSelector } from 'react-redux';
import { useState } from 'react';
import { Form } from 'react-bootstrap';
import { uploadGrammarAudio } from '../api';

export function ManualGrammarSubmission() {
  const dispatch = useDispatch();
  const change = useSelector((state) => state.some.toChange);
  const [blob, setBlob] = useState(null);
  const [showSaveButton, setShowSaveButton] = useState(false); 
  const [description, setDescription] = useState("");
  const [name, setName] = useState("");

  const addAudioElement = (event) => {
    const file = event.target.files[0];
    if (file) {
      const blob = new Blob([file], {type: file.type});
      setBlob(blob);
      setShowSaveButton(true);
    } else {
      alert("Please upload a valid .m4a file");
    }
  };

  const handleSaveAudio = () => {
    
    const fetching = async () => {
      const data = await uploadGrammarAudio({name: name, description: description, blob: blob});
      console.log(data);
      dispatch(setToChange(change + 1));
    }
    fetching();
    setShowSaveButton(false);
    setBlob(null);
  };

  const handleDiscardAudio = () => {
    setAudioURL(null);
    setShowSaveButton(false);
    setBlob(null);
  };

  const handleNameChange = (event) => {
    setName(event.target.value);
  }

  const handleDescriptionChange = (event) => {
    setDescription(event.target.value);
  }

  return (
    <div>
      <div>
      <Form>
        <Form.Group controlId="nameInput">
          <Form.Control
            type="text"
            value={name}
            onChange={handleNameChange}
            placeholder="Enter name of lesson"
          />
        </Form.Group>

        {/* Description input field with more vertical space */}
        <Form.Group controlId="descriptionInput">
          <Form.Control
            as="textarea" // Use textarea for multi-line input
            rows={4}      // Adjust the number of rows as needed
            value={description}
            onChange={handleDescriptionChange}
            placeholder="Grammar lesson you are seeking to learn"
          />
        </Form.Group>
      </Form>
        <input 
          type="file"
          accept=".m4a"
          onChange={addAudioElement}
        />
      </div>

      {blob && (
        <div style={{ marginTop: '10px' }}>
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
