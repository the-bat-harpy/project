import axios from 'axios';

export const handleLoginOrSignup = async (email, password) => {
  try {
    let response = await axios.post('http://127.0.0.1:8000/api/login/', {
      username: email,
      password: password
    });

    if (response.status === 200) {
      console.log('Login bem-sucedido:', response.data);
      localStorage.setItem('auth_token', response.data.token);
      localStorage.setItem('user_data', JSON.stringify({
        email,
        username: email.split('@')[0]
      }));
      return true;
    }
  } catch (error) {
    if (error.response && error.response.status === 401) {
      console.log('Login falhou. Tentando registrar novo usuário.');
      try {
        let signupResponse = await axios.post('http://127.0.0.1:8000/api/signup/', {
          email: email,
          password: password
        });

        if (signupResponse.status === 201) {
          console.log('Sign-in bem-sucedido:', signupResponse.data);
          localStorage.setItem('auth_token', signupResponse.data.token);
          localStorage.setItem('user_data', JSON.stringify({
            email,
            username: email.split('@')[0]
          }));
          return true;
        }
      } catch (signupError) {
        console.error('Erro ao tentar registrar o user:', signupError.response ? signupError.response.data : signupError.message);
        alert('Erro ao registrar user.');
      }
    } else {
      console.error('Erro desconhecido ao tentar fazer login:', error.response ? error.response.data : error.message);
      alert('Erro desconhecido ao tentar fazer login');
    }
  }

  return false;
};