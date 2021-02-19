import React from 'react';
import Button from '@material-ui/core/Button';
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import DialogTitle from '@material-ui/core/DialogTitle';
import { socketMessageEnableFreedrive, socketMessageDisableFreedrive } from '../services/socket/actions';
import { makeStyles } from '@material-ui/core/styles';
import { connect } from 'react-redux';

const useStyles = makeStyles(() => ({
    button: {
        borderRadius: 0,
        boxShadow: 'none'
    }
}));

function FreedriveDialogButton({ freedriveEnabled, freedriveTimeout, socketMessageEnableFreedrive, socketMessageDisableFreedrive}) {
  const classes = useStyles();

  return (
    <span>
      <Button variant="contained" color="secondary"  className={classes.button} onClick={socketMessageEnableFreedrive}>
        FREEDRIVE
      </Button>
      <Dialog
        open={freedriveEnabled}
        aria-labelledby="alert-dialog-title"
        aria-describedby="alert-dialog-description"
      >
        <DialogTitle id="alert-dialog-title">{"Freedrive"}</DialogTitle>
        <DialogContent>
          <DialogContentText id="alert-dialog-description">
            Freedrive is running now for {freedriveTimeout} seconds or until you disable the freedrive manually.
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={socketMessageDisableFreedrive} color="primary">
            Disable
          </Button>
        </DialogActions>
      </Dialog>
    </span>
  );
}

const mapStateToProps = (state) => {
  return {
    freedriveEnabled: state.socket.freedrive.enabled,
    freedriveTimeout: state.socket.freedrive.timeout
  }
}

const mapDispatchToProps = { socketMessageEnableFreedrive, socketMessageDisableFreedrive }

export default connect(mapStateToProps, mapDispatchToProps)(FreedriveDialogButton);