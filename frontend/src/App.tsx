import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import './App.scss'
import { Header } from './components/Header';
import { Login } from './components/Login';
import { Home } from './components/Home';
import { Signup } from './components/Signup';
import { Admin } from './components/Admin';
import useAuthRedirect from "./hooks/useAuthRedirect";

export const App = () => {
  const AllRoutes = () => {
    useAuthRedirect();

    return (
      <Routes>
        <Route path="/" element={<Home/>} />
        <Route path="/login/" element={<Login/>}/>
        <Route path="/signup/" element={<Signup/>}/>
        <Route path="/admin/" element={<Admin/>}/>
        {/* <Route path="*" element={<NotFound />} /> */}
      </Routes>
    )
  }
  
  return (
    <Router>
      <Header/>
      <div className='page-content'>
        <AllRoutes></AllRoutes>
      </div>
    </Router>
  )
}
