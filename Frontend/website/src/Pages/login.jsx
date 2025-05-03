import "../Pages/login.css"
import { useState } from 'react';
import axios from 'axios';
import { toast } from 'react-toastify';

const Login = () => {

    const [formData, setFormData] = useState({
        email: '',
        password: ''
    });

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        const { email, password } = formData;
        console.log('Form data:', formData); // Logando os dados do formulário
        try {
            const response = await axios.post('http://127.0.0.1:8000/login_cliente/', formData,{
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            // Armazenando os dados do usuário no localStorage
            localStorage.setItem('userData', JSON.stringify(response.data)); // Armazenando dados do usuário
            localStorage.setItem('authToken', response.data.token); // Armazenando o token de autenticação

            console.log('Login successful:', response.data);
            toast.success('Login realizado com sucesso!');
            setTimeout(() => {
                window.location.href = '/';
            }, 2000);
        } catch (error) {
            console.error('Error during login:', error);
            toast.error('Tente novamente.');
        }
    }

    return (
        <div className='register-container'>
            <form className='login-box' onSubmit={handleSubmit}>
                <h1>Login</h1>
                <div className='n-input'>
                    <label htmlFor="email">Email</label>
                    <input
                        className='box'
                        type="email"
                        id="email"
                        name="email"
                        value={formData.email}
                        onChange={handleChange}
                        required
                    />
                </div>
                <div className='n-input'>
                    <label htmlFor="password">Password</label>
                    <input
                        className='box'
                        type="password"
                        id="password"
                        name="password"
                        value={formData.password}
                        onChange={handleChange}
                        required
                    />
                </div>
                <div>
                    <button type="submit" className='register-button'>Submit</button>
                </div>
            </form>
        </div>
    );
}

export default Login;