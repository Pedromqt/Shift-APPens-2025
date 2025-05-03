import '../FirstSection/FirstSection.css'
import { useState, useEffect } from 'react';
import { toast } from 'react-toastify';
import axios from 'axios';

const FirstSection = () => {
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const [userName, setUserName] = useState('');
    const [handleSoftwareflag, setHandleSoftwareflag] = useState(true);

    const handleSoftware = async () => {

        setHandleSoftwareflag(false);
        toast.success('A iniciar Software!');
        try {
            const response = await axios.get('http://127.0.0.1:8000/executar_script/');

            if (response.ok) {
                toast.success('Software iniciado!');
            } 
        } catch (error) {
            toast.error('Erro na comunicação com o servidor.');
            console.error(error);
        }
    };



    useEffect(() => {
        const userData = localStorage.getItem('userData');
        if (userData) {
            const parsedUserData = JSON.parse(userData);
            setIsLoggedIn(true);
            setUserName(parsedUserData.nome_completo);
        }
    }, []);

    const handlePage = (page) => {

        if (page === 0) {
            window.location.href = '/register';
        } else if (page === 1) {
            window.location.href = '/login';
        }
    }


    const handleLogout = () => {
        localStorage.removeItem('userData');
        localStorage.removeItem('authToken');
        setIsLoggedIn(false);
        setUserName('');
        toast.success('Logout realizado com sucesso!');
    }
    const handleSoftwareShutdown = async () => {
        try {
            const response = await axios.get('http://127.0.0.1:8000/kill_script/');
            toast.success('Software desligado!');
            setHandleSoftwareflag(true);
        } catch (error) {
        }
    };

    return (
        <div className='first-section-container'>
            <h1 className='brand-name-first-section'>
                {isLoggedIn ? (
                    <span className='welcome-text'>{userName}, </span>
                ) : null}
                <span className='welcome-text'>Welcome to </span>
                <span className='brand-name-black'>g</span>
                <span className='brand-name-black'>u</span>
                <span className='brand-name-green'>I</span>
                <span className='brand-name-green'>A</span>
                <span className='brand-name-black'>r</span>
            </h1>
            <div className='middle-part-text'>
                <span className='brand-name-green'>I</span>
                <span className='brand-name-green'>A </span>
                para guiar quem mais precisa
            </div>
            {isLoggedIn ? (
                <>
                    {handleSoftwareflag ? <button className='register-button' onClick={handleSoftware}>Ligar Software</button> : <button className='register-button' onClick={handleSoftwareShutdown}>Desligar Software</button>}
                    <button className='register-button' onClick={handleLogout}>Sair</button>
                </>
            ) : (
                <div className='registerButtons'>
                    <button className='register-button' onClick={() => handlePage(0)}>Registrar</button>
                    <button className='register-button' onClick={() => handlePage(1)}>Entrar</button>
                </div>
            )}
        </div>
    )
}

export default FirstSection;