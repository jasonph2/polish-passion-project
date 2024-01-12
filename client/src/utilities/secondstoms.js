export function formatSeconds(dur) {
    const seconds = Math.round(parseFloat(dur));
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const remainingSeconds = seconds % 60;
  
    let formattedDuration = '';
  
    if (hours > 0) {
      formattedDuration += `${hours}h `;
    }
  
    if (minutes > 0 || hours > 0) {
      const formattedMinutes = minutes < 10 ? `0${minutes}` : minutes;
      formattedDuration += `${formattedMinutes}m `;
    }
  
    const formattedSeconds = remainingSeconds < 10 ? `0${remainingSeconds}` : remainingSeconds;
    formattedDuration += `${formattedSeconds}s`;
  
    return formattedDuration;
  }
  