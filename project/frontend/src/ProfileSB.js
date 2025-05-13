import { useEffect } from 'react';
import { handleLoginOrSignup } from './Auth';

function ProfileSidebar({ logout, isAuthenticated, setIsAuthenticated }) {
  useEffect(() => {
    const sidebarProfile = document.createElement('div');
    sidebarProfile.classList.add('sidebar-profile');
    document.body.appendChild(sidebarProfile);

    const overlayProfile = document.createElement('div');
    overlayProfile.classList.add('overlay');
    document.body.appendChild(overlayProfile);

    const renderLoginForm = () => {
      sidebarProfile.innerHTML = `
        <button class="close-profile" aria-label="Fechar">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" stroke="currentColor"
            stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-x">
            <line x1="18" y1="6" x2="6" y2="18" />
            <line x1="6" y1="6" x2="18" y2="18" />
          </svg>
        </button>
        <h2 class="sidebar-title">Login/Registo</h2>
        <p class="sidebar-subtitle">Introduza o seu email</p>
        <input type="email" placeholder="Email" class="sidebar-input" />
        <input type="password" placeholder="Palavra-passe" class="sidebar-input" />
        <button class="sidebar-button" id="loginButton">Seguinte</button>
      `;

      sidebarProfile.querySelector('.close-profile')?.addEventListener('click', () => {
        sidebarProfile.classList.remove('active');
        overlayProfile.classList.remove('active');
      });

      document.getElementById('loginButton')?.addEventListener('click', async () => {
        const email = sidebarProfile.querySelector('input[type="email"]').value;
        const password = sidebarProfile.querySelector('input[type="password"]').value;

        const success = await handleLoginOrSignup(email, password);
        if (success) {
          setIsAuthenticated(true);
          window.location.reload();
        }
      });
    };

    const token = localStorage.getItem('auth_token');
    if (!token) {
      renderLoginForm();
    } else {
      const userData = JSON.parse(localStorage.getItem('user_data')) || {};
      const greetingName = userData.username || userData.email;

      sidebarProfile.innerHTML = `
        <div class="sidebar-logged-in">
          <h2 class="sidebar-title">Olá, ${greetingName}</h2>
          <div class="sidebar-actions">
            <button class="sidebar-nav-button" id="gotoPage1">Dados Pessoais</button>
            <button class="sidebar-nav-button" id="gotoPage2">Minhas Encomendas</button>
            <button class="sidebar-button logout-button">Terminar Sessão</button>
          </div>
        </div>
      `;

      sidebarProfile.querySelector('.logout-button')?.addEventListener('click', logout);
      document.getElementById('gotoPage1')?.addEventListener('click', () => (window.location.href = '/pagina1'));
      document.getElementById('gotoPage2')?.addEventListener('click', () => (window.location.href = '/pagina2'));
    }

    const profileBtn = document.querySelector('.profile-button');
    profileBtn?.addEventListener('click', () => {
      sidebarProfile.classList.toggle('active');
      overlayProfile.classList.toggle('active');
    });

    overlayProfile?.addEventListener('click', () => {
      sidebarProfile.classList.remove('active');
      overlayProfile.classList.remove('active');
    });

    return () => {
      sidebarProfile.remove();
      overlayProfile.remove();
    };
  }, [logout, isAuthenticated, setIsAuthenticated]);

  return null;
}

export default ProfileSidebar;
