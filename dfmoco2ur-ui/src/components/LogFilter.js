import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import FormGroup from '@material-ui/core/FormGroup';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Chip from '@material-ui/core/Chip';

const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
    maxWidth: 752,
  },
  
}));

function generate(element) {
  return [0, 1, 2].map((value) =>
    React.cloneElement(element, {
      key: value,
    }), 
  );
}

export default function LogFilter() {
  const classes = useStyles();
 // prolly need state to know if have to turn on off  --> doesnt work -->  state= {selected, deselected}     

  // What to put as default? all selected? --> check
  const handleToggle = () => {
    console.info("here we wanna selected/deselect the severity")
    // TODO: actual filtering and coloring red green would be nice. 
  }


  return (
    <div className={classes.root}>
      <FormGroup row>
        <FormControlLabel
          control={
            <Chip size="medium" label="Critical" onClick={handleToggle }/>
          }
        />
        <FormControlLabel
          control={
            <Chip size="medium" label="Error" onClick={handleToggle }/>
          }
        />
        <FormControlLabel
          control={
            <Chip size="medium" label="Warning" onClick={handleToggle }/>
          }
        />
        <FormControlLabel
          control={
            <Chip size="medium" label="Info" onClick={handleToggle }/>
          }
        />
        <FormControlLabel
          control={
            <Chip size="medium" label="Debug" onClick={handleToggle }/>
          }
        />
      </FormGroup>   
    </div>
  );
}
