import * as React from 'react';
import { DataGrid } from '@material-ui/data-grid';

const columns = [
  { field: 'dateTime', headerName: 'dateTime', type: 'date', width: 150 },
  { field: 'severity', headerName: 'severity', width: 90 },
  { field: 'message',  headerName: 'message', type: 'text', width: 300,  },
  
  /*  // getter method which would be nice, but adds an empty column to the grid
      { valueGetter: (params) =>
      `${params.getValue('dateTime') || ''} 
        ${params.getValue('severity') || ''
      } ${params.getValue('message') || ''}`,
  }, */
];

const rows = [
  { id: 1, severity: 'critical', dateTime: '11.11.2020 14:00', message: "you have been promoted general" },
  { id: 2, severity: 'info', dateTime: '12.11.2020 15:30 ', message: "mom says i'm special" },
  { id: 3, severity: 'warning', dateTime: '10.10.2010', message: "make america great again" },
  { id: 4, severity: 'warning', dateTime: '11.11.2019', message: "ja, .. es ist ja so.." },
  { id: 5, severity: 'debug', dateTime: '12.12.2020', message: null },
  { id: 6, severity: 'debug', dateTime: null, message: "meh dräck" },
  { id: 7, severity: null, dateTime: '13.10.2020 - 15:00', message: "tatüü tataaa die post ist da" },
  { id: 8, severity: 'info', dateTime: '04.10.2020 17:00', message: "und die sieben geislein auch" },
  { id: 9, severity: 'error', dateTime: null, message: "alea acta est" },
];

export default function dataTable() {
  return (
    <div style={{ height: 400, width: '100%' }}>
      <DataGrid rows={rows} columns={columns} pageSize={5} checkboxSelection />
    </div>
  );
}
