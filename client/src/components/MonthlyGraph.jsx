import React from 'react';

const MonthlyListeningGraph = () => {
    return (
        <div>
            <h2>Monthly Listening Time</h2>
            <img src="http://localhost:5000/getmonthlygraph" />
            <h2>Learned Over Time</h2>
            <img src="http://localhost:5000/getlearned" />
        </div>
    )
  };
  
  export default MonthlyListeningGraph;
