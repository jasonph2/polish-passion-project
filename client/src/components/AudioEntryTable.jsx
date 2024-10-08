import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { setAudioFiles, setToChange } from '../redux/reducer';
import { getAudioList, removeEntry, updateFamLevel } from '../api';

const AudioTable = () => {
    const dispatch = useDispatch();
    const audioFiles = useSelector((state) => state.some.audioFiles);
    const change = useSelector((state) => state.some.toChange);
    const [currPage, setCurrPage] = useState(1);
    const rowsPerPage = 10;
    const totalPages = Math.ceil(audioFiles.length / rowsPerPage);
  
    useEffect(() => {
        const fetchAudioList = async () => {
            try {
              const response = await getAudioList();
              dispatch(setAudioFiles(response));
            } catch (error) {
              console.error('Error fetching audio list:', error);
            }
        };
    
        fetchAudioList();
    }, [change]);

    useEffect(() => {
      console.log('Audio files in state:', audioFiles);
    }, [audioFiles]);
  

    const handleDelete = (translated_path, original_path) => {
      const fetching = async () => {
        const data = await removeEntry({translated_path: translated_path, original_path: original_path});
        console.log(data);
        dispatch(setToChange(change + 1));
      }
      fetching();
    }

    const handleFamChange = (event, id) => {
      const fetching = async () => {
        const data = await updateFamLevel({id: id, familiarity_level: event.target.value});
        console.log(data);
        dispatch(setToChange(change + 1));
      }
      fetching();
    }

    const currFiles = audioFiles.slice((currPage - 1) * rowsPerPage, currPage * rowsPerPage);
    const handlePreviousPage = () => {
      if (currPage > 1) {
        setCurrPage(currPage - 1)
      }
    }

    const handleNextPage = () => {
      if (currPage < totalPages) {
        setCurrPage(currPage + 1)
      }
    }
    
    const handleFirstPage = () => {
      setCurrPage(1);
    }

    const handleLastPage = () => {
      setCurrPage(totalPages);
    }
  
    return (
      <div>
        <h3>List of Saved Files</h3>
        <div>Familiarty levels</div>
        <div> 1- never seen this word/phrase before</div>
        <div> 2- I recognize this word/phrase, but do not know it</div>
        <div> 3- I am in the process of learning this word/phrase</div>
        <div> 4- I can translate this word/phrase both ways relatively consistently</div>
        <div> 5- I can apply this word/phrase to a sentence in conversation</div>
        {audioFiles && audioFiles.length > 0 ? (
          <>
            <table>
              <thead>
                <tr>
                  <th>English Word</th>
                  <th>Polish Word</th>
                  <th>Play</th>
                  <th>Familiarity</th>
                  <th>Delete</th>
                </tr>
              </thead>
              <tbody>
                {currFiles.map((file) => (
                  <tr key={file.id}>
                    <td>{file.original_word}</td>
                    <td>{file.translated_word}</td>
                    <td>
                      <audio key={file.id} controls>
                        <source src={`http://localhost:5000/audio/${file.translated_path}`} type="audio/webm" />
                        Your browser does not support the audio element.
                      </audio>
                    </td>
                    <>
                      <select id="dropdown" value={file.familiarity} onChange={(event) => handleFamChange(event, file.id)}>
                          <option value="">-- Choose an option --</option>
                          <option value="1">1</option>
                          <option value="2">2</option>
                          <option value="3">3</option>
                          <option value="4">4</option>
                          <option value="5">5</option>
                      </select>
                    </>
                    <td>
                      <button onClick={() => handleDelete(file.translated_path, file.original_path)}>delete</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
            <div className="pagination-controls">
              <button onClick={handleFirstPage} disabled={currPage === 1}>
                First
              </button>
              <button onClick={handlePreviousPage} disabled={currPage === 1}>
                Previous
              </button>
              <span>
                Page {currPage} of {totalPages}
              </span>
              <button onClick={handleNextPage} disabled={currPage === totalPages}>
                Next
              </button>
              <button onClick={handleLastPage} disabled={currPage === totalPages}>
                Last
              </button>
            </div>
          </>
        ) : (
          <p>No audio files found.</p>
        )}
      </div>
    );
  };
  
  export default AudioTable;
