import React, { useState } from 'react';
import Button from '@material-ui/core/Button';
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import DialogTitle from '@material-ui/core/DialogTitle';
import { socketMessageEnableSaveDialog, socketMessageSavePosition } from '../services/socket/actions';
import { makeStyles } from '@material-ui/core/styles';
import { connect } from 'react-redux';

const useStyles = makeStyles(() => ({
  button: {
    borderRadius: 0,
    boxShadow: 'none'
  }
}));

function SaveDialogButton({ saveEnabled, socketMessageSavePosition, socketMessageEnableSaveDialog }) {
  const classes = useStyles();
  const [positionName, setPositionName]= useState('')

  return (
    <span>
      <Button variant="contained" color="Primary" className={classes.button} onClick={socketMessageEnableSaveDialog}>
        Save
      </Button>

      <Dialog
        open={saveEnabled}  
        aria-labelledby="alert-dialog-title"
        aria-describedby="alert-dialog-description"
      >
        <DialogTitle id="alert-dialog-title">{"Select a Name:"}</DialogTitle>
        <DialogContent>
          <DialogContentText id="alert-dialog-description">
              <label>
                <input type="text" placeholder="Position Name" value={positionName} onChange={(e) => setPositionName(e.target.value)}></input>
              </label>
              <Button type="submit" color="primary" onClick={() => socketMessageSavePosition(positionName)}>
                Save
             </Button>
          </DialogContentText>
        </DialogContent>
        <DialogActions>

        </DialogActions>
      </Dialog>
    </span>
  );
}  



const mapStateToProps = (state) => {

  return {  
    saveEnabled: state.socket.saveEnabled,
    positionName: state.socket.positionName,
    
  }
}

const mapDispatchToProps = { socketMessageEnableSaveDialog, socketMessageSavePosition }

export default connect(mapStateToProps, mapDispatchToProps)(SaveDialogButton);