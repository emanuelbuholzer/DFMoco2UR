import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import Paper from "@material-ui/core/Paper";
import Grid from "@material-ui/core/Grid";
import PositionSelection from "./PositionSelection";
import LogView from './LogView';


const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
    marginTop: theme.spacing(5),
  },
  paper: {
    padding: theme.spacing(2),
    textAlign: "center",
    color: theme.palette.text.secondary,
  },
  canvas: {
    padding: theme.spacing(2),
    textAlign: "center",
    color: theme.palette.text.secondary,
    height: "50vh",
  },
  canvasSide: {
    padding: theme.spacing(2),
    height: "50vh",
  },
  bottomSide: {
    padding: theme.spacing(2),
    minHeight: "10vh",
  },
}));

export default function ControlGrid() {
  const classes = useStyles();

  return (
    <div className={classes.root}>
      <Grid container justify="space-around" alignItems="stretch" spacing={3}>
        <Grid item xs={12}>
          <LogView></LogView>
        </Grid>
        <Grid item xs={12}>
          <Paper>
            <PositionSelection></PositionSelection>
          </Paper>
        </Grid>
        
      </Grid>
    </div>
  );
}
