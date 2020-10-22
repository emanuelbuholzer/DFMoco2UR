import React from "react";
import "./App.css";
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Redirect,
} from "react-router-dom";

import CssBaseline from "@material-ui/core/CssBaseline";
import DenseAppBar from "./components/DenseAppBar";
import StartupPage from "./components/StartupPage";
import ControlPage from "./components/ControlPage";
import ManualPage from "./components/ManualPage"

function App() {
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

export default App;
