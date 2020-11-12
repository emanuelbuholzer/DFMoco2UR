import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';
import FormGroup from '@material-ui/core/FormGroup';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Chip from '@material-ui/core/Chip';
import Grid from '@material-ui/core/Grid';
import Typography from '@material-ui/core/Typography';

const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
    maxWidth: 752,
  },
  demo: {
    backgroundColor: theme.palette.background.paper,
  },
  title: {
    margin: theme.spacing(4, 0, 2),
  },
}));

function generate(element) {
  return [0, 1, 2].map((value) =>
    React.cloneElement(element, {
      key: value,
    }),
  );
}

export default function LoggerFilter() {
  const classes = useStyles();
  const [activeFilters, setActiveFilter] = React.useState({critical: true, Error: true, Warning: true, Info: false, Debug: false});
  const [secondary, setSecondary] = React.useState(false);

  return (
    <div className={classes.root}>
      <FormGroup row>
        <FormControlLabel
          control={
            <Chip size="small" label="Basic" />          }
          label="Critical"
        />
        <FormControlLabel
          control={
            <Chip size="small" label="Basic" />
          }
          label="Error"
        />
        <FormControlLabel
          control={
            <Chip size="small" label="Basic" />
          }
          label="Warning"
        />
        <FormControlLabel
          control={
            <Chip size="small" label="Basic" />

          }
          label="Info"
        />
        <FormControlLabel
          control={
            <Chip size="small" label="Basic" />

          }
          label="Debug"
        />
      </FormGroup>
    
    </div>
  );
}
