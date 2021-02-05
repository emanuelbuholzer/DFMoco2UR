export const SOCKET_CONNECTION_INIT = 'SOCKET_CONNECTION_INIT';
export const SOCKET_CONNECTION_SUCCESS = 'SOCKET_CONNECTION_SUCCESS';
export const SOCKET_CONNECTION_ERROR = 'SOCKET_CONNECTION_ERROR';
export const SOCKET_CONNECTION_CLOSED = 'SOCKET_CONNECTION_CLOSED';

export function initializeSocket() {
  return (dispatch) => {
    const socket = new WebSocket('ws://localhost:10002');
    dispatch(socketConnectionInit(socket));

    socket.onopen = function () {
      dispatch(socketConnectionSuccess());
    };

    socket.onerror = function () {
      dispatch(socketConnectionError());
    };

    socket.onmessage = function (event) {
      dispatch(socketMessage(event.data));
    };

    socket.onclose = function () {
      dispatch(socketConnectionClosed());
    };
  };
}

function socketConnectionInit(socket) {
  return {
    type: SOCKET_CONNECTION_INIT,
    socket,
  };
}

function socketConnectionSuccess() {
  return {
    type: SOCKET_CONNECTION_SUCCESS,
  };
}

function socketConnectionError() {
  return {
    type: SOCKET_CONNECTION_ERROR,
  };
}

function socketConnectionClosed() {
  return {
    type: SOCKET_CONNECTION_CLOSED,
  };
}

function socketMessage(data) {
  return JSON.parse(data);
}

export function socketMessageEnableFreedrive() {
  return {
    type: 'SOCKET_MESSAGE_FREEDRIVE_REQUEST_ENABLE'
  }
}

export function socketMessageDisableFreedrive() {
  return {
    type: 'SOCKET_MESSAGE_FREEDRIVE_REQUEST_DISABLE'
  }
}

export function socketMessageUnlock() {
  return {
    type: 'SOCKET_MESSAGE_UNLOCK_REQUEST'
  }
}

export function resetRecentUnlockView() {
  return {
    type: 'RESET_RECENT_UNLOCK'
  }
}

// we need more functions, namely "Safe", "Delete" and "GoTo"

export function savePosition(){
  return {
    type: 'SAVE_POSITION_REQUEST'
    
  }
}

export function goToPosition(){
  return {
    type: 'GO_TO_POSITION_REQUEST'
  }
}

export function deletePosition(){
  return {
    type: 'DELETE_POSITION_REQUEST'
  }
}

export function selectPosition(){
  return{
    type: 'SELECT_POSITION'
  }
} // not sure if needed

