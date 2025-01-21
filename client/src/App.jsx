import React from 'react';
import { BrowserRouter as Router, Route, NavLink, Routes } from 'react-router-dom';
import { Navbar, Nav } from 'react-bootstrap';
import './App.css';
import AudioTable from './components/AudioEntryTable';
import { PodcastGenerator } from './components/PodcastGenerator';
import { WordEntry } from './components/WordEntry';
import PodcastHistoryTable from './components/PodcastHistoryTable';
import { GrammarSubmission } from './components/GrammarSubmission';
import GTable from './components/GrammarTable';

const WordAndAudioTab = () => (
  <>
    <WordEntry />
    <AudioTable />
  </>
);

const PodcastTab = () => (
  <>
    <PodcastGenerator />
    <PodcastHistoryTable />
  </>
)

const GrammarTab = () => (
  <>
    <GrammarSubmission />
    <GTable />
  </>
)

function App() {
  return (
    <Router>
      <div className="App">
        <h1>App to Practice Polish</h1>
      </div>

      <Navbar bg="light" expand="lg">
          <Navbar.Toggle aria-controls="basic-navbar-nav" />
          <Navbar.Collapse id="basic-navbar-nav">
              <Nav className="me-auto">
                  <Nav.Link as={NavLink} to="/word-and-audio" activeClassName="active">
                      Word and Audio
                  </Nav.Link>
                  <Nav.Link as={NavLink} to="/podcast-generator" activeClassName="active">
                      Podcast Generator
                  </Nav.Link>
                  <Nav.Link as={NavLink} to="/grammar-hub" activeClassName="active">
                      Grammar Hub
                  </Nav.Link>
              </Nav>
          </Navbar.Collapse>
      </Navbar>

      <div className="content">
        <Routes>
          <Route path="/podcast-generator" element={<PodcastTab />} />
          <Route path="/word-and-audio" element={<WordAndAudioTab />} />
          <Route path="/grammar-hub" element={<GrammarTab />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
