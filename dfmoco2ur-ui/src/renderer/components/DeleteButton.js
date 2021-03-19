import React from "react";
import Button from '@material-ui/core/Button';
import {deletePosition} from "../services/socket/actions"
import { connect } from 'react-redux';


function DeleteButton({selectedPosition, deletePosition}) {
    return (
        <Button onClick={() => deletePosition(selectedPosition)}>Delete</Button>
    )
}

const mapStateToProps = state => {
    return {
        selectedPosition: state.socket.selectedPositionName
    }
};

const mapDispatchToProps = { deletePosition };

export default connect(mapStateToProps, mapDispatchToProps)(DeleteButton);