// someReducer.js
const initialState = {
    toChange: 1,
    audioFiles: [],
    ltl: []
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
    case 'SET_LTL':
      return {
        ...state,
        ltl: action.payload,
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

export const setLtl = (payload) => {
  return {
    type: 'SET_LTL',
    payload,
  };
}
export default reducer;
  