import React from "react";
import Button from '@material-ui/core/Button';
import {goToPosition} from "../services/socket/actions"
import { connect } from 'react-redux';



function GoToButton({selectedPositionName, goToPosition}) {
    return (
        <Button onClick={() => goToPosition(selectedPositionName)}>GoTo</Button>
    )
}

const mapStateToProps = state => ({selectedPositionName: state.socket.selectedPositionName})

const mapDispatchToProps = {goToPosition};


export default connect(mapStateToProps, mapDispatchToProps)(GoToButton)



