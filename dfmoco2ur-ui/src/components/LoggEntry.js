
import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import Paper from "@material-ui/core/Paper";
import Grid from "@material-ui/core/Grid";
import Container from "@material-ui/core/Container";
import ControlCanvas from "./ControlCanvas";
import Button from '@material-ui/core/Button';
import LoggView from './LoggView';

const useStyles = makeStyles((theme) => ({
    paper: {
      padding: "6px 16px",
    },
    secondaryTail: {
      backgroundColor: theme.palette.secondary.main,
    },
  }));

  export default function ControlGrid() {
    const classes = useStyles();
  
    return (
      <div className={classes.root}>
          <div level="X" timestamp="xxx" message="adaaaa">tüdelüüüü</div>
      </div>
    );
  }