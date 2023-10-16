// Your React component
import React from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { setDict } from '../redux/reducer';

const YourComponent = () => {
  const dictionary = useSelector((state) => state.some.dictionary);
  const dispatch = useDispatch();

  const handleSetDict = () => {
    const newValues = {
      key1: 'value3',
      key2: 'value4',
    };
    dispatch(setDict(newValues));
  };

  return (
    <div>
      <p>Dictionary Values:</p>
      <ul>
        {Object.entries(dictionary).map(([key, value]) => (
          <li key={key}>
            {key}: {value}
          </li>
        ))}
      </ul>
      <button onClick={handleSetDict}>Set Dictionary</button>
    </div>
  );
};

export default YourComponent;
