import './main.css'
import Navbar from './../components/navbar/navbar'
import PopApps from './../components/popApps/popApps'


const Main = () => {
  return <div>
    <Navbar/>
    <div className='main-app-divider' />
    <div className='main-app-container'>
      <PopApps/>
    </div>
  </div>
}


export default Main;
