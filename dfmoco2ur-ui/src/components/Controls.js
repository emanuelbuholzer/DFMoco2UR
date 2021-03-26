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
import TextField from '@material-ui/core/TextField'

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
    },
    Button: {
        display: 'flex',
        flexDirection: 'row',
        padding: '10px'

    },
    MuiDialogContentText: {
        padding: '8px',

    },
    p: {
        justifyContent: 'center',
        display: 'flex',
        flexDirection: 'row'

    }

}));

function Controls({ socketMessageSavePosition, selectedPositionName, goToPosition, deletePosition, freedriveEnabled, freedriveTimeout, socketMessageEnableFreedrive, socketMessageDisableFreedrive, recentlyUnlocked, socketMessageUnlock, resetRecentUnlockInView }) {
    const classes = useStyles();
    const [positionName, setPositionName] = useState('')
    const [dialogOpen, setSaveDialogOpen] = useState(false);

    const handleClose = () => {
        setSaveDialogOpen(false);
    };

    const handleOpen = () => {
        setSaveDialogOpen(true);
    };

    return (
        <div>
            <div className={classes.buttonGroopRoot}>
                <ButtonGroup variant="contained" color="primary" fullWidth={true}>
                    <Button variant="contained" color="primary" className={classes.button} onClick={handleOpen}>Save</Button>
                    <Dialog open={dialogOpen} aria-labelledby="alert-dialog-title" aria-describedby="alert-dialog-description">
                        <DialogTitle id="alert-dialog-title">{"Save current position"}</DialogTitle>
                        <DialogContent>
                            <DialogContentText id="alert-dialog-description">
                                <TextField
                                    id="standard-full-width"
                                    label="Name of the current position"
                                    placeholder="Position name"
                                    helperText="Avoid special characters such as %, $ and so on. :-)"
                                    fullWidth
                                    margin="normal"
                                    InputLabelProps={{
                                        shrink: true,
                                    }}
                                    value={positionName} onChange={(e) => setPositionName(e.target.value)}
                                />
                            </DialogContentText>
                        </DialogContent>
                        <DialogActions>
                            <Button type="submit" color="primary" onClick={() => {
                                socketMessageSavePosition(positionName)
                                setPositionName('')
                                handleClose()
                            }}>Save</Button>
                            <Button type="submit" color="secondary" id="cancelButton" onClick={handleClose}>Cancel</Button>
                        </DialogActions>
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
                                Freedrive is running now for a week starting <span>{new Date().toString()}</span> or until you disable the freedrive manually.
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