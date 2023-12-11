import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { setAudioFiles } from '../redux/reducer';

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

    const handleDelete = () => {
        console.log("time to delete");
    }
  
    return (
      <div>
        {audioFiles && audioFiles.length > 0 ? (
          <table>
            <thead>
              <tr>
                <th>File Name</th>
                <th>Play</th>
                <th>Delete</th>
              </tr>
            </thead>
            <tbody>
              {audioFiles.map((filename, index) => (
                <tr key={index}>
                  <td>{filename}</td>
                  <td>
                    <audio controls>
                      <source src={`http://localhost:5000/audio/${filename}`} type="audio/webm" />
                      Your browser does not support the audio element.
                    </audio>
                  </td>
                  <td>
                    <button onClick={handleDelete} />
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
