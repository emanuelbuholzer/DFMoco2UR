import * as React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import { DataGrid } from '@material-ui/data-grid';
import { connect } from 'react-redux';

const useStyles = makeStyles((theme) => ({
  root: {
    height: '62vh'
  }
}));

const sortModel = [{
  field: 'time',
  sort: 'desc'
}]

const time = {
  type: 'date',
  valueFormatter: ({ value }) => `${value.getHours()}:${value.getMinutes()}:${value.getSeconds()}`,
  cellClassName: ''
}

const columns = [
  // TODO: Style text according to its severity
  { field: 'severity', headerName: 'Severity', sortable: false, flex: 0.2, headerClassName: 'log-column-header', headerAlign: 'center' },
  { field: 'time', headerName: 'Time', ...time, flex: 0.2, headerClassName: 'log-column-header', headerAlign: 'center' },
  // TODO: Set width after getting the longest message (by hand)
  { field: 'message', headerName: 'Message', type: 'string', sortable: false, flex: 1, headerClassName: 'log-column-header', headerAlign: 'center', width: 450 }, 
];


const mapStateToProps = (state) => {
  return {
    logs: state.socket.logs,
    pageSize: state.socket.pageSize
  }
}

function LogView({ logs, pageSize }) {
  const classes = useStyles();

  return (
    <div className={classes.root}>
      <DataGrid
        rows={logs}
        columns={columns}
        pageSize={pageSize}
        sortModel={sortModel}
        autoHeight={false}
        hideFooterPagination={true}
        hideFooter={true}>
      </DataGrid>
    </div>
  );
}

export default connect(mapStateToProps, {})(LogView);




