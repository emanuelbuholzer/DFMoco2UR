import moment from 'moment';
import { SOCKET_CONNECTION_CLOSED, SOCKET_CONNECTION_ERROR, SOCKET_CONNECTION_INIT, SOCKET_CONNECTION_SUCCESS} from './actions'

const initialState = {
    connected: false,
    socket: null,
    logs: [],
    freedrive: {
      enabled: false,
      timeout: null, 
    },
    recentlyUnlocked: false,
    save: {
      enabled: false, 
      posName: null, 
    }
  };

export default function reducer(state = initialState, action = {}) {
    switch (action.type) {
      case "SOCKET_MESSAGE_LOG":
        const log = {
          time: moment.unix(action.payload.timestamp).toDate(),
          severity: action.payload.severity,
          message: action.payload.message
        }

        // We love material-ui DataGrid, as it does not always update on row changes :*
        let pageSize = state.pageSize === 100 ? 99 : 100;

        return Object.assign({}, state, {
          logs: state.logs.concat(log)
                          .map((e,i) => Object.assign({id: i}, e)),
          pageSize: pageSize
        })
      
      case "SOCKET_MESSAGE_FREEDRIVE_REQUEST_ENABLE": 
        state.socket.send(JSON.stringify({type: "SOCKET_MESSAGE_FREEDRIVE_REQUEST_ENABLE"}));
        return state;

      case "SOCKET_MESSAGE_FREEDRIVE_RESPONSE_ENABLE": 
        return Object.assign({}, state, {
          freedrive: {
            enabled: true,
            timeout: action.payload.timeout
          }
        });

      case "SOCKET_MESSAGE_FREEDRIVE_REQUEST_DISABLE": 
        state.socket.send(JSON.stringify({type: "SOCKET_MESSAGE_FREEDRIVE_REQUEST_DISABLE"}));
        return state;

      case "SOCKET_MESSAGE_FREEDRIVE_RESPONSE_DISABLE": 
        return Object.assign({}, state, {
          freedrive: {
            enabled: false,
            timeout: null
          }
        });

        case "SOCKET_MESSAGE_SAVE_REQUEST_ENABLE": 
        state.socket.send(JSON.stringify({type: "SOCKET_MESSAGE_SAVE_REQUEST_ENABLE"}));
        return state;

      case "SOCKET_MESSAGE_SAVE_RESPONSE_ENABLE": 
        return Object.assign({}, state, {
          save: {
            enabled: true,
          }
        });

      case "SOCKET_MESSAGE_SAVE_REQUEST_DISABLE": 
        state.socket.send(JSON.stringify({type: "SOCKET_MESSAGE_SAVE_REQUEST_DISABLE"}));
        return state;

      case "SOCKET_MESSAGE_SAVE_RESPONSE_DISABLE": 
        return Object.assign({}, state, {
          save: {
            enabled: false,
            posName: null,
          }
        });
      
      case "SOCKET_MESSAGE_UNLOCK_REQUEST":
        state.socket.send(JSON.stringify({type: "SOCKET_MESSAGE_UNLOCK_REQUEST"}));
        return state;

      case "SOCKET_MESSAGE_UNLOCK_RESPONSE":
        return Object.assign({}, state, {
          recentlyUnlocked: true,
        });
      
      case "RESET_RECENT_UNLOCK":
        return Object.assign({}, state, {
          recentlyUnlocked: false,
        });

      case SOCKET_CONNECTION_INIT:
        return Object.assign({}, state, {
          connected: false,
          socket: action.socket,
        });
  
      case SOCKET_CONNECTION_SUCCESS:
        return Object.assign({}, state, {
          connected: true,
        });
  
      case SOCKET_CONNECTION_ERROR:
        return Object.assign({}, state, {
          connected: false,
        });
  
      case SOCKET_CONNECTION_CLOSED:
        return Object.assign({}, state, {
          connected: false,
          socket: null,
        });
  
      default:
        return state;
    }
  }