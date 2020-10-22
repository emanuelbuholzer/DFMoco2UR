import React from 'react';
import Container from '@material-ui/core/Container';
import CustomizedTimeline from './CustomizedTimeline';
import { Typography } from '@material-ui/core';
import VerticalLinearStepper from './VerticalLineStepper';

export default function StartupPage() {
    return (
        <Container>
            <Typography variant="h3">
                Setup
            </Typography>
            <Typography>
                Welcome to the Dragonframe to Universal Robot bridge (hue).
                Please follow the instructions below in order to connect the Universal Robot with Dragonframe.
            </Typography>
            <VerticalLinearStepper></VerticalLinearStepper>
        </Container>
    );
}