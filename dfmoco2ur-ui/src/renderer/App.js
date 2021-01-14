import React from "react";
import "./App.css";
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Redirect,
} from "react-router-dom";
import { connect } from 'react-redux';
import {initializeSocket} from './services/socket/actions';

import CssBaseline from "@material-ui/core/CssBaseline";
import DenseAppBar from "./components/DenseAppBar";
import StartupPage from "./components/StartupPage";
import ControlPage from "./components/ControlPage";
import ManualPage from "./components/ManualPage";

class App extends React.Component {
  componentWillMount() {
    const { dispatch } = this.props;
    
    dispatch(initializeSocket());
  }

  render() {
    return (
      <React.Fragment>
        <CssBaseline></CssBaseline>
        <Router>
          <DenseAppBar></DenseAppBar>
          <Switch>
            <Route path="/startup">
              <StartupPage></StartupPage>
            </Route>
            <Route path="/control">
              <ControlPage></ControlPage>
            </Route>
            <Route path="/manual">
              <ManualPage></ManualPage>
            </Route>
            <Route path="/shutdown">
              <p>Shutdown</p>
            </Route>

            <Route path="/">
              <Redirect to="/startup"></Redirect>
            </Route>
          </Switch>
        </Router>
      </React.Fragment>
    );
  }
}

function mapStateToProps(state) {
  return {
    socket: state.socket,
  };
}

export default connect(mapStateToProps)(App);