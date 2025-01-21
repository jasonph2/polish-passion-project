import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { setLtl, setToChange } from '../redux/reducer';
import { getLessonList, removeLessonEntry, updateLessonFamLevel } from '../api';
import { Table, Button, Form, Pagination } from 'react-bootstrap';
import "react-datepicker/dist/react-datepicker.css";

const GTable = () => {
    const dispatch = useDispatch();
    const change = useSelector((state) => state.some.toChange);
    const ltl = useSelector((state) => state.some.ltl);
    const [currPage, setCurrPage] = useState(1);
    const [lessons, setLessons] = useState([]);
    const rowsPerPage = 10;
    const totalPages = Math.ceil(lessons.length / rowsPerPage);
  
    useEffect(() => {
        const fetchLessonList = async () => {
            try {
              const response = await getLessonList();
              setLessons(response);
            } catch (error) {
              console.error('Error fetching audio list:', error);
            }
        };
    
        fetchLessonList();
    }, [change]);
  

    const handleDelete = (id, path) => {
      const fetching = async () => {
        const data = await removeLessonEntry({id: id, path: path});
        console.log(data);
        const updatedLtl = ltl.filter((rowId) => rowId !== id);
        dispatch(setLtl(updatedLtl));
        dispatch(setToChange(change + 1));
      }
      fetching();
    }

    const handleFamChange = (event, id) => {
      const fetching = async () => {
        const data = await updateLessonFamLevel({id: id, familiarity_level: event.target.value});
        console.log(data);
        dispatch(setToChange(change + 1));
      }
      fetching();
    }

    // const handleKnownChange = (known, id) => {
    //   const fetching = async () => {
    //     const adjusted = known ? format(known, 'yyyy-MM-dd') : '';
    //     const data = await updateKnown({id: id, known: adjusted});
    //     console.log(data);
    //     dispatch(setToChange(change + 1));
    //   }
    //   fetching();
    // }

    const currFiles = lessons.slice((currPage - 1) * rowsPerPage, currPage * rowsPerPage);
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

    const handleCheckboxChange = (id) => {
        const updatedLtl = ltl.includes(id)
          ? ltl.filter((rowId) => rowId !== id)
          : [...ltl, id]; 
        console.log(updatedLtl);
        dispatch(setLtl(updatedLtl));
    };
  
    return (
      <div>
      <h3 className="text-center">List of Saved Files</h3>
      
      {/* Centering familiarity level descriptions */}
      <div className="text-center mb-4">
        <strong>Familiarity levels:</strong>
        <div className="d-flex flex-column align-items-center">
          <div>1 - Never seen this lesson before</div>
          <div>2 - I recognize this lesson, but barely</div>
          <div>3 - I am in the process of learning this lesson</div>
          <div>4 - I am close to understanding this lesson</div>
          <div>5 - I can apply this lesson to a sentence in conversation</div>
        </div>
      </div>

      {lessons && lessons.length > 0 ? (
        <>
          <Table bordered hover responsive className="text-center">
            <thead>
              <tr>
                <th>Lesson Name</th>
                <th>Description</th>
                <th>Familiarity</th>
                <th>Delete</th>
                <th>To Learn</th>
              </tr>
            </thead>
            <tbody>
              {currFiles.map((file) => {
                // const selectedDate = file.known ? parseISO(file.known) : null;

                // const handleDateChangeWrapper = (date) => {
                //   handleKnownChange(date, file.id);
                // };
              return (
                <tr key={file.id}>
                  <td className="align-middle">{file.name}</td>
                  <td className="align-middle">{file.description}</td>
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
                    <Button variant="danger" onClick={() => handleDelete(file.id, file.path)}>
                      Delete
                    </Button>
                  </td>
                  <td className="align-middle">
                    <Form>
                        <Form.Check 
                        type="checkbox" 
                        checked={ltl.includes(file.id)} 
                        onChange={() => handleCheckboxChange(file.id)} 
                        />
                    </Form>
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
  
  export default GTable;
