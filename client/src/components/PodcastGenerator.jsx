import { useState } from 'react'
import { generatePodcast } from '../api';

export function PodcastGenerator() {
    const [length, setLength] = useState("");
    const [famLevel, setFamLevel] = useState("");
    const [speed, setSpeed] = useState("");
    const handleLengthChange = (event) => {
        setLength(event.target.value);
    } 
    const handleFamChange = (event) => {
        setFamLevel(event.target.value);
    }
    const handleSpeedChange = (event) => {
        setSpeed(event.target.value);
    }
    const handleGeneration = () => {
        const fetching = async () => {
            const data = await generatePodcast({length: length, familiarity_level: famLevel, speed: speed});
            console.log(data);
        }
        fetching();
    }
    return (
        <div>
            <input 
                type='text'
                id='textInput'
                value={length}
                onChange={handleLengthChange}
                placeholder='Desired Podcast Length'
            />
            <input 
                type='text'
                id='textInput'
                value={famLevel}
                onChange={handleFamChange}
                placeholder='Familiarity Level'
            />
            <input 
                type='text'
                id='textInput'
                value={speed}
                onChange={handleSpeedChange}
                placeholder='Speed'
            />
            <button onClick={handleGeneration}>Generate Podcast</button>
        </div>
    )
}