import React from 'react';
import Container from '@material-ui/core/Container';
import { Typography } from '@material-ui/core';
import ControlGrid from './ControlGrid';
import { Link } from "react-router-dom";


export default function ControlPage() {
    // TODO: Put button in the top right corner, red?
    return (
        <Container>
            <Typography variant="h3">
                Control
            </Typography>
            <Typography>
                For more information on how about to use hue, refer to the <Link to="/manual">hue manual</Link>.
            </Typography>
            <ControlGrid></ControlGrid>
        </Container>
    );
}