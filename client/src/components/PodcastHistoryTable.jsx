import React, { useEffect, useState } from 'react';

import { getPodcastList, removePodcastEntry, updateListenedStatus } from '../api';

export function PodcastHistoryTable() {
    const [change, setChange] = useState(0);
    const [podcasts, setPodcasts] = useState(null);
  
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
  
    return (
      <div>
        <h3>List of Generated Podcasts</h3>
        {podcasts && podcasts.length > 0 ? (
          <table>
            <thead>
              <tr>
                <th>Date</th>
                <th>Duration</th>
                <th>Generated Percentage</th>
                <th>Familiarity</th>
                <th>Listened</th>
                <th>Delete</th>
              </tr>
            </thead>
            <tbody>
              {podcasts.map((pod) => (
                <tr key={pod.id}>
                  <td>{pod.date}</td>
                  <td>{pod.duration}</td>
                  <td>{pod.generated_percentage}</td>
                  <td>{pod.familiarity}</td>
                  <>
                    <select id="dropdown" value={pod.listened} onChange={(event) => handleListenedChange(event, pod.id)}>
                        <option value="">-- Choose an option --</option>
                        <option value="0">No</option>
                        <option value="1">Yes</option>
                    </select>
                  </>
                  <td>
                    <button onClick={() => handleDelete(pod.id)}>delete</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <p>No podcasts found.</p>
        )}
      </div>
    );
  };
  
  export default PodcastHistoryTable;
