import { useState, useEffect } from 'react'
import './App.css'

function App() {
  const [helloWorld, setHelloWorld] = useState(null);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/test")
      .then((response) => response.json())
      .then((data) => setHelloWorld(data))
  }, []);

  return (
    <>
      <div className='App'>
        <h1>App to Practice Polish</h1>
        {helloWorld &&
          <div>{helloWorld.message}</div>
        }
      </div>
    </>
  )
}

export default App;
