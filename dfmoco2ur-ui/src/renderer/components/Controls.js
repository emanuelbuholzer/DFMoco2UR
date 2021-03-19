import React, { useState } from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Button from '@material-ui/core/Button';
import ButtonGroup from '@material-ui/core/ButtonGroup';
import PositionList from './PositionList';
import Snackbar from '@material-ui/core/Snackbar';
import MuiAlert from '@material-ui/lab/Alert';
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import DialogTitle from '@material-ui/core/DialogTitle';
import { socketMessageEnableSaveDialog, socketMessageSavePosition, goToPosition, deletePosition, socketMessageEnableFreedrive, socketMessageDisableFreedrive, socketMessageUnlock, resetRecentUnlockInView } from '../services/socket/actions';
import { connect } from 'react-redux'

function Alert(props) {
    return <MuiAlert elevation={6} variant="filled" {...props} />;
}

const useStyles = makeStyles((theme) => ({
    root: {
        width: '100%',
        maxWidth: 360,
        backgroundColor: theme.palette.background.paper,
    },
    buttonGroupRoot: {
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        '& > *': {
            margin: theme.spacing(1),
        },
    },
    button: {
        borderRadius: 0,
        boxShadow: 'none'
    }
}));

function Controls({ saveEnabled, socketMessageSavePosition, socketMessageEnableSaveDialog, selectedPositionName, goToPosition, deletePosition, freedriveEnabled, freedriveTimeout, socketMessageEnableFreedrive, socketMessageDisableFreedrive, recentlyUnlocked, socketMessageUnlock, resetRecentUnlockInView }) {
    const classes = useStyles();
    const [positionName, setPositionName] = useState('savePositionName')
    return (
        <div>
            <div className={classes.buttonGroopRoot}>
                <ButtonGroup variant="contained" color="primary" fullWidth={true}>
                    <Button variant="contained" color="primary" className={classes.button} onClick={socketMessageEnableSaveDialog}>Save</Button>
                    <Dialog open={saveEnabled} aria-labelledby="alert-dialog-title" aria-describedby="alert-dialog-description">
                        <DialogTitle id="alert-dialog-title">{"Select a Name:"}</DialogTitle>
                        <DialogContent>
                            <DialogContentText id="alert-dialog-description">
                                <label>
                                    <input type="text" placeholder="Position Name" value={positionName} onChange={(e) => setPositionName(e.target.value)}></input>
                                </label>
                                <Button type="submit" color="primary" onClick={() => socketMessageSavePosition(positionName)}>Save</Button>
                            </DialogContentText>
                        </DialogContent>
                    </Dialog>

                    <Button className={classes.button} onClick={() => goToPosition(selectedPositionName)}>GoTo</Button>

                    <Button className={classes.button} onClick={() => deletePosition(selectedPositionName)}>Delete</Button>

                    <Button variant="contained" color="secondary" className={classes.button} onClick={socketMessageEnableFreedrive}>
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
                    <Button color="secondary" variant="contained" className={classes.button} fullWidth={true} onClick={socketMessageUnlock}>Unlock</Button>
                    <Snackbar open={recentlyUnlocked} autoHideDuration={6000}>
                        <Alert onClose={resetRecentUnlockInView} severity="success">
                            Robot unlocked!
                        </Alert>
                    </Snackbar>

                </ButtonGroup>
            </div>
            <PositionList></PositionList>
        </div>
    );
}

const mapStateToProps = (state) => {

    return {
        saveEnabled: state.socket.saveEnabled,
        positionName: state.socket.positionName,
        selectedPositionName: state.socket.selectedPositionName,
        freedriveEnabled: state.socket.freedrive.enabled,
        freedriveTimeout: state.socket.freedrive.timeout,
        recentlyUnlocked: state.socket.recentlyUnlocked
    }
}

const mapDispatchToProps = { socketMessageEnableSaveDialog, socketMessageSavePosition, goToPosition, deletePosition, socketMessageEnableFreedrive, socketMessageDisableFreedrive, socketMessageUnlock, resetRecentUnlockInView }

export default connect(mapStateToProps, mapDispatchToProps)(Controls);