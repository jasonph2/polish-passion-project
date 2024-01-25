// PodcastGenerator.js

import { useEffect, useState } from 'react';
import { generatePodcast } from '../api';

import '../stylings/PodcastGenerator.css';

export function PodcastGenerator() {
    const [length, setLength] = useState("");
    const [famLevel, setFamLevel] = useState("");
    const [speed, setSpeed] = useState("");
    const [gap, setGap] = useState("");
    const [percent, setPercent] = useState("");
    const [percentOrig, setPercentOrig] = useState("");

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
    const handlePercentChange = (event) => {
        setPercent(event.target.value);
    }
    const handlePercentOrigChange = (event) => {
        setPercentOrig(event.target.value);
    }

    const handleGeneration = () => {
        const fetching = async () => {
            const data = await generatePodcast({ length: length, familiarity_level: famLevel, speed: speed, gap: gap, percent: percent, percent_orig: percentOrig });
            console.log(data);
        };
        fetching();
    }

    return (
        <div className="podcast-generator-container">
            <div className="row">
                <input
                    type='text'
                    value={length}
                    onChange={handleLengthChange}
                    placeholder='Desired Podcast Length'
                    className='podcast-custom-item'
                />
                <input
                    type='text'
                    value={gap}
                    onChange={handleGapChange}
                    placeholder='Time in between words'
                    className='podcast-custom-item'
                />
                <label htmlFor="familiarity-dropdown" className='podcast-custom-item'>Familiarity:</label>
                <select id="familiarity-dropdown" value={famLevel} onChange={handleFamChange} className='podcast-custom-item'>
                    <option value="">-- Choose an option --</option>
                    <option value="Unfamiliar">Unfamiliar</option>
                    <option value="Random">Completely Random</option>
                    <option value="Familiar">Familiar</option>
                </select>
            </div>
            <div className='row'>
                <label htmlFor="speed-dropdown" className='podcast-custom-item'>Speed:</label>
                <select id="speed-dropdown" value={speed} onChange={handleSpeedChange} className='podcast-custom-item'>
                    <option value="">-- Choose an option --</option>
                    <option value="very_slow">Very Slow</option>
                    <option value="slow">Slow</option>
                    <option value="normal">Normal</option>
                    <option value="fast">Fast</option>
                    <option value="very_fast">Very Fast</option>
                </select>
                <label htmlFor="percent-input" className='podcast-custom-item'>Percent of Original Words First:</label>
                <input
                    type='text'
                    value={percentOrig}
                    onChange={handlePercentOrigChange}
                    placeholder='Type as whole number'
                    className='podcast-custom-item'
                />
                %
            </div>
            <div className="row">
                <label htmlFor="percent-input" className='podcast-custom-item'>Percent of podcast using generated phrases:</label>
                <input
                    type='text'
                    value={percent}
                    onChange={handlePercentChange}
                    placeholder='Type as whole number'
                    className='podcast-custom-item'
                />
                %
                <button onClick={handleGeneration} className='generate-button'>Generate Podcast</button>
            </div>
        </div>
    );
}
