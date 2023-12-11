import React, { useEffect, useState } from 'react';

const AudioTable = () => {
    const [audioFiles, setAudioFiles] = useState([]);
  
    useEffect(() => {
      const fetchAudioList = async () => {
        try {
          const response = await fetch('http://localhost:5000/audio-list');
          const data = await response.json();
          setAudioFiles(data);
        } catch (error) {
          console.error('Error fetching audio list:', error);
        }
      };
  
      fetchAudioList();
    }, []);
  
    return (
      <div>
        {audioFiles.length > 0 ? (
          <table>
            <thead>
              <tr>
                <th>File Name</th>
                <th>Play</th>
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
