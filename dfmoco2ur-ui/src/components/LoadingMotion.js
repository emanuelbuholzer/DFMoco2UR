import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import { motion } from "framer-motion";

const useStyles = makeStyles((theme) => ({
  motion: {
    height: theme.spacing(1),
    width: theme.spacing(1),
    borderRadius: "3px",
    background: theme.palette.secondary.main,
    float: "right",
    marginTop: theme.spacing(2),
  },
}));

export default function LoadingMotion({ isActive }) {
  const classes = useStyles();
  if (isActive) {
    return (
      <motion.div
        className={classes.motion}
        initial={{ scale: 0 }}
        animate={{ rotate: 360, scale: 1 }}
        transition={{
          ease: "circOut",
          duration: 1,
          loop: Infinity,
        }}
      ></motion.div>
    );
  } else {
    return <div></div>;
  }
}
