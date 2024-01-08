import React from 'react';
import { BrowserRouter as Router, Route, NavLink, Routes } from 'react-router-dom';
import './App.css';
import AudioTable from './components/AudioEntryTable';
import { PodcastGenerator } from './components/PodcastGenerator';
import { WordEntry } from './components/WordEntry';
import PodcastHistoryTable from './components/PodcastHistoryTable';

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

function App() {
  return (
    <Router>
      <div className="App">
        <h1>App to Practice Polish</h1>
      </div>

      <nav className="navbar">
        <NavLink to="/word-and-audio" className="nav-link">
          Word and Audio
        </NavLink>
        <NavLink to="/podcast-generator" className="nav-link">
          Podcast Generator
        </NavLink>
      </nav>

      <div className="content">
        <Routes>
          <Route path="/podcast-generator" element={<PodcastTab />} />
          <Route path="/word-and-audio" element={<WordAndAudioTab />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
