import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Chip from '@material-ui/core/Chip';
import { DataGrid } from '@material-ui/data-grid';


const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
    marginTop: theme.spacing(5),
    marginBottom: theme.spacing(5),
  }
}));


const columns = [
  { field: 'dateTime', headerName: 'dateTime', type: 'date', width: 150 },
  { field: 'severity', headerName: 'severity', width: 90 },
  { field: 'message',  headerName: 'message', type: 'string', width: 300,  },
  
  /*  // getter method which would be nice, but adds an empty column to the grid, but also no clue tbh
      { valueGetter: (params) =>
      `${params.getValue('dateTime') || ''} 
        ${params.getValue('severity') || ''
      } ${params.getValue('message') || ''}`,
  }, */
];
// data (logs) to be passed to the datatable, but how?..

const data = [
  {id: 1, dateTime:"22.11.2019 14:00" , severity:"Critical" , message: "blabla"},
  {id: 2, dateTime:"22.11.2019 14:00" , severity:"Critical" , message: "blabla"},
  {id: 3, dateTime:"22.11.2019 14:00" , severity:"Critical" , message: "blabla"},
  {id: 4, dateTime:"22.11.2019 14:00" , severity:"Critical" , message: "blabla"}];

  

const handleClick = () => {
   let element = document.getElementById('chip')
    element.style.backgroundColor = 'blue';

  }
  // TODO: actual filtering and coloring red green would be nice. 

  //then filter foor severitys


export default function Logview() {
  const classes = useStyles();



  return (
    <div className={classes.root}>
      <FormControlLabel
        control={
          <Chip id='chip' label="Critical" size="medium"  message="message" onClick={handleClick} />
        }
      />
      <FormControlLabel
        control={
          <Chip size="medium" label="Error" onClick={handleClick} />
        }
      />
      <FormControlLabel
        control={
          <Chip size="medium" label="Warning" onClick={handleClick} />
        }
      />
      <FormControlLabel
        control={
          <Chip size="medium" label="Info" onClick={handleClick} />
        }
      />
      <FormControlLabel
        control={
          <Chip size="medium" label="Debug" onClick={handleClick} />
        }
      />

    <div style={{ height: 400, width: '100%' }}>
      <DataGrid rows={data} columns={columns} pageSize={10} />
    </div>
  );    
  </div>
  );
}





