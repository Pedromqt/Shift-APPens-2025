import logo from './logo.svg';
import './App.css';
import Homepage from './Pages/homepage';
import { BrowserRouter, Route, Routes } from "react-router-dom";
import Register from './Pages/register';
import Login from './Pages/login';

function App() {
  return (
    <BrowserRouter>
          <Routes>
            <Route path="/" element={<Homepage />} />

            <Route path="/register" element={<Register />} />
            <Route path="/login" element={<Login />} />
              

          </Routes>
    </BrowserRouter >
  );
}

export default App;
