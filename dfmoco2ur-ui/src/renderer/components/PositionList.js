import React from 'react';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem'
import { ListItemText } from '@material-ui/core';
import { connect } from 'react-redux';
import  { selectPosition, loadPositions } from '../services/socket/actions'


function PositionList({ positionNames, selectedPositionName, selectPosition, loadPositions }) {

    return (
        <List>
            {positionNames.map((positionName, i) => {
                let isSelected = positionName === selectedPositionName;
                return (
                    <ListItem button key={i} selected={isSelected} onClick={() => selectPosition(positionName)}>
                        <ListItemText>{positionName}</ListItemText>
                    </ListItem>
                )
            })}
        </List>

    )
}

const mapStateToProps = (state) => {

    return {
        positionNames: state.socket.positionNames,
        selectedPositionName: state.socket.selectedPositionName,
    }
}

const mapDispatchToProps = {selectPosition, loadPositions}

export default connect(mapStateToProps, mapDispatchToProps)(PositionList);