import { useState } from "react";
import { getAudio, removeAudio, submitWord, submitManualWord, getFreqWords } from '../api';
import { setToChange } from "../redux/reducer";
import { useDispatch, useSelector } from 'react-redux';

export function WordEntry() {
    const [word, setWord] = useState("");
    const [path, setPath] = useState("");
    const [tab, setTab] = useState(0);
    const [manOrigWord, setManOrigWord] = useState("");
    const [manTranWord, setManTranWord] = useState("");
    const [freq, setFreq] = useState("");
    const change = useSelector((state) => state.some.toChange);
    const dispatch = useDispatch();

    const handleManualOrigWordChange = (event) => {
        setManOrigWord(event.target.value);
    }

    const handleManualTranWordChange = (event) => {
        setManTranWord(event.target.value);
    }

    const handleWordChange = (event) => {
        setWord(event.target.value);
    }

    const handleFreqChange = (event) => {
        setFreq(event.target.value);
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

    const handleManualSubmission = () => {
        const fetching = async () => {
            const data = await submitManualWord({original_word: manOrigWord, translated_word: manTranWord, familiarity: 1});
            console.log(data);
            dispatch(setToChange(change + 1));
        }
        fetching();
        setManOrigWord("");
        setManTranWord("");
    }

    const handleGetFreqWords = () => {
        const fetching = async () => {
            const data = await getFreqWords({freq: freq});
            console.log(data);
            dispatch(setToChange(change + 1));
        }
        fetching();
        setFreq("");
    }

    const handleManualNo = () => {
        setManOrigWord("");
        setManTranWord("");
    }

    return (
        <div>
            <div>
                <button onClick={() => setTab(0)}>Automatic Entry</button>
                <button onClick={() => setTab(1)}>Manual Entry</button>
                <button onClick={() => setTab(2)}>Frequency Entry</button>
            </div>
            <>
            {tab === 0 && (
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
            )}
            {tab === 1 && (
                <div style={{padding: '10px' }}>
                    <input 
                        type='text'
                        id='textInput'
                        value={manOrigWord}
                        onChange={handleManualOrigWordChange}
                        placeholder='Original Word to Learn'
                        style={{padding: '2px', marginRight: '4px' }}
                    />
                    <input 
                        type='text'
                        id='textInput'
                        value={manTranWord}
                        onChange={handleManualTranWordChange}
                        placeholder='Translated Word to Learn'
                        style={{padding: '2px', marginLeft: '4px' }}
                    />
                    {manOrigWord !== "" && manTranWord != "" ? (
                        <div>
                            <div>Add Word?</div>
                            <button onClick={handleManualSubmission}>Yes</button>
                            <button onClick={handleManualNo}>No</button>
                        </div>
                    ) : (
                        <></>
                    )}
                </div>
            ) }
            {tab === 2 && (
                <div>
                    <input 
                        type='text'
                        id='textInput'
                        value={freq}
                        onChange={handleFreqChange}
                        placeholder='Amount of new words'
                    />
                    <button onClick={handleGetFreqWords}>Add Words</button>
                </div>
            )}
            </>
        </div>
        
    )
}