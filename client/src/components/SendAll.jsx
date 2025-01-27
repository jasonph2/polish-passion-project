import * as React from 'react';
import { Button } from 'react-bootstrap';
import { sendAll } from '../api';

export function SendAll() {

  const handleSend = () => {
    const fetching = async () => {
      const data = await sendAll();
      console.log(data);
    }
    fetching();
  };

  return (
    <div>
        <Button onClick={handleSend}>
            Send All Words to Tutor
        </Button>
    </div>
      
  );
}
