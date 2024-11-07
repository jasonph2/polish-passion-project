// PodcastGenerator.js

import { useEffect, useState } from 'react';
import { generatePodcast } from '../api';
import { Container, Row, Col, Form, Button } from 'react-bootstrap';

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
    
    const handleGenerateAll = () => {
        const fetching = async () => {
            const data = await generatePodcast({ length: 1, familiarity_level: "All", speed: "fast", gap: 2, percent: 0, percent_orig: 0 });
            console.log(data);
        };
        fetching();
    }

    return (
        <Container className="podcast-generator-container">
            {/* Row 1 */}
            <Row className="mb-3">
                <Col xs={12} md={4}>
                    <Form.Group controlId="length-input">
                        <Form.Label>Desired Podcast Length:</Form.Label>
                        <Form.Control
                            type="text"
                            value={length}
                            onChange={handleLengthChange}
                            placeholder="Type as whole number"
                        />
                    </Form.Group>
                </Col>
                <Col xs={12} md={4}>
                    <Form.Group controlId="gap-input">
                        <Form.Label>Time in between words:</Form.Label>
                        <Form.Control
                            type="text"
                            value={gap}
                            onChange={handleGapChange}
                            placeholder="Type as whole number"
                        />
                    </Form.Group>
                </Col>
                <Col xs={12} md={4}>
                    <Form.Group controlId="familiarity-dropdown">
                        <Form.Label>Familiarity:</Form.Label>
                        <Form.Select value={famLevel} onChange={handleFamChange}>
                            <option value="">-- Choose an option --</option>
                            <option value="Unfamiliar">Unfamiliar</option>
                            <option value="Random">Completely Random</option>
                            <option value="Familiar">Familiar</option>
                        </Form.Select>
                    </Form.Group>
                </Col>
            </Row>

            {/* Row 2 */}
            <Row className="mb-3">
                <Col xs={12} md={4}>
                    <Form.Group controlId="speed-dropdown">
                        <Form.Label>Speed:</Form.Label>
                        <Form.Select value={speed} onChange={handleSpeedChange}>
                            <option value="">-- Choose an option --</option>
                            <option value="very_slow">Very Slow</option>
                            <option value="slow">Slow</option>
                            <option value="normal">Normal</option>
                            <option value="fast">Fast</option>
                            <option value="very_fast">Very Fast</option>
                        </Form.Select>
                    </Form.Group>
                </Col>
                <Col xs={12} md={4}>
                    <Form.Group controlId="percent-orig-input">
                        <Form.Label>Percent of Original Words First:</Form.Label>
                        <Form.Control
                            type="text"
                            value={percentOrig}
                            onChange={handlePercentOrigChange}
                            placeholder="Type as whole number"
                        />
                    </Form.Group>
                </Col>
                <Col xs={12} md={4}>
                    <Form.Group controlId="percent-input">
                        <Form.Label>Percent with generated phrases:</Form.Label>
                        <Form.Control
                            type="text"
                            value={percent}
                            onChange={handlePercentChange}
                            placeholder="Type as whole number"
                        />
                    </Form.Group>
                </Col>
            </Row>

            {/* Row 3 */}
            <Row className="mb-3">
                <Col>
                    <Button variant="primary" onClick={handleGeneration} className="generate-button">
                        Generate Podcast
                    </Button>
                </Col>
            </Row>

            {/* Row 4 */}
            <Row>
                <Col>
                    <Button variant="secondary" onClick={handleGenerateAll} className="generate-all-button">
                        Generate Podcast of All Saved Words
                    </Button>
                </Col>
            </Row>
        </Container>
    );
}
