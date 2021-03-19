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

export function socketMessageEnableSaveDialog() {
  return {
    type: 'SOCKET_MESSAGE_SAVE_REQUEST_ENABLE_DIALOG'

  }
}

export function socketMessageSavePosition(posName) {
  return {
    type: 'SOCKET_MESSAGE_SAVE_REQUEST',
    payload: {
      positionName: posName
    }
  }
}


export function socketMessageUnlock() {
  return {
    type: 'SOCKET_MESSAGE_UNLOCK_REQUEST'
  }
}

export function resetRecentUnlockInView() {
  return {
    type: 'RESET_RECENT_UNLOCK'
  }
}

export function selectPosition(positionName){
  return{
    type: 'SELECT_POSITION',
    payload: {
      positionName: positionName
    }
  }
}

export function loadPositions(){
  return {
    type:'LOAD_POSITION_REQUEST', 
    
  }
}

export function deletePosition(positionName) {
  return {
    type: 'DELETE_POSITION_REQUEST',
    payload: {
      positionName: positionName
    }
  }
}

export function goToPosition(selectedPositionName){
  return{
    type: 'GOTO_POSITION_REQUEST',
    payload:{
      positionName: selectedPositionName
    }
  }
}