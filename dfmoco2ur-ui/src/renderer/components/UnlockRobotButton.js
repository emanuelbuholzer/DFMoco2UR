import React from 'react';
import Button from '@material-ui/core/Button';
import Snackbar from '@material-ui/core/Snackbar';
import MuiAlert from '@material-ui/lab/Alert';
import { makeStyles } from '@material-ui/core/styles';
import { socketMessageUnlock, resetRecentUnlockInView } from '../services/socket/actions';
import { connect } from 'react-redux';

function Alert(props) {
  return <MuiAlert elevation={6} variant="filled" {...props} />;
}

const useStyles = makeStyles(() => ({
    button: {
        borderRadius: 0,
        boxShadow: 'none'
    }
}));

function UnlockRobotButton({ recentlyUnlocked, socketMessageUnlock, resetRecentUnlockInView}) {
  const classes = useStyles();

  return (
    <span>
      <Button color="secondary" variant="contained" className={classes.button} fullWidth={true} onClick={socketMessageUnlock}>Unlock</Button>
      <Snackbar open={recentlyUnlocked} autoHideDuration={6000}>
        <Alert onClose={resetRecentUnlockInView} severity="success">
          Robot unlocked!
        </Alert>
      </Snackbar>
    </span>
  );
}


const mapStateToProps = (state) => {
  return {
    recentlyUnlocked: state.socket.recentlyUnlocked,
  }
}

const mapDispatchToProps = { socketMessageUnlock, resetRecentUnlockInView  }

export default connect(mapStateToProps, mapDispatchToProps)(UnlockRobotButton);