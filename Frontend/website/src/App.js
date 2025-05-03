import logo from './logo.svg';
import './App.css';
import Homepage from './Pages/homepage';
import { BrowserRouter, Route, Routes } from "react-router-dom";
import Register from './Pages/register';
import Login from './Pages/login';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

function App() {
  return (
    <BrowserRouter>
          <Routes>
            <Route path="/" element={<Homepage />} />

            <Route path="/register" element={<Register />} />
            <Route path="/login" element={<Login />} />
              

          </Routes>
          <ToastContainer 
            position="top-center"
            autoClose={3000}
            hideProgressBar={false}
            newestOnTop
            closeOnClick
            pauseOnHover
            theme="colored"
          />
    </BrowserRouter >
  );
}

export default App;
