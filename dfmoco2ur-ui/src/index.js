import React from 'react';
import ReactDOM from 'react-dom';
import "fontsource-roboto"
import './renderer/index.css';
import App from './renderer/App';
import { Provider } from 'react-redux';
import store from './renderer/store';

ReactDOM.render(
  <Provider store={store}>
    <App />
  </Provider>
  , document.getElementById('root')
);