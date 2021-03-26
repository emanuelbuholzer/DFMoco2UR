import { combineReducers } from 'redux';

import socket from './services/socket/reducer';

export default combineReducers({socket: socket})