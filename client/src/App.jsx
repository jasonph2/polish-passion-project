import { useState, useEffect } from 'react'
import './App.css'
import { AudioElement, ExampleComponent } from './components/AudioRecorder';
import YourComponent from './components/reduxTest';

function App() {
  const [helloWorld, setHelloWorld] = useState(null);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/test", {
      method: "GET",
      mode:"cors",
      headers: {
        "Content-Type": "application/json"
      }
    })
      .then((response) => response.json())
      .then((data) => setHelloWorld(data))
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
        {helloWorld &&
          <div>{helloWorld.message}</div>
        }
      </div>
      <div>
        <AudioElement />
      </div>
      <div>
        <YourComponent />
      </div>
    </>
  )
}

export default App;
