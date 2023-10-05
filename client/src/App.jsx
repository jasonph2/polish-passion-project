import { useState, useEffect } from 'react'
import './App.css'
import { ExampleComponent } from './components/AudioRecorder';

function App() {
  const [helloWorld, setHelloWorld] = useState(null);

  // useEffect(() => {
  //   fetch("http://127.0.0.1:5000/test", {
  //     method: "GET",
  //     mode:"cors",
  //     headers: {
  //       "Content-Type": "application/json"
  //     }
  //   })
  //     .then((response) => response.json())
  //     .then((data) => setHelloWorld(data))
  // }, []);

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
        <ExampleComponent />
      </div>
    </>
  )
}

export default App;
