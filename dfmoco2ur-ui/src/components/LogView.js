import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import { DataGrid } from '@material-ui/data-grid';



const useStyles = makeStyles((theme) => ({
  root: {
    height: '62vh'
  }
}));

const sortModel =[{
  field: 'dateTime',
  sort: 'desc'
}]

const data = [
  { id: 1, dateTime: new Date(), severity: "Critical", message: "blabla" },
  { id: 2, dateTime: new Date(), severity: "Critical", message: "blabla" },
  { id: 3, dateTime: new Date(), severity: "Critical", message: "blabla" },
  { id: 4, dateTime: new Date(), severity: "Critical", message: "blabla" },
  { id: 5, dateTime: new Date(), severity: "Critical", message: "blabla" },
  { id: 6, dateTime: new Date(), severity: "Critical", message: "blabla" },
  { id: 7, dateTime: new Date(), severity: "Critical", message: "blabla" },
  { id: 8, dateTime: new Date(), severity: "Critical", message: "blabla" },
  { id: 9, dateTime: new Date(), severity: "Critical", message: "blabla" },
  { id: 10, dateTime: new Date(), severity: "Critical", message: "this text is intended to test the width of the message cell of the log table in order to check what happens when this text is intended to test the width of the message cell of the log table i order to check wehat happens" },
  { id: 11, dateTime: new Date(), severity: "Critical", message: "blabla" },
  { id: 12, dateTime: new Date(), severity: "Critical", message: "blabla" },
  { id: 13, dateTime: new Date('December 17, 2019 14:23:15'), severity: "Critical", message: "blabla" },
  { id: 14, dateTime: new Date('December 17, 2019 14:22:15'), severity: "Critical", message: "blabla" }];

const time = {
  type: 'date',
  valueFormatter: ({ value }) => `${value.getHours()}:${value.getMinutes()}:${value.getSeconds()}`,
  cellClassName: ''
}

const columns = [
  { field: 'dateTime', headerName: 'Time', ...time, flex: 0.2, headerClassName: 'log-column-header', headerAlign: 'center'},
  { field: 'severity', headerName: 'Severity', sortable: false, flex: 0.2, headerClassName: 'log-column-header', headerAlign: 'center'},
  // TODO: Set width after getting the longest message (by hand)
  { field: 'message', headerName: 'Message', type: 'string', sortable: false, flex: 1, headerClassName: 'log-column-header', headerAlign: 'center'}];

export default function Logview(props) {
  const classes = useStyles();

  return (
    <div className={classes.root}>
        <DataGrid 
        rows={data} 
        columns={columns} 
        pageSize={100} 
        sortModel={sortModel}
        autoHeight={false} 
        hideFooterPagination={true}
        hideFooter={true}>
        </DataGrid>
  </div>
  );
}





