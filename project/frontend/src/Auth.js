import axios from 'axios';

export const handleLoginOrSignup = async (email, password) => {
  try {


    let response = await axios.post(
      'http://localhost:8000/api/login/',
      {
        username: email,
        password: password,
      },
      {
        withCredentials: true,
      }
    );

    if (response.status === 200) {
      console.log('Login bem-sucedido:', response.data);
      localStorage.setItem('user_data', JSON.stringify({
        email,
        username: email.split('@')[0],
      }));
      return true;
    }
  } catch (error) {
    if (error.response && error.response.status === 401) {
      console.log('Login falhou. Tentando registrar novo cliente.');

      try {
        let signupResponse = await axios.post(
          'http://localhost:8000/api/signup/',
          {
            email,
            password,
          },
          {
            withCredentials: true,
          }
        );

        if (signupResponse.status === 201) {
          console.log('Signin bem-sucedido:', signupResponse.data);
          localStorage.setItem('user_data', JSON.stringify({
            email,
            username: email.split('@')[0],
          }));
          return true;
        }
      } catch (signupError) {
        console.error('Erro ao registrar:', signupError.response?.data || signupError.message);
        alert('Erro ao registrar cliente.');
      }
    } else {
      console.error('Erro no login:', error.response?.data || error.message);
      alert('Erro no login.');
    }
  }

  return false;
};
