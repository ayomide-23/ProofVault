import {Routes, Route, Navigate, useLocation } from 'react-router-dom'
import Login from './pages/Login.jsx'
import {useauth } from './auth.jsx'
import Home from './pages/Home.jsx';
import CreateAgreement from './pages/CreateAgreement.jsx';
import AgreementPage from "./pages/AgreementPage.jsx";

//function to redirct check if a user can access homepage
function Requireauth({children}){
  const {user} = useauth();
  const location = useLocation();
  if(!user){
    return <Navigate to={`/login?next=${encodeURIComponent(location.pathname)}`} replace/>
  }
  return children
}

//function to check if user is authenticated trying to access from /
function Redirect(){
  const {user} = useauth();
  return <Navigate to={user ? "/home" : "/login"} replace/>
}

export default function App(){
  return(
    <Routes>
      <Route path="/" element={<Redirect/>} />
      <Route path="/login" element={<Login/>} />
      <Route path="/home" element={<Requireauth><Home/></Requireauth>} />
      <Route path="/new" element={<Requireauth><CreateAgreement/></Requireauth>} />
      <Route path="/agreements/:id" element={<Requireauth><AgreementPage/></Requireauth>} />
    </Routes>
  )
}
