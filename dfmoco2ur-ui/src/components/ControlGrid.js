import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import Paper from "@material-ui/core/Paper";
import Grid from "@material-ui/core/Grid";
import Container from "@material-ui/core/Container";
import ControlCanvas from "./ControlCanvas";
import Button from '@material-ui/core/Button';
import LoggView from './LogView';

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
        <Grid item xs={3}>
          <Container className={classes.canvasSide}>
            left
          </Container>
        </Grid>
        <Grid item xs={6}>
          <Paper className={classes.canvas}>
            <ControlCanvas></ControlCanvas>
          </Paper>
        </Grid>
        <Grid item xs={3}>
          <Container className={classes.canvasSide}>
            <Button variant="contained" size="large">
              
            </Button>
          </Container>
        </Grid>
        <Grid item xs={3}>
          <Container className={classes.bottomSide}>left</Container>
        </Grid>
        <Grid item xs={6}>
          <Container className={classes.bottomSide}>Logger
            <LoggView></LoggView>
          </Container>
        </Grid>
 
        <Grid item xs={3}>
          <Container className={classes.bottomSide}>left</Container>
        </Grid>
      </Grid>
    </div>
  );
}
