import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { handleLoginOrSignup } from './Auth';
import { useAuth } from './AuthContext';

function ProfileSidebar() {
  const [isSidebarActive, setIsSidebarActive] = useState(false);
    const [is_superuser, setIsSuperuser] = useState(false);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const { isAuthenticated, setIsAuthenticated, logout } = useAuth();

  useEffect(() => {
    const profileBtn = document.querySelector('.profile-button');
    const handleClick = () => setIsSidebarActive(!isSidebarActive);

    profileBtn?.addEventListener('click', handleClick);

    return () => {
      profileBtn?.removeEventListener('click', handleClick);
    };
  }, [isSidebarActive]);

  const handleLogin = async () => {
    const success = await handleLoginOrSignup(email, password);
    if (success) {
      setIsAuthenticated(true);
      setIsSidebarActive(false);
        const userData = JSON.parse(localStorage.getItem('user_data'));
          setIsSuperuser(userData?.is_superuser || false);
     // window.location.reload();
    }
  };

  const handleNavigate = (path) => {
    setIsSidebarActive(false);
    navigate(path);
  };

  const userData = JSON.parse(localStorage.getItem('user_data')) || {};
  const greetingName = userData.username || userData.email;

  return (
    <>
      {isSidebarActive && (
        <>
          <div className="overlay" onClick={() => setIsSidebarActive(false)}></div>

          <div className="sidebar-profile active">
            <button
              className="close-profile"
              aria-label="Fechar"
              onClick={() => setIsSidebarActive(false)}
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none"
                   stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"
                   className="feather feather-x">
                <line x1="18" y1="6" x2="6" y2="18" />
                <line x1="6" y1="6" x2="18" y2="18" />
              </svg>
            </button>

            {!isAuthenticated ? (
              <>
                <h2 className="sidebar-title">Login/Registo</h2>
                <p className="sidebar-subtitle">Introduza o seu email</p>
                <input
                  type="email"
                  placeholder="Email"
                  className="sidebar-input"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                />
                <input
                  type="password"
                  placeholder="Palavra-passe"
                  className="sidebar-input"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                />
                <button className="sidebar-button" onClick={handleLogin}>Seguinte</button>
              </>
            ) : (
              <div className="sidebar-logged-in">
                <h2 className="sidebar-title">Olá, {greetingName}</h2>
                <div className="sidebar-actions">
                  <button className="sidebar-nav-button" onClick={() => handleNavigate('/profile')}>
                    Dados Pessoais
                  </button>
                  <button className="sidebar-nav-button" onClick={() => handleNavigate('/encomendas')}>
                    Minhas Encomendas
                  </button>
                  <button className="sidebar-button logout-button" onClick={logout}>
                    Terminar Sessão
                  </button>
                </div>
              </div>
            )}
          </div>
        </>
      )}
    </>
  );
}

export default ProfileSidebar;