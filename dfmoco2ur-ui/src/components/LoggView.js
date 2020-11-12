import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import LoggerFilter from './LoggerFilter';
import LoggerMessages from './LoggerMessages';




const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
    marginTop: theme.spacing(5),
  }}));

  export default function Loggview(){
    const classes = useStyles();

    return (
      <div classname = {classes.root}>
          <LoggerFilter></LoggerFilter>
          <LoggerMessages></LoggerMessages>
      </div>
    );
  }





