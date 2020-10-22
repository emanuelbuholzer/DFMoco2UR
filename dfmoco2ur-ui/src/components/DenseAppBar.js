import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import AppBar from "@material-ui/core/AppBar";
import Toolbar from "@material-ui/core/Toolbar";
import Typography from "@material-ui/core/Typography";
import HueIcon from "./HueIcon";
import { Link } from "react-router-dom";

const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
    marginBottom: theme.spacing(5),
  },
  logo: {
    marginRight: theme.spacing(2),
  },
}));

export default function DenseAppBar() {
  const classes = useStyles();

  return (
    <div className={classes.root} id="AppBar">
      <AppBar position="static">
        <Toolbar variant="dense">
          <Link to="/">
            <HueIcon
              edge="start"
              className={classes.logo}
              color="secondary"
              aria-label="logo"
            ></HueIcon>
          </Link>
        </Toolbar>
      </AppBar>
    </div>
  );
}
