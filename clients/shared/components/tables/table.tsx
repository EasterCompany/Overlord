// React imports
import './table.css';
import { useState } from 'react';
// Shared library
import api from '../../library/server/api';
// Shared components
import { dp } from '../routes/routes';
import ConfirmationModal from '../modals/confirmation';
import filterElements from '../search/table/filterElements';


/*
    ERROR VIEW
    reports error messages as a view
*/
export const ErrorView = (props: any) => <>
  <h2> ERROR </h2>
  <p> {props.error} </p>
</>


/*
  TABLE COMPONENT
*/
const Table = (props: any) => {

  // State Managers
  const [selectedRow, selectRow] = useState('');
  const [viewAll, setViewAll] = useState(false);
  const [createView, setCreateView] = useState(false);
  const [editView, setEditView] = useState(false);
  const [deleteView, setDeleteView] = useState(false);

  const config = {
    /* Basic */
    name: props.name || '',
    previewSize: props.previewSize || 1,

    /* TABLE */
    tableHeaders: props.headers || [ 'ERROR', ],
    tableData: props.data || [
      [ 'No headers & data props on the <Table .. headers=[string, ] .. data = [ [], ]>', ],
    ],

    /* API Paths */
    viewAPI: props.view !== null ? props.view : <ErrorView error={{message:"no view."}}/>,
    createAPI: props.create !== null ? props.create : <ErrorView error={{message:"no view."}}/>,
    deleteAPI: props.delete !== null ? props.delete : <ErrorView error={{message:"no view."}}/>,
  };

  // View State Variables
  const buttonTxt = viewAll ? `..SEE LESS` : `SEE MORE..`;

  // Alternative Views
  if (createView) {
    return <props.CreateView close={() => { window.location.reload() }}/>
  }

  if (editView) {
    const pkRowEl = document.getElementById(selectedRow) as HTMLElement
    const pkEl = pkRowEl.firstChild as HTMLElement
    const PK = pkEl.innerText.trim()
    window.location.href = window.location.href += `/${encodeURIComponent(PK)}`;
  }

  if (deleteView) {
    const pkRowEl = document.getElementById(selectedRow) as HTMLElement
    const pkEl = pkRowEl.firstChild as HTMLElement
    const PK = pkEl.innerText

    const onAccept = () => {
      api(
        `${config.deleteAPI}/${encodeURIComponent(PK)}`,
        (resp: any) => null,
        (resp: any) => window.location.reload()
      );
    }

    const modal = {
      header: `DELETE [ ${config.name} ]`,
      message: `delete ${PK}`,
      accept: onAccept,
      cancel: () => { window.location.reload() }
    }

    return <ConfirmationModal modal={modal} />

  }

  return <>
    <div className="flex-between" style={{paddingTop: "2.5vmin"}}>

      <div className="flex-right" style={{
          padding: "2px 2px 8px 8px",
          borderRadius: "6px",
          borderTop: "3px solid #c4444444",
          borderRight: "1px solid #c4444444",
        }}>

        <div
          style={{ display: 'flex', justifyContent: 'center' }}
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="24px" height="24px"
            style={{ padding: "12px" }}
            viewBox="0 0 24 24" fill="white"
          >
            <path d="M23.111 20.058l-4.977-4.977c.965-1.52 1.523-3.322 1.523-5.251 0-5.42-4.409-9.83-9.829-9.83-5.42 0-9.828 4.41-9.828 9.83s4.408 9.83 9.829 9.83c1.834 0 3.552-.505 5.022-1.383l5.021 5.021c2.144 2.141 5.384-1.096 3.239-3.24zm-20.064-10.228c0-3.739 3.043-6.782 6.782-6.782s6.782 3.042 6.782 6.782-3.043 6.782-6.782 6.782-6.782-3.043-6.782-6.782zm2.01-1.764c1.984-4.599 8.664-4.066 9.922.749-2.534-2.974-6.993-3.294-9.922-.749z"/>
          </svg>
          <input
            id="form-search"
            name="form-search"
            style={{
              width: "25vw",
              height: "12px",
              borderRadius: "6px",
              margin: "12px 6px 0 12px",
              padding: "6px"
            }}
            type="text"
            onChange={ (event: any) =>
              filterElements('form-search', config.tableData.length)
            }
          />
        </div>
      </div>

      { props.view === undefined && props.create === undefined && props.delete === undefined ? <></> :
        <div className="flex-right" style={{
          padding: "2px 2px 8px 8px",
          borderRadius: "6px",
          borderTop: "3px solid #c4444444",
          borderRight: "1px solid #c4444444",
        }}>
          { props.create === undefined ? <> </> :
            <button
              disabled={config.createAPI !== '' ? false : true}
              onClick={() => setCreateView(!createView)}
              style={{ display: 'flex', justifyContent: 'center' }}
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="18px" height="18px"
                style={{ margin: '2px' }}
                viewBox="0 0 24 24" fill="white"
              >
                <path d="M24 9h-9v-9h-6v9h-9v6h9v9h6v-9h9z"/>
              </svg>
              <h4 style={{ margin: "1px 0 0 12px", padding: "0 0 0 0" }}> CREATE </h4>
            </button>}

          { props.view === undefined ? <> </> :
            <button
              disabled={selectedRow && config.deleteAPI !== '' ? false : true}
              onClick={() => setEditView(!editView)}
              style={{ display: 'flex', justifyContent: 'center' }}
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="18px" height="18px"
                style={{ margin: '2px' }}
                viewBox="0 0 24 24" fill="white"
              >
                <path d="
                  M9 19h-4v-2h4v2zm2.946-4.036l3.107 3.105-4.112.931 1.005-4.036zm12.054-5.839l-7.898 7.996-3.202-3.202
                  7.898-7.995 3.202 3.201zm-6 8.92v3.955h-16v-20h7.362c4.156 0 2.638 6 2.638 6s2.313-.635
                  4.067-.133l1.952-1.976c-2.214-2.807-5.762-5.891-7.83-5.891h-10.189v24h20v-7.98l-2 2.025z
                "/>
              </svg>
              <h4 style={{ margin: "1px 0 0 12px", padding: "0 0 0 0" }}> VIEW & EDIT </h4>
            </button>}

          { props.delete === undefined ? <> </> :
            <button
              disabled={selectedRow && config.deleteAPI !== '' ? false : true}
              onClick={() => setDeleteView(!deleteView)}
              style={{ display: 'flex', justifyContent: 'center' }}
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="18px" height="18px"
                style={{ margin: '2px' }}
                viewBox="0 0 24 24" fill="white"
              >
                <path d="
                  M24 20.188l-8.315-8.209 8.2-8.282-3.697-3.697-8.212 8.318-8.31-8.203-3.666 3.666 8.321 8.24-8.206
                  8.313 3.666 3.666 8.237-8.318 8.285 8.203z
                "/>
              </svg>
              <h4 style={{ margin: "1px 0 0 12px", padding: "0 0 0 0" }}> DELETE </h4>
            </button>}

        </div>
      }
    </div>

    <table>

      {/* Table Headers */}
      <tr>
        {config.tableHeaders.map( (header: any) =>
          <th> {header} </th>
        )}
      </tr>

      {/* Table Rows */}
      { (viewAll ? config.tableData : config.tableData.slice(0, config.previewSize)).map((
          row: any, row_index: number
        ) => {
          const rowID = `${row_index}`;
          return <tr
            id={rowID}
            className={selectedRow === rowID ? 'selectedRow' : ''}
            onClick={() => selectedRow === rowID ? selectRow('') : selectRow(rowID)}
          >
            {row.map( (data: any, data_index: number) => {
              const data_id = `${rowID},${data_index}`;
              return <td id={data_id}> { data } </td>
            })}
          </tr>
        })
      }

      {/* Table View More... */}
      {
        viewAll || config.tableData.length <= config.previewSize ?
        null : <tr> <td> ... </td> </tr>
      }
    </table>

    <div className="flex-between">
      <div className="flex-left">
        <button
          onClick={() => setViewAll(!viewAll)}
          disabled={ props.data.length <= props.previewSize ? true : false }
        > {buttonTxt} </button>
      </div>
    </div>

  </>
}


export default Table;
