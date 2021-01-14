import React from 'react';
import Container from '@material-ui/core/Container';
import { Typography } from '@material-ui/core';
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