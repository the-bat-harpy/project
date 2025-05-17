import axios from 'axios';

export const handleLoginOrSignup = async (email, password) => {
  try {
    const response = await axios.post(
      'http://localhost:8000/api/login/',
      { username: email, password },
      { withCredentials: true }
    );

    if (response.status === 200) {
      console.log('Login bem-sucedido:', response.data);
      const userData = {
        email,
        username: email.split('@')[0],
        is_superuser: response.data.is_superuser || false,
      };
      localStorage.setItem('user_data', JSON.stringify(userData));
      return true;
    }
  } catch (error) {
    if (error.response && error.response.status === 401) {
      try {
        const signupResponse = await axios.post(
          'http://localhost:8000/api/signup/',
          { email, password },
          { withCredentials: true }
        );

        if (signupResponse.status === 201) {
          console.log('Signup bem-sucedido:', signupResponse.data);
          const userData = {
            email,
            username: email.split('@')[0],
            is_superuser: false,
          };
          localStorage.setItem('user_data', JSON.stringify(userData));
          return true;
        }
      } catch (signupError) {
        alert('Erro ao registrar cliente.');
      }
    } else {
      alert('Erro no login.');
    }
  }
  return false;
};
