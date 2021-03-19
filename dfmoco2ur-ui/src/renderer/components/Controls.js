import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';
import Button from '@material-ui/core/Button';
import ButtonGroup from '@material-ui/core/ButtonGroup';
import UnlockRobot from './UnlockRobotButton'
import FreedriveDialog from './FreedriveDialogButton';
import SavePosition from './SavePosition';
import PositionList from './PositionList';
import DeleteButton from './DeleteButton';
import GoToButton from './GoToButton';

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

export default function Controls() {
    const classes = useStyles();

    return (
        <div>
            <div className={classes.buttonGroopRoot}>
                <ButtonGroup variant="contained" color="primary" fullWidth={true}>
                    <SavePosition></SavePosition>
                    <GoToButton></GoToButton>
                    <DeleteButton></DeleteButton>
                    <FreedriveDialog></FreedriveDialog>
                    <UnlockRobot></UnlockRobot>

                </ButtonGroup>
            </div>
            <PositionList></PositionList>
        </div>
    );
}