
import './App.css'
import Login from './pages/Login'
import RankTable from './pages/RankTable'
import cookie from 'react-cookies'
import React from 'react'
import Signup from './pages/Signup'


function App() {
  const [token, setToken] = React.useState<string>(cookie.load('token'))
  const [isLoginPage, setIsLoginPage] = React.useState(true)
  return (
    <>
        <div className='container'>
          {
              (token)
                ? <RankTable setToken={setToken}></RankTable>
                : (isLoginPage) ?<Login setToken={setToken} setIsLoginPage={setIsLoginPage}></Login> : <Signup setToken={setToken} setIsLoginPage={setIsLoginPage}></Signup>
          }
        </div>
          
    
    </>
  )
}

export default App
