import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { setAudioFiles, setToChange } from '../redux/reducer';
import { removeEntry } from '../api';

const AudioTable = () => {
    const dispatch = useDispatch();
    const audioFiles = useSelector((state) => state.some.audioFiles);
    const change = useSelector((state) => state.some.toChange);
  
    useEffect(() => {
        console.log("HERE");
        const fetchAudioList = async () => {
            try {
              const response = await fetch('http://localhost:5000/audio-list');
              const data = await response.json();
              console.log(data);
              dispatch(setAudioFiles(data));
            } catch (error) {
              console.error('Error fetching audio list:', error);
            }
        };
    
        fetchAudioList();
    }, [change]);

    const handleDelete = (path) => {
      const fetching = async () => {
        const data = await removeEntry({path: path});
        console.log(data);
        dispatch(setToChange(change + 1));
      }
      fetching();
    }
  
    return (
      <div>
        {audioFiles && audioFiles.length > 0 ? (
          <table>
            <thead>
              <tr>
                <th>File Name</th>
                <th>File Path</th>
                <th>Play</th>
                <th>Length</th>
                <th>Familiarity</th>
                <th>Delete</th>
              </tr>
            </thead>
            <tbody>
              {audioFiles.map((file, index) => (
                <tr key={index}>
                  <td>{file.word}</td>
                  <td>{file.path}</td>
                  <td>
                    <audio controls>
                      <source src={`http://localhost:5000/audio/${file.path}`} type="audio/webm" />
                      Your browser does not support the audio element.
                    </audio>
                  </td>
                  <td>{file.rec_length}</td>
                  <td>{file.familiarity}</td>
                  <td>
                    <button onClick={() => handleDelete(file.path)}>delete</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <p>No audio files found.</p>
        )}
      </div>
    );
  };
  
  export default AudioTable;
