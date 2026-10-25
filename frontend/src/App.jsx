import { BrowserRouter, Routes, Route, Navigate, useLocation } from 'react-router-dom'
import Login from './pages/Login.jsx'
import { Authprovider, useauth } from './auth.jsx'


function Requireauth({children}){
  const {user_loggedin} = useauth();
  const location = useLocation();
  if(!user_loggedin){
    return <Navigate to={`/login?next=${location.pathname}`} replace/>
  }
}

export default function App(){
  return(
    <Routes>
      <Route path="/login" element={<Login/>} />
    </Routes>
  )
}
