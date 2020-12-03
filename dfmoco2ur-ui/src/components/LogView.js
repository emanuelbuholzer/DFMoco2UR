import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Chip from '@material-ui/core/Chip';
import { DataGrid } from '@material-ui/data-grid';
import Pagination from '@material-ui/lab/Pagination';
import PaginationItem from '@material-ui/lab/PaginationItem';
import PropTypes from 'prop-types'


const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
    marginTop: theme.spacing(5),
    marginBottom: theme.spacing(5),
  }
}));

const sortModel =[{
  field: 'dateTime',
  sort: 'asc'
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
  { id: 10, dateTime: new Date(), severity: "Critical", message: "blabla" },
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
  { field: 'dateTime', headerName: 'Time', ...time},
  { field: 'severity', headerName: 'Severity', sortable: false },
  { field: 'message', headerName: 'Message', type: 'string', sortable: false }];

export default function Logview(props) {
  const classes = useStyles();

  return (
    <div className={classes.root}>
      <div style={{ height: 400 }}>
        <DataGrid 
        rows={data} 
        columns={columns} 
        pageSize={100} 
        sortModel={sortModel}
        autoHeight={false} 
        hideFooterPagination={true}>
        </DataGrid>
      </div>
  </div>
  );
}





