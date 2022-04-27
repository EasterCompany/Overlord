// Local components
import './home.css';
import '../global.css';
// Local assets
import ePanelImg from '../../assets/e_panel_header.png';
// Shared components
import { clientAdr, serverAdr, serverAPI } from '../../shared/library/server/api';

const Home = () => {
  document.title = "[E PANEL] Home";

  return <>
    <img
      src={ePanelImg}
      alt="E PANEL Header"
      style={{ width: "50%", height: "50%", margin: "5vmin 25% 5vmin 25%" }}
    />

    <div style={{
      display: 'flex',
      justifyContent: 'center',
      margin: '2.5vmin auto 2.5vmin auto',
      width: '50vw',
      minWidth: "300px"
    }}>
      <span style={{
        display: 'flex',
        borderRadius: '10px',
        backgroundColor: 'rgba(99,99,99,0.66)',
        width: '145px', padding: '0 0 0 10px'
      }}>
        <h3 style={{ color: 'darkgrey' }}>STATUS:&nbsp;</h3><h3 style={{ color: '#4CAF50' }}>GOOD</h3>
      </span>

      <span style={{
        display: 'flex',
        borderRadius: '10px',
        backgroundColor: 'rgba(99,99,99,0.66)',
        width: '130px', padding: '0 0 0 10px', margin: '0 0 0 64px'
      }}>
        <h3 style={{ color: 'darkgrey' }}>UPTIME:&nbsp;</h3><h3 style={{ color: '#4CAF50' }}>95%</h3>
      </span>

      <span style={{
        display: 'flex',
        borderRadius: '10px',
        backgroundColor: 'rgba(99,99,99,0.66)',
        width: '145px', paddingLeft: '10px', margin: '0 0 0 64px'
      }}>
        <h3 style={{ color: 'darkgrey' }}>VERSION:&nbsp;</h3><h3 style={{ color: 'white' }}>0.8A</h3>
      </span>
    </div>

    <div style={{
      borderBottom: '3px solid #c44444',
      margin: '5vmin auto 0 auto',
      width: '50vw',
      minWidth: "300px"
    }}>
      <p> &nbsp;&nbsp; <b> CLIENT </b>: {clientAdr} </p>
    </div>

    <div style={{
      display: 'flex',
      justifyContent: 'space-around',
      margin: '2.5vmin auto 2.5vmin auto',
      width: '50vw',
      minWidth: "300px"
    }}>

      <div className="home-content-widget">
        <span>
          <div style={{ backgroundColor: "#b33636", width: "33%" }}>
            4
          </div>
        </span>
        <h3 style={{ color: '#b33636' }}> -97% </h3>
        <p> Last 24 hrs </p>
      </div>

      <div className="home-content-widget">
        <span>
          <div style={{ backgroundColor: "#ceb733", width: "66%" }}>
            133
          </div>
        </span>
        <h3 style={{ color: '#ceb733' }}> -18% </h3>
        <p> Last 7 days </p>
      </div>

      <div className="home-content-widget">
        <span>
          <div style={{ backgroundColor: "#4CAF50", width: "99%" }}>
            4670
          </div>
        </span>
        <h3 style={{ color: '#4CAF50' }}> +23% </h3>
        <p> Last 30 days </p>
      </div>

    </div>

    <div style={{
      borderBottom: '3px solid #c44444',
      margin: '2.5vmin auto 2.5vmin auto',
      width: '50vw',
      minWidth: "300px"
    }}>
      <p> &nbsp;&nbsp; <b> API </b>: {serverAPI} </p>
    </div>

    <div style={{
      display: 'flex',
      justifyContent: 'space-around',
      margin: '2.5vmin auto 2.5vmin auto',
      width: '50vw',
      minWidth: "300px"
    }}>

      <div className="home-content-widget" style={{ display: 'flex', minWidth: '77.5%' }} >
        <span>
          <div style={{ backgroundColor: '#b33636', width: '90%' }}>
            4670
          </div>
          <div style={{ backgroundColor: '#ceb733', width: '25%' }}>
            569
          </div>
          <div style={{ backgroundColor: '#4CAF50', width: '60%' }}>
            2938
          </div>
        </span>

        <div style={{ minWidth: '100%', display: 'flex', justifyContent: 'space-around', margin: '16px 0 16px 0' }}>

          <span className="key-span" style={{ backgroundColor: '#b33636' }}>
            <p> user </p>
          </span>

          <span className="key-span" style={{ backgroundColor: '#ceb733' }}>
            <p> post </p>
          </span>

          <span className="key-span" style={{ backgroundColor: '#4CAF50' }}>
            <p> job </p>
          </span>

        </div>
      </div>

    </div>

    <div style={{
      borderBottom: '3px solid #c44444',
      margin: '2.5vmin auto 2.5vmin auto',
      width: '50vw',
      minWidth: "300px"
    }}>
      <p> &nbsp;&nbsp; <b> SERVER </b>: {serverAdr} </p>
    </div>

    {/* SERVER TASK CYCLE - 1st ROW */}

    <h3 style={{textAlign:'center'}}> Backup & Update </h3>

    <div style={{
      display: 'flex',
      justifyContent: 'center',
      margin: '2.5vmin auto 2.5vmin auto',
      width: '50vw',
      minWidth: "300px"
    }}>

      <div style={{ display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
        <svg
          fill="rgba(99,99,99,0.5)"
          width="32px"
          height="32px"
          viewBox="0 0 24 24"
          style={{ margin: '0 auto' }}
          fillRule="evenodd"
          clipRule="evenodd">
            <path d="M19 2h-14l-5 14v6h24v-6l-5-14zm-7 3l4 4h-3v5h-2v-5h-3l4-4zm10 15h-20v-3h20v3zm-3-1.5c0-.276.224-.5.5-.5s.5.224.5.5-.224.5-.5.5-.5-.224-.5-.5z"/>
        </svg>
        <p style={{ color: 'rgba(99,99,99,0.5)' }}> Backup Server </p>
      </div>

      <b style={{ margin: '8px 32px 0 32px' }}> ➡ </b>

      <div style={{ display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
        <svg
          fill="rgba(99,99,99,0.5)"
          width="32px"
          height="32px"
          viewBox="0 0 24 24"
          style={{ margin: '0 auto' }}
          fillRule="evenodd"
          clipRule="evenodd">
            <path d="M23.548 10.931l-10.479-10.478c-.302-.302-.698-.453-1.093-.453-.396 0-.791.151-1.093.453l-2.176 2.176 2.76 2.76c.642-.216 1.377-.071 1.889.44.513.515.658 1.256.435 1.9l2.66 2.66c.644-.222 1.387-.078 1.901.437.718.718.718 1.881 0 2.6-.719.719-1.883.719-2.602 0-.54-.541-.674-1.334-.4-2l-2.481-2.481v6.529c.175.087.34.202.487.348.717.717.717 1.881 0 2.601-.719.718-1.884.718-2.601 0-.719-.72-.719-1.884 0-2.601.177-.178.383-.312.602-.402v-6.589c-.219-.089-.425-.223-.602-.401-.544-.544-.676-1.343-.396-2.011l-2.721-2.721-7.185 7.185c-.302.302-.453.697-.453 1.093 0 .395.151.791.453 1.093l10.479 10.478c.302.302.697.452 1.092.452.396 0 .791-.15 1.093-.452l10.431-10.428c.302-.303.452-.699.452-1.094 0-.396-.15-.791-.452-1.093"/></svg>
        <p style={{ color: 'rgba(99,99,99,0.5)' }}> Reset Branch </p>
      </div>

      <b style={{ margin: '8px 32px 0 32px' }}> ➡ </b>

      <div style={{ display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
        <svg
          fill="rgba(99,99,99,0.5)"
          width="32px"
          height="32px"
          viewBox="0 0 24 24"
          style={{ margin: '0 auto' }}
        >
          <path d="M21 3c0-1.657-1.343-3-3-3s-3 1.343-3 3c0 1.323.861 2.433 2.05 2.832.168 4.295-2.021 4.764-4.998 5.391-1.709.36-3.642.775-5.052 2.085v-7.492c1.163-.413 2-1.511 2-2.816 0-1.657-1.343-3-3-3s-3 1.343-3 3c0 1.305.837 2.403 2 2.816v12.367c-1.163.414-2 1.512-2 2.817 0 1.657 1.343 3 3 3s3-1.343 3-3c0-1.295-.824-2.388-1.973-2.808.27-3.922 2.57-4.408 5.437-5.012 3.038-.64 6.774-1.442 6.579-7.377 1.141-.425 1.957-1.514 1.957-2.803zm-16.8 0c0-.993.807-1.8 1.8-1.8s1.8.807 1.8 1.8-.807 1.8-1.8 1.8-1.8-.807-1.8-1.8zm3.6 18c0 .993-.807 1.8-1.8 1.8s-1.8-.807-1.8-1.8.807-1.8 1.8-1.8 1.8.807 1.8 1.8zm10.2-16.2c-.993 0-1.8-.807-1.8-1.8s.807-1.8 1.8-1.8 1.8.807 1.8 1.8-.807 1.8-1.8 1.8z"/>
        </svg>
        <p style={{ color: 'rgba(99,99,99,0.5)' }}> Pull Repository </p>
      </div>

      <b style={{ margin: '8px 32px 0 32px' }}> ➡ </b>

      <div style={{ display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
        <svg
          fill="rgba(99,99,99,0.5)"
          width="32px"
          height="32px"
          viewBox="0 0 24 24"
          style={{ margin: '0 auto' }}
        >
          <path d="M19.479 10.092c-.212-3.951-3.473-7.092-7.479-7.092-4.005 0-7.267 3.141-7.479 7.092-2.57.463-4.521 2.706-4.521 5.408 0 3.037 2.463 5.5 5.5 5.5h13c3.037 0 5.5-2.463 5.5-5.5 0-2.702-1.951-4.945-4.521-5.408zm-7.479 6.908l-4-4h3v-4h2v4h3l-4 4z"/>
        </svg>
        <p style={{ color: 'rgba(99,99,99,0.5)' }}> Run Installer </p>
      </div>

    </div>

    {/* SERVER TASK CYCLE - 2nd ROW */}

    <h3 style={{textAlign:'center'}}> Build & Test </h3>

    <div style={{
      display: 'flex',
      justifyContent: 'center',
      margin: '2.5vmin auto 2.5vmin auto',
      width: '50vw',
      minWidth: "300px"
    }}>

      <div style={{ display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
        <svg
          fill="rgba(99,99,99,0.5)"
          width="32px"
          height="32px"
          viewBox="0 0 24 24"
          style={{ margin: '0 auto' }}
        >
          <path d="M21 3c0-1.657-1.343-3-3-3s-3 1.343-3 3c0 1.323.861 2.433 2.05 2.832.168 4.295-2.021 4.764-4.998 5.391-1.709.36-3.642.775-5.052 2.085v-7.492c1.163-.413 2-1.511 2-2.816 0-1.657-1.343-3-3-3s-3 1.343-3 3c0 1.305.837 2.403 2 2.816v12.367c-1.163.414-2 1.512-2 2.817 0 1.657 1.343 3 3 3s3-1.343 3-3c0-1.295-.824-2.388-1.973-2.808.27-3.922 2.57-4.408 5.437-5.012 3.038-.64 6.774-1.442 6.579-7.377 1.141-.425 1.957-1.514 1.957-2.803zm-16.8 0c0-.993.807-1.8 1.8-1.8s1.8.807 1.8 1.8-.807 1.8-1.8 1.8-1.8-.807-1.8-1.8zm3.6 18c0 .993-.807 1.8-1.8 1.8s-1.8-.807-1.8-1.8.807-1.8 1.8-1.8 1.8.807 1.8 1.8zm10.2-16.2c-.993 0-1.8-.807-1.8-1.8s.807-1.8 1.8-1.8 1.8.807 1.8 1.8-.807 1.8-1.8 1.8z"/>
        </svg>
        <p style={{ color: 'rgba(99,99,99,0.5)' }}> Build Clients </p>
      </div>

      <b style={{ margin: '8px 32px 0 32px' }}> ➡ </b>

      <div style={{ display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
        <svg
          fill="rgba(99,99,99,0.5)"
          width="32px"
          height="32px"
          viewBox="0 0 24 24"
          style={{ margin: '0 auto' }}
        >
          <path d="M12.255 21.954c-.443.03-.865.046-1.247.046-3.412 0-8.008-1.002-8.008-2.614v-2.04c2.197 1.393 5.513 1.819 8.099 1.778-.146-.64-.161-1.39-.085-1.998h-.006c-3.412 0-8.008-1.001-8.008-2.613v-2.364c2.116 1.341 5.17 1.78 8.008 1.78l.569-.011.403-2.02c-.342.019-.672.031-.973.031-3.425-.001-8.007-1.007-8.007-2.615v-2.371c2.117 1.342 5.17 1.78 8.008 1.78 2.829 0 5.876-.438 7.992-1.78v2.372c0 .871-.391 1.342-1 1.686 1.178 0 2.109.282 3 .707v-7.347c0-3.361-5.965-4.361-9.992-4.361-4.225 0-10.008 1.001-10.008 4.361v15.277c0 3.362 6.209 4.362 10.008 4.362.935 0 2.018-.062 3.119-.205-1.031-.691-1.388-1.134-1.872-1.841zm-1.247-19.954c3.638 0 7.992.909 7.992 2.361 0 1.581-5.104 2.361-7.992 2.361-3.412.001-8.008-.905-8.008-2.361 0-1.584 4.812-2.361 8.008-2.361zm6.992 15h-5l1-5 1.396 1.745c.759-.467 1.647-.745 2.604-.745 2.426 0 4.445 1.729 4.901 4.02l-1.96.398c-.271-1.376-1.486-2.418-2.941-2.418-.483 0-.933.125-1.335.331l1.335 1.669zm5 2h-5l1.335 1.669c-.402.206-.852.331-1.335.331-1.455 0-2.67-1.042-2.941-2.418l-1.96.398c.456 2.291 2.475 4.02 4.901 4.02.957 0 1.845-.278 2.604-.745l1.396 1.745 1-5z"/>
        </svg>
        <p style={{ color: 'rgba(99,99,99,0.5)' }}> Reload Server & Cache </p>
      </div>

      <b style={{ margin: '8px 32px 0 32px' }}> ➡ </b>

      <div style={{ display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
        <svg
          fill="rgba(99,99,99,0.5)"
          width="32px"
          height="32px"
          viewBox="0 0 24 24"
          style={{ margin: '0 auto' }}
        >
          <path d="M4.045 22h-1.622c-1.4 0-2.423-1.162-2.423-2.445 0-.35.076-.709.241-1.057l3.743-6.856c1.041-2.186 2.016-4.581 2.016-7.007v-.635h2l-.006 1c-.09 2.71-1.158 5.305-2.205 7.501l-3.742 6.857c-.147.303.076.642.376.642h1.887c-.352.934-.33 1.39-.265 2zm1.955-20h6c.553 0 1-.448 1-1s-.447-1-1-1h-6c-.553 0-1 .448-1 1s.447 1 1 1zm12 1h-6c-.553 0-1 .448-1 1s.447 1 1 1h6c.553 0 1-.448 1-1s-.447-1-1-1zm6 18.554c0 1.284-1.023 2.446-2.424 2.446h-13.153c-1.4 0-2.423-1.162-2.423-2.445 0-.35.076-.709.241-1.057 2.385-3.732 5.759-8.129 5.759-12.863v-.635h2l-.006 1c-.104 3.105-1.492 6.005-2.441 8h4.666l3.861 6h1.496c.309 0 .52-.342.377-.644-2.441-3.817-5.78-8.144-5.953-13.356v-1h2v.635c0 4.732 3.354 9.101 5.759 12.862.165.348.241.707.241 1.057z"/>
        </svg>
        <p style={{ color: 'rgba(99,99,99,0.5)' }}> Backend & API </p>
      </div>

      <b style={{ margin: '8px 32px 0 32px' }}> ➡ </b>

      <div style={{ display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
        <svg
          fill="rgba(99,99,99,0.5)"
          width="32px"
          height="32px"
          viewBox="0 0 24 24"
          style={{ margin: '0 auto' }}
        >
          <path d="M15.794 2.707c-.634-.634-.174-1.707.707-1.707.256 0 .512.098.707.293l4.243 4.242c.391.391.391 1.023 0 1.414s-1.023.391-1.414 0l-4.243-4.242zm-1.811 9.293h-11.42l-.445-.445c-.212-.213-.129-.609.188-.721 6.171-1.357 9.375-1.261 13.573-5.414l-1.414-1.414c-3.784 3.794-7.231 3.712-12.827 4.944-1.029.366-1.638 1.317-1.638 2.322 0 .605.224 1.217.705 1.697l9.301 9.301c.48.48 1.091.73 1.696.73 1 0 1.955-.629 2.323-1.664 1.235-5.617.884-9.288 4.683-13.086l-1.414-1.414c-1.732 1.732-2.689 3.398-3.311 5.164zm10.017 1.517c0 1.363-1.106 2.483-2.47 2.483-2.991 0-4.06-4.22.912-8-.058 2.365 1.558 3.302 1.558 5.517zm-2.371-3.466c-.346.189-.856.698-.934 1.333-.115.95.867 1.23.953-.044.04-.537 0-.794-.019-1.289z"/>
        </svg>
        <p style={{ color: 'rgba(99,99,99,0.5)' }}> Frontend Client </p>
      </div>

    </div>

    {/* SERVER TASK CYCLE - 3rd ROW */}

    <div style={{ width: '300px', border: '1px solid rgba(99,99,99,0.5)', margin: '0 auto' }} />

    <div style={{
      display: 'flex',
      justifyContent: 'center',
      margin: '2.5vmin auto 2.5vmin auto',
      width: '50vw',
      minWidth: "300px"
    }}>

      <div style={{ display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
        <svg
          fill="rgba(99,99,99,0.5)"
          width="32px"
          height="32px"
          viewBox="0 0 24 24"
          style={{ margin: '0 auto' }}
        >
          <path d="M13.931 10.245l2.021-2.042-2.778-.403-1.223-2.653-1.222 2.653-2.778.402 2.021 2.042-.492 2.903 2.471-1.391 2.472 1.391-.492-2.902zm-9.481 4.518c-.866-1.382-1.374-3.012-1.374-4.763 0-4.971 4.029-9 9-9s9 4.029 9 9c0 1.792-.53 3.458-1.433 4.861-.607-.31-1.228-.585-1.862-.819.812-1.143 1.295-2.536 1.295-4.042 0-3.86-3.141-7-7-7s-7 3.14-7 7c0 1.476.462 2.844 1.244 3.974-.636.225-1.26.488-1.87.789zm15.307 2.45l-2.334 3.322c-1.603-.924-3.448-1.464-5.423-1.473-1.975.009-3.82.549-5.423 1.473l-2.334-3.322c2.266-1.386 4.912-2.202 7.757-2.211 2.845.009 5.491.825 7.757 2.211zm4.243 2.787h-2.359l-.566 3c-.613-1.012-1.388-1.912-2.277-2.68l2.343-3.335c1.088.879 2.052 1.848 2.859 3.015zm-21.14-3.015l2.343 3.335c-.89.769-1.664 1.668-2.277 2.68l-.566-3h-2.36c.807-1.167 1.771-2.136 2.86-3.015z"/>
        </svg>
        <p style={{ color: 'rgba(99,99,99,0.5)' }}> Verified </p>
      </div>

    </div>

    <div style={{
      display: 'flex',
      justifyContent: 'center',
      margin: '2.5vmin auto 2.5vmin auto',
      width: '50vw',
      minWidth: "300px"
    }}>

    </div>

    {/* SERVER TASK CYCLE - 4th ROW */}

    <h3 style={{textAlign:'center'}}> Reboot Server </h3>

    <div style={{
      display: 'flex',
      justifyContent: 'center',
      margin: '2.5vmin auto 2.5vmin auto',
      width: '50vw',
      minWidth: "300px"
    }}>

      <div style={{ display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
        <svg
          fill="rgba(99,99,99,0.5)"
          width="32px"
          height="32px"
          viewBox="0 0 24 24"
          style={{ margin: '0 auto' }}
        >
          <path d="M15.408 21h-9.908c-3.037 0-5.5-2.463-5.5-5.5 0-2.702 1.951-4.945 4.521-5.408.212-3.951 3.473-7.092 7.479-7.092 3.267 0 6.037 2.089 7.063 5.003l-.063-.003c-.681 0-1.336.102-1.958.283-.878-2.025-2.73-3.283-5.042-3.283-3.359 0-5.734 2.562-5.567 6.78-1.954-.113-4.433.923-4.433 3.72 0 1.93 1.57 3.5 3.5 3.5h7.76c.566.81 1.3 1.49 2.148 2zm2.257-8.669c.402-.206.852-.331 1.335-.331 1.455 0 2.67 1.042 2.941 2.418l1.96-.398c-.456-2.291-2.475-4.02-4.901-4.02-.957 0-1.845.278-2.604.745l-1.396-1.745-1 5h5l-1.335-1.669zm5.335 8.669l-1.396-1.745c-.759.467-1.647.745-2.604.745-2.426 0-4.445-1.729-4.901-4.02l1.96-.398c.271 1.376 1.486 2.418 2.941 2.418.483 0 .933-.125 1.335-.331l-1.335-1.669h5l-1 5z"/>
        </svg>
        <p style={{ color: 'rgba(99,99,99,0.5)' }}> Restart </p>
      </div>

      <b style={{ margin: '8px 32px 0 32px' }}> ➡ </b>

      <div style={{ display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
        <svg
          fill="rgba(99,99,99,0.5)"
          width="32px"
          height="32px"
          viewBox="0 0 24 24"
          style={{ margin: '0 auto' }}
        >
          <path d="M0 1v16.981h4v5.019l7-5.019h13v-16.981h-24zm7 10c-.828 0-1.5-.671-1.5-1.5s.672-1.5 1.5-1.5c.829 0 1.5.671 1.5 1.5s-.671 1.5-1.5 1.5zm5 0c-.828 0-1.5-.671-1.5-1.5s.672-1.5 1.5-1.5c.829 0 1.5.671 1.5 1.5s-.671 1.5-1.5 1.5zm5 0c-.828 0-1.5-.671-1.5-1.5s.672-1.5 1.5-1.5c.829 0 1.5.671 1.5 1.5s-.671 1.5-1.5 1.5z"/>
        </svg>
        <p style={{ color: 'rgba(99,99,99,0.5)' }}> Check Status </p>
      </div>

      <b style={{ margin: '8px 32px 0 32px' }}> ➡ </b>

      <div style={{ display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
        <svg
          fill="rgba(99,99,99,0.5)"
          width="32px"
          height="32px"
          viewBox="0 0 24 24"
          style={{ margin: '0 auto' }}
        >
          <path d="M20 12.194v9.806h-20v-20h18.272l-1.951 2h-14.321v16h16v-5.768l2-2.038zm.904-10.027l-9.404 9.639-4.405-4.176-3.095 3.097 7.5 7.273 12.5-12.737-3.096-3.096z"/>
        </svg>
        <p style={{ color: 'rgba(99,99,99,0.5)' }}> Success </p>
      </div>

    </div>

    <div style={{
      margin: '2.5vh auto 0 auto',
      padding: '16px',
      backgroundColor: 'rgba(99,99,99,0.45)',
      borderRadius: '8px',
      width: '33vw',
      minWidth: '300px'
    }}>

      <h3 style={{ textAlign: 'center', width: '100%', margin: '6px auto 16px auto' }}> User Actions </h3>

      <div style={{
        display: 'flex',
        justifyContent: 'center',
      }}>
        <button className="basic-btn"> Backup & Update </button>
        <button className="basic-btn"> Build & Test </button>
      </div>

      <div style={{
        display: 'flex',
        justifyContent: 'center',
      }}>
        <button className="basic-btn"> Reboot Server </button>
        <button className="basic-btn"> Run All (Deploy) </button>
      </div>

    </div>
  </>
}


export default Home;
