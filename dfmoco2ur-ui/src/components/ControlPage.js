import React from 'react';
import Container from '@material-ui/core/Container';
import { Typography } from '@material-ui/core';
import ControlGrid from './ControlGrid';
import { Link } from "react-router-dom";
import { makeStyles } from '@material-ui/core/styles';

const useStyles = makeStyles((theme) => ({
    info: {
        float: 'left',
        marginTop: '8px'
    },
    shutdown: {
        float: 'right'
    },
  }));

export default function ControlPage() {
    const classes = useStyles();

    return (
        <Container>
            <Typography variant="h4">
                Control
            </Typography>
            <Typography className={classes.info}>
                For more information on how about to use hue, refer to the <Link to="/manual">hue manual</Link>.
            </Typography>
            {/*<Button color="secondary" variant="contained" className={classes.shutdown}>SHUTDOWN</Button>*/}
            <ControlGrid></ControlGrid>
        </Container>
    );
}