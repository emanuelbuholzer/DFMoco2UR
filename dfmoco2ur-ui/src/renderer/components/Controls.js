import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';
import Button from '@material-ui/core/Button';
import ButtonGroup from '@material-ui/core/ButtonGroup';
import { connect } from 'react-redux';
import { socketMessageEnableFreedrive, socketMessageUnlock, savePosition, goToPosition, deletePosition } from '../services/socket/actions';

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
}));

function Controls({ freedriveEnabled, recentlyUnlocked, socketMessageEnableFreedrive, socketMessageUnlock, savePosition, goToPosition, deletePosition }) {
    const classes = useStyles();
    console.log("Freedrive: " + freedriveEnabled);
    console.log("Recently Unlocked: " + recentlyUnlocked)
    return (
        <div>
            <div className={classes.buttonGroopRoot}>
                <ButtonGroup variant="contained" color="primary" fullWidth={true}>
                
                    <Button onClick={savePosition}>Save</Button>
                    <Button onClick={goToPosition}>Goto</Button>
                    <Button onClick={deletePosition}>Delete</Button>
                    <Button color="secondary" onClick={socketMessageEnableFreedrive}>Freedrive</Button>
                    <Button color="secondary" onClick={socketMessageUnlock}>Unlock</Button>
                </ButtonGroup>
            </div>
            <div className={classes.root}>
                <List>
                    <ListItem button>
                        <ListItemText primary="Position1" />
                    </ListItem>
                    <ListItem button>
                        <ListItemText primary="Position 3" />
                    </ListItem>
                </List>
            </div>
        </div>
    );
}

const mapStateToProps = (state) => {
    return {
      freedriveEnabled: state.socket.freedrive.enabled,
      recentlyUnlocked: state.socket.recentlyUnlocked,
      updatedPosition: state.socket.List
    }
}

const mapDispatchToProps = { socketMessageEnableFreedrive, socketMessageUnlock, savePosition, goToPosition, deletePosition }

export default connect(mapStateToProps, mapDispatchToProps)(Controls);