import { useEffect, useState } from 'react'
import { generatePodcast } from '../api';

export function PodcastGenerator() {
    const [length, setLength] = useState("");
    const [famLevel, setFamLevel] = useState("");
    const [speed, setSpeed] = useState("");
    const [gap, setGap] = useState("");
    const [email, setEmail] = useState("");
    const [selectedOption, setSelectedOption] = useState('');

    const handleLengthChange = (event) => {
        setLength(event.target.value);
    } 
    const handleFamChange = (event) => {
        setFamLevel(event.target.value);
    }
    const handleSpeedChange = (event) => {
        setSpeed(event.target.value);
    }
    const handleGapChange = (event) => {
        setGap(event.target.value);
    }
    const handleEmailChange = (event) => {
        setEmail(event.target.value);
    }
    const handleGeneration = () => {
        const fetching = async () => {
            const data = await generatePodcast({length: length, familiarity_level: famLevel, speed: speed, gap: gap, email: email});
            console.log(data);
        }
        fetching();
    }

    return (
        <div>
            <div>
                <input 
                    type='text'
                    id='textInput'
                    value={length}
                    onChange={handleLengthChange}
                    placeholder='Desired Podcast Length'
                />
                <>
                    <label htmlFor="dropdown">Familiarity:</label>
                    <select id="dropdown" value={famLevel} onChange={handleFamChange}>
                        <option value="">-- Choose an option --</option>
                        <option value="unfamiliar">Unfamiliar</option>
                        <option value="random">Completely Random</option>
                        <option value="familiar">Normal</option>
                    </select>
                </>
                <>
                    <label htmlFor="dropdown">Speed:</label>
                    <select id="dropdown" value={speed} onChange={handleSpeedChange}>
                        <option value="">-- Choose an option --</option>
                        <option value="very_slow">Very Slow</option>
                        <option value="slow">Slow</option>
                        <option value="normal">Normal</option>
                        <option value="fast">Fast</option>
                        <option value="very_fast">Very Fast</option>
                    </select>
                </>
                <button onClick={handleGeneration}>Generate Podcast</button>
            </div>
            <div>
                <input 
                    type='text'
                    id='textInput'
                    value={gap}
                    onChange={handleGapChange}
                    placeholder='Time in between words'
                />
                <input 
                    type='text'
                    id='textInput'
                    value={email}
                    onChange={handleEmailChange}
                    placeholder='email to send the podcast to'
                />
            </div>
        </div>
    )
}