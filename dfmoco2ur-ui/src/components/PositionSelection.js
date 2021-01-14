import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';
import Button from '@material-ui/core/Button';
import ButtonGroup from '@material-ui/core/ButtonGroup';

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

export default function SimpleList() {
    const classes = useStyles();

    return (
        <div>
            <div className={classes.buttonGroopRoot}>
                <ButtonGroup variant="contained" color="primary" fullWidth={true}>
                    <Button>Save</Button>
                    <Button>Goto</Button>
                    <Button>Delete</Button>
                    <Button color="secondary">Freedrive</Button>
                    <Button color="secondary">Unlock</Button>
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