import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { setAudioFiles, setToChange } from '../redux/reducer';
import { getAudioList, removeEntry, updateFamLevel, updateKnown } from '../api';
import { Table, Button, Form, Pagination, InputGroup } from 'react-bootstrap';
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import { format, parseISO } from 'date-fns'

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

    const handleKnownChange = (known, id) => {
      const fetching = async () => {
        const adjusted = known ? format(known, 'yyyy-MM-dd') : '';
        const data = await updateKnown({id: id, known: adjusted});
        console.log(data);
        dispatch(setToChange(change + 1));
      }
      fetching();
    }

    
    const [searchQuery, setSearchQuery] = useState("");

    const filteredWords = audioFiles.filter(
      (word) =>
        word.original_word.toLowerCase().includes(searchQuery.toLowerCase()) ||
        word.translated_word.toLowerCase().includes(searchQuery.toLowerCase())
    );

    const currFiles = filteredWords.slice((currPage - 1) * rowsPerPage, currPage * rowsPerPage);

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
      <h3 className="text-center">List of Saved Files</h3>
      
      {/* Centering familiarity level descriptions */}
      <div className="text-center mb-4">
        <strong>Familiarity levels:</strong>
        <div className="d-flex flex-column align-items-center">
          <div>1 - Never seen this word/phrase before</div>
          <div>2 - I recognize this word/phrase, but do not know it</div>
          <div>3 - I am in the process of learning this word/phrase</div>
          <div>4 - I can translate this word/phrase both ways relatively consistently</div>
          <div>5 - I can apply this word/phrase to a sentence in conversation</div>
        </div>
      </div>

      {audioFiles && audioFiles.length > 0 ? (
        <>
          <Table bordered hover responsive className="text-center">
          <thead>
              <tr>
                <th colSpan="6" className="p-2">
                  <div className="d-flex justify-content-end">
                    <InputGroup style={{ maxWidth: "300px" }}>
                      <Form.Control
                        type="text"
                        placeholder="Search words..."
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                      />
                      {/* <Button variant="primary" disabled>
                        🔍
                      </Button> */}
                    </InputGroup>
                  </div>
                </th>
              </tr>
            </thead>
            <thead>
              <tr>
                <th>English Word</th>
                <th>Polish Word</th>
                <th>Play</th>
                <th>Familiarity</th>
                <th>Delete</th>
                <th>Learned Date</th>
              </tr>
            </thead>
            <tbody>
              {currFiles.map((file) => {
                const selectedDate = file.known ? parseISO(file.known) : null;

                const handleDateChangeWrapper = (date) => {
                  handleKnownChange(date, file.id);
                };
              return (
                <tr key={file.id}>
                  <td className="align-middle">{file.original_word}</td>
                  <td className="align-middle">{file.translated_word}</td>
                  <td className="align-middle">
                    <audio controls>
                      <source src={`http://localhost:5000/audio/${file.translated_path}`} type="audio/webm" />
                      Your browser does not support the audio element.
                    </audio>
                  </td>
                  <td className="align-middle">
                    <Form.Select
                      className="text-center"
                      value={file.familiarity}
                      onChange={(event) => handleFamChange(event, file.id)}
                    >
                      <option value="">-- Choose an option --</option>
                      <option value="1">1</option>
                      <option value="2">2</option>
                      <option value="3">3</option>
                      <option value="4">4</option>
                      <option value="5">5</option>
                    </Form.Select>
                  </td>
                  <td className="align-middle">
                    <Button variant="danger" onClick={() => handleDelete(file.translated_path, file.original_path)}>
                      Delete
                    </Button>
                  </td>
                  <td className="align-middle">
                    <Form.Control
                      as={DatePicker} 
                      selected={selectedDate}
                      onChange={handleDateChangeWrapper}
                      dateFormat="yyyy-MM-dd"
                      className="text-center"
                      placeholderText="Select a date"
                    />
                  </td>
                </tr>
              );})}
            </tbody>
          </Table>

          <Pagination className="justify-content-center">
            <Pagination.First onClick={handleFirstPage} disabled={currPage === 1} />
            <Pagination.Prev onClick={handlePreviousPage} disabled={currPage === 1} />
            <Pagination.Item active>{`Page ${currPage} of ${totalPages}`}</Pagination.Item>
            <Pagination.Next onClick={handleNextPage} disabled={currPage === totalPages} />
            <Pagination.Last onClick={handleLastPage} disabled={currPage === totalPages} />
          </Pagination>
        </>
      ) : (
        <p className="text-center">No audio files found.</p>
      )}
    </div>
    );
  };
  
  export default AudioTable;
