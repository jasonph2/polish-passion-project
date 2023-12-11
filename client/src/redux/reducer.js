// someReducer.js
const initialState = {
    toChange: 1,
    audioFiles: [],
  };
  
  const reducer = (state = initialState, action) => {
    switch (action.type) {
      case 'SET_TO_CHANGE':
        return {
          ...state,
          toChange: action.payload,
        };
      case 'SET_AUDIO_FILES':
        return {
          ...state,
          audioFiles: action.payload,
        };
      default:
        return state;
    }
  };
  
  export const setToChange = (payload) => {
    return {
      type: 'SET_TO_CHANGE',
      payload,
    };
  };
  
  export const setAudioFiles = (payload) => {
    return {
      type: 'SET_AUDIO_FILES',
      payload,
    };
  }
  export default reducer;
  