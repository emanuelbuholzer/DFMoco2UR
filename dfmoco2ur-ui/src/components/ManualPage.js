import React from 'react';
import Container from '@material-ui/core/Container';
import CustomizedTimeline from './CustomizedTimeline';
import { Typography } from '@material-ui/core';
import VerticalLinearStepper from './VerticalLineStepper';
import ManualPageContent from './ManualPageContent'

export default function StartupPage() {
    return (
        <Container>
            <Typography variant="h3">
                Manual
            </Typography>
            <ManualPageContent path="/test.md"></ManualPageContent>
        </Container>
    );
}