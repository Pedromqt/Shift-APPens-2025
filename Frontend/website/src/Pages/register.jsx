import '../Pages/register.css';
import { useState } from 'react';
import axios from 'axios';

const Register = () => {
  const [formData, setFormData] = useState({
    nome_completo: '',
    password: '',
    idade: '',
    morada: '',
    email: '',
    observacoes: ''
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault(); // Evita refresh da página

    // Garantir que a idade seja um número inteiro
    const idadeInt = parseInt(formData.idade, 10);
    
    // Verificar se a idade é um número válido
    if (isNaN(idadeInt)) {
      console.error('Idade deve ser um número válido!');
      return;
    }

    // Atualizar o estado para garantir que a idade seja um número inteiro
    const updatedFormData = {
      ...formData,
      idade: idadeInt,
    };

    try {
      const response = await axios.post('http://127.0.0.1:8000/registar_cliente/', updatedFormData, {
        headers: {
          'Content-Type': 'application/json', // Garanta que o conteúdo seja JSON
        },
      });
      console.log('Dados enviados com sucesso:', response.data);
      // Aqui você pode limpar o formulário ou redirecionar
    } catch (error) {
      console.error('Erro ao enviar os dados:', error.response ? error.response.data : error.message);
    }
    window.location.href = '/login'; // Redireciona para a página inicial após o envio
  };

  return (
    <div className='register-container'>
      <form className='register-box' onSubmit={handleSubmit}>
        <h1>Register</h1>

        <div className='n-input'>
          <label htmlFor="nome_completo">Nome</label>
          <input 
            className='box' 
            type="text" 
            id="nome_completo" 
            name="nome_completo" 
            value={formData.nome_completo} 
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
          <label htmlFor="idade">Idade</label>
          <input 
            className='box' 
            type="number" 
            id="idade" 
            name="idade" 
            value={formData.idade} 
            onChange={handleChange} 
            required 
            min="0"
          />
        </div>

        <div className='n-input'>
          <label htmlFor="morada">Morada</label>
          <input 
            className='box' 
            type="text" 
            id="morada" 
            name="morada" 
            value={formData.morada} 
            onChange={handleChange} 
            required 
          />
        </div>

        <div className='n-input'>
          <label htmlFor="observacoes">Observações</label>
          <input 
            className='box' 
            type="text" 
            id="observacoes" 
            name="observacoes" 
            value={formData.observacoes} 
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
};

export default Register;
