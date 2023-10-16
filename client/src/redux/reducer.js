// someReducer.js
const initialState = {
    dictionary: {
      key1: 'value1',
      key2: 'value2',
    },
  };
  
  const reducer = (state = initialState, action) => {
    switch (action.type) {
      case 'SET_DICT':
        return {
          ...state,
          dictionary: {
            ...state.dictionary,
            ...action.payload,
          },
        };
      default:
        return state;
    }
  };
  
  export const setDict = (payload) => {
    return {
      type: 'SET_DICT',
      payload,
    };
  };
  
  export default reducer;
  