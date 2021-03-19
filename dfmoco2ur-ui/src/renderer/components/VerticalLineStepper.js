import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import Stepper from "@material-ui/core/Stepper";
import Step from "@material-ui/core/Step";
import StepLabel from "@material-ui/core/StepLabel";
import StepContent from "@material-ui/core/StepContent";
import Button from "@material-ui/core/Button";
import Paper from "@material-ui/core/Paper";
import Typography from "@material-ui/core/Typography";
import LoadingMotion from "./LoadingMotion";
import { Link } from "react-router-dom";

const useStyles = makeStyles((theme) => ({
  root: {
    width: "100%",
    marginTop: theme.spacing(3),
  },
  stepper: {
    backgroundColor: "inherit",
  },
  button: {
    marginTop: theme.spacing(1),
    marginRight: theme.spacing(1),
  },
  link: {
    textDecoration: "none",
  },
  actionsContainer: {
    marginBottom: theme.spacing(2),
  },
  resetContainer: {
    padding: theme.spacing(3),
  },
}));

function getSteps() {
  return ["Ensure the Universal Robot is started", "Connect DragonFrame"];
}

function getStepContent(step) {
  switch (step) {
    case 0:
      return (
        <Typography>
          Ensure the Universal Robot is up and running, such that the robot is in normal mode.
        </Typography>
      );
    case 1:
      return (
        <Typography>
          Connect the DFMoco2UR bridge in DragonFrame.
          You can connect the bridge under: Scenes, Connections.
          You'll need to use the DFMoco Protocol / TCP on ArcMoco #1.
          The DFMoco2UR bridge is avaialable under 127.0.0.1:10001.
        </Typography>
      );
    default:
      return <Typography>Unknown step</Typography>;
  }
}

export default function VerticalLinearStepper() {
  const classes = useStyles();
  const [activeStep, setActiveStep] = React.useState(0);
  const steps = getSteps();

  const handleNext = () => {
    setActiveStep((prevActiveStep) => prevActiveStep + 1);
  };

  const handleBack = () => {
    setActiveStep((prevActiveStep) => prevActiveStep - 1);
  };

  const handleReset = () => {
    setActiveStep(0);
  };

  return (
    <div className={classes.root}>
      <Stepper
        activeStep={activeStep}
        orientation="vertical"
        className={classes.stepper}
      >
        {steps.map((label, index) => (
          <Step key={label}>
            <StepLabel>
              {label}
              <LoadingMotion isActive={activeStep === index}></LoadingMotion>
            </StepLabel>
            <StepContent>
              {getStepContent(index)}
              <div className={classes.actionsContainer}>
                <div>
                  <Button
                    disabled={activeStep === 0}
                    onClick={handleBack}
                    className={classes.button}
                  >
                    Back
                  </Button>
                  <Button
                    variant="contained"
                    color="primary"
                    onClick={handleNext}
                    className={classes.button}
                  >
                    {activeStep === steps.length - 1 ? "Finish" : "Next"}
                  </Button>
                </div>
              </div>
            </StepContent>
          </Step>
        ))}
      </Stepper>
      {activeStep === steps.length && (
        <Paper square elevation={0} className={classes.resetContainer}>
          <Typography>
            All steps completed - you&apos;re ready to animate!
          </Typography>
          <Link to="/control" className={classes.link}>
            <Button
              variant="contained"
              onClick={handleReset}
              className={classes.button}
            >
              Go to Control
            </Button>
          </Link>
        </Paper>
      )}
    </div>
  );
}
