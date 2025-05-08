export async function handleLoginOrSignup(email, password) {
  try {
    const loginRes = await fetch('http://localhost:8000/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username: email, password }),
    });

    if (loginRes.ok) {
      alert('Login efetuado com sucesso!');
      return true;  // Login bem-sucedido
    }

    const signupRes = await fetch('http://localhost:8000/signup', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username: email, password }),
    });

    if (signupRes.ok) {
      const retryLogin = await fetch('http://localhost:8000/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: email, password }),
      });

      if (retryLogin.ok) {
        alert('Conta criada e login efetuado com sucesso!');
        return true;  // Login após cadastro bem-sucedido
      } else {
        alert('Erro ao fazer login após signup.');
        return false;
      }
    } else {
      const data = await signupRes.json();
      alert(data.error || 'Erro ao criar conta.');
      return false;
    }
  } catch (err) {
    console.error('Erro de rede:', err);
    alert('Erro de rede.');
    return false;
  }
}
