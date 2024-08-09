import React, { useEffect, useState } from 'react';

import { getPodcastList, removePodcastEntry, updateListenedStatus } from '../api';
import { formatSeconds } from '../utilities/secondstoms';

export function PodcastHistoryTable() {
    const [change, setChange] = useState(0);
    const [podcasts, setPodcasts] = useState(null);
    const [totalDur, setTotalDur] = useState("");
  
    useEffect(() => {
        const fetchPodcasts = async () => {
            try {
              const response = await getPodcastList();
              setPodcasts(response);
            } catch (error) {
              console.error('Error fetching audio list:', error);
            }
        };
    
        fetchPodcasts();
    }, [change]);
  

    const handleDelete = (id) => {
      const fetching = async () => {
        const data = await removePodcastEntry({id: id});
        console.log(data);
        setChange(change + 1)
      }
      fetching();
    }

    const handleListenedChange = (event, id) => {
      const fetching = async () => {
        const data = await updateListenedStatus({id: id, listened: event.target.value});
        console.log(data);
        setChange(change + 1)
      }
      fetching();
    }

    const getTotalListenedDuration = () => {
      if (podcasts && podcasts.length > 0) {
        // const listenedPodcasts = podcasts.filter((pod) => pod.listened === "1");
        const totalDurationInSeconds = podcasts.reduce((sum, pod) => {
          const mult = parseFloat(pod.listened);
          const dur = parseFloat(pod.duration);
          return sum + (mult * dur);
        }, 0);
        setTotalDur(formatSeconds(totalDurationInSeconds));
      }
    };

    useEffect(() => {
      getTotalListenedDuration();
    }, [podcasts]);
  
    return (
      <div>
        <h3>List of Generated Podcasts</h3>
        {podcasts && podcasts.length > 0 ? (
          <>
            <table>
              <thead>
                <tr>
                  <th>Date</th>
                  <th>Duration</th>
                  <th>Generated %</th>
                  <th>Familiarity</th>
                  <th>Listened</th>
                  <th>Delete</th>
                </tr>
              </thead>
              <tbody>
                {podcasts.map((pod) => (
                  <tr key={pod.id}>
                    <td>{new Date(pod.date).toLocaleString()}</td>
                    <td>{formatSeconds(pod.duration)}</td>
                    <td>{pod.generated_percentage}</td>
                    <td>{pod.familiarity}</td>
                    <>
                      <select id="dropdown" value={pod.listened} onChange={(event) => handleListenedChange(event, pod.id)}>
                          <option value="">-- Choose an option --</option>
                          <option value="0">0</option>
                          <option value="1">1</option>
                          <option value="2">2</option>
                          <option value="3">3</option>
                      </select>
                    </>
                    <td>
                      <button onClick={() => handleDelete(pod.id)}>delete</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
            <div style={{ border: '1px solid #000', padding: '10px', marginTop: '10px' }}>
              Total Duration: {totalDur}
            </div>
          </>
        ) : (
          <p>No podcasts found.</p>
        )}
      </div>
    );
  };
  
  export default PodcastHistoryTable;
