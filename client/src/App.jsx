import { useState, useEffect } from 'react'
import './App.css'
import { AudioElement } from './components/AudioRecorder';
import { helloWorld } from './api';
// import YourComponent from './components/reduxTest';
import AudioTable from './components/AudioEntryTable';

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
        {a &&
          <div>{a.message}</div>
        }
      </div>
      <div>
        <AudioElement />
      </div>
      {/* <div>
        <YourComponent />
      </div> */}
      <div>
        <AudioTable />
      </div>
    </>
  )
}

export default App;
