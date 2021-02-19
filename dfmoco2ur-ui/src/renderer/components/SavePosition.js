import React, { useState } from 'react';
import Button from '@material-ui/core/Button';
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import DialogTitle from '@material-ui/core/DialogTitle';
import { socketMessageEnableSave, socketMessageDisableSave } from '../services/socket/actions';
import { makeStyles } from '@material-ui/core/styles';
import { connect } from 'react-redux';

const useStyles = makeStyles(() => ({
    button: {
        borderRadius: 0,
        boxShadow: 'none'
    }
}));

function SaveDialogButton({ saveEnabled, posName, socketMessageEnableSave, socketMessageDisableSave}) {
  const classes = useStyles();

  return (
    <span>
      <Button variant="contained" color="Primary"  className={classes.button} onClick={socketMessageEnableSave}>
        Save
      </Button>
      <Dialog
        open={saveEnabled}
        aria-labelledby="alert-dialog-title"
        aria-describedby="alert-dialog-description"
      >
        <DialogTitle id="alert-dialog-title">{"Choose a name to save"}</DialogTitle>
        <DialogContent>
          <DialogContentText id="alert-dialog-description">
              <form>
                  <label>
                    <input type="text" onChange={e => set({posName: e.target.value})}></input> 
                  </label>
                    
              </form>
               
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={socketMessageDisableSave} color="primary">
            Save
          </Button>
        </DialogActions>
      </Dialog>
    </span>
  );
}

const mapStateToProps = (state) => {
  return {
    saveEnabled: state.socket.save.enabled,
    saveMessage: state.socket.save.posName
  }
}

const mapDispatchToProps = { socketMessageEnableSave, socketMessageDisableSave }

export default connect(mapStateToProps, mapDispatchToProps)(SaveDialogButton);