import { useState } from "react";
import { setToChange } from "../redux/reducer";
import { useDispatch, useSelector } from 'react-redux';
import { AudioElement } from "./AudioRecorder";
import { Form } from "react-bootstrap"

export function GrammarSubmission() {
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

    const handleManualNo = () => {
        setManOrigWord("");
        setManTranWord("");
    }

    return (
        <div>
            <div>
                <button onClick={() => setTab(0)}>Record Audio</button>
                <button onClick={() => setTab(1)}>Add Entry for Saved Audio</button>
            </div>
            <>
            {tab === 0 && (
                <div>
                    <AudioElement />
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
            </>
        </div>
        
    )
}