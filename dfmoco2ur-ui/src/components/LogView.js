import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import LogFilter from './LogFilter';
import DataTable from './DataTable';




const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
    marginTop: theme.spacing(5),
  }}));

  export default function Logview(){
    const classes = useStyles();

    return (
      <div classname = {classes.root}>
          <LogFilter></LogFilter>
          <DataTable></DataTable>
      </div>
    );
  }





