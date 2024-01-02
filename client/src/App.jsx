import { useState, useEffect } from 'react'
import './App.css'
import { AudioElement } from './components/AudioRecorder';
import { helloWorld } from './api';
// import YourComponent from './components/reduxTest';
import AudioTable from './components/AudioEntryTable';
import { PodcastGenerator } from './components/PodcastGenerator';
import { WordEntry } from './components/WordEntry';
import { Generator } from './components/Generator';

function App() {
  const [a, setA] = useState(null);

  useEffect(() => {
    const fetching = async () => {
      const data = await helloWorld();
      setA(data);
    }
    fetching();
  }, []);

  useEffect(() => {
    if (self.crossOriginIsolated) {
      console.log("enabled");
    } else {
      console.log("failed");
    }
  }, [])
  
  return (
    <>
      <div className='App'>
        <h1>App to Practice Polish</h1>
        {/* {a &&
          <div>{a.message}</div>
        } */}
      </div>
      <div>
        <PodcastGenerator />
      </div>
      <div>
        <Generator />
      </div>
      {/* <div>
        <AudioElement />
      </div> */}
      <div>
        <WordEntry />
      </div>
      <div>
        <AudioTable />
      </div>
    </>
  )
}

export default App;
