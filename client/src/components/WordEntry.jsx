import { useState } from "react";
import { getAudio, removeAudio, submitWord } from '../api';
import { setToChange } from "../redux/reducer";
import { useDispatch, useSelector } from 'react-redux';

export function WordEntry() {
    const [word, setWord] = useState("");
    const [path, setPath] = useState("");
    const change = useSelector((state) => state.some.toChange);
    const dispatch = useDispatch();

    const handleWordChange = (event) => {
        setWord(event.target.value);
    }

    const handleGetAudio = () => {
        const fetching = async () => {
            const data = await getAudio({word: word});
            console.log(data);
            setPath(data.path);
        }
        fetching();
    }

    const handleSubmission = () => {
        const fetching = async () => {
            const data = await submitWord({word: word, path: path, familiarity: 1});
            console.log(data);
            dispatch(setToChange(change + 1));
        }
        fetching();
        setPath("");
    }

    const handleNo = () => {
        const fetching = async () => {
            const data = await removeAudio({path: path});
            console.log(data);
            setPath("");
        }
        fetching();
        setPath("");
    }

    return (
        <div>
            <input 
                type='text'
                id='textInput'
                value={word}
                onChange={handleWordChange}
                placeholder='Word to Learn'
            />
            <button onClick={handleGetAudio}>Get Audio</button>
            {path ? (
                <div>
                    <audio controls>
                        <source src={`http://localhost:5000/audio/${path}`} type="audio/webm" />
                        Your browser does not support the audio element.
                    </audio>
                    <div>Add Word?</div>
                    <button onClick={handleSubmission}>Yes</button>
                    <button onClick={handleNo}>No</button>
                </div>
            ) : (
                <></>
            )}
        </div>
    )
}