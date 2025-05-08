import './Styles.css';
import { useEffect, useState } from 'react';
import { handleLoginOrSignup } from './Auth'; // Importe a função de login/signup

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false); // Estado para autenticação

  // Função de logout
  const logout = async () => {
    try {
      // Limpa o token de autenticação
      localStorage.removeItem('auth_token');
      setIsAuthenticated(false); // Atualiza o estado de autenticação para false
      alert('Logout efetuado com sucesso!');
    } catch (err) {
      console.error('Erro ao fazer logout:', err);
      alert('Erro de rede ao tentar fazer logout.');
    }
  };

  useEffect(() => {
    // Verifica se o token de autenticação está presente no localStorage
    const token = localStorage.getItem('auth_token');
    if (token) {
      setIsAuthenticated(true);
    }

    const searchToggle = document.getElementById('searchToggle');
    const searchInput = searchToggle.querySelector('input');

    searchToggle.addEventListener('click', (e) => {
      e.stopPropagation();
      const isExpanded = searchToggle.classList.contains('expanded');
      if (!isExpanded) {
        searchToggle.classList.remove('collapsed');
        searchToggle.classList.add('expanded');
        setTimeout(() => searchInput.focus(), 100);
      }
    });

    document.addEventListener('click', (e) => {
      if (!searchToggle.contains(e.target)) {
        searchToggle.classList.remove('expanded');
        searchToggle.classList.add('collapsed');
      }
    });

    const sidebarMenu = document.createElement('div');
    sidebarMenu.classList.add('sidebar');
    sidebarMenu.innerHTML = `
      <ul>
        <li>Bikinis</li>
        <li>Sandálias</li>
        <li>Toalhas</li>
        <li>Malas</li>
        <li>Óculos de sol</li>
        <li>Pareos</li>
        <li>Saias</li>
        <li>Vestidos</li>
      </ul>
    `;
    document.body.appendChild(sidebarMenu);

    const overlayMenu = document.createElement('div');
    overlayMenu.classList.add('overlay');
    document.body.appendChild(overlayMenu);

    const sidebarProfile = document.createElement('div');
    sidebarProfile.classList.add('sidebar-profile');
    sidebarProfile.innerHTML = `
      <h2 class="sidebar-title">Login/Registo</h2>
      <p class="sidebar-subtitle">Introduza o seu email</p>
      <input type="email" placeholder="Email" class="sidebar-input" />
      <input type="password" placeholder="Palavra-passe" class="sidebar-input" />
      <button class="sidebar-button" id="loginButton">Seguinte</button>
    `;
    document.body.appendChild(sidebarProfile);

    const overlayProfile = document.createElement('div');
    overlayProfile.classList.add('overlay');
    document.body.appendChild(overlayProfile);

    const menuButton = document.querySelector('.menu-button');
    if (menuButton) {
      menuButton.addEventListener('click', () => {
        sidebarMenu.classList.toggle('active');
        overlayMenu.classList.toggle('active');
      });
    }

    overlayMenu.addEventListener('click', () => {
      sidebarMenu.classList.remove('active');
      overlayMenu.classList.remove('active');
    });

    const profileButton = document.querySelector('.profile-button');
    if (profileButton) {
      profileButton.addEventListener('click', () => {
        sidebarProfile.classList.toggle('active');
        overlayProfile.classList.toggle('active');
      });
    }

    overlayProfile.addEventListener('click', () => {
      sidebarProfile.classList.remove('active');
      overlayProfile.classList.remove('active');
    });

    // Função de login
    const loginButton = document.getElementById('loginButton');
    if (loginButton) {
      loginButton.addEventListener('click', async () => {
        const email = sidebarProfile.querySelector('input[type="email"]').value;
        const password = sidebarProfile.querySelector('input[type="password"]').value;

        const success = await handleLoginOrSignup(email, password);
        if (success) {
          localStorage.setItem('auth_token', 'seu_token_de_autenticacao'); // Defina o token
          setIsAuthenticated(true); // Atualiza o estado de autenticação
          sidebarProfile.classList.remove('active');
          overlayProfile.classList.remove('active');
        }
      });
    }

    const cards = document.querySelectorAll('.card');
    const revealOnScroll = () => {
      const windowHeight = window.innerHeight;
      cards.forEach((card) => {
        const cardTop = card.getBoundingClientRect().top;
        if (cardTop < windowHeight - 100) {
          card.classList.add('visible');
        }
      });
    };
    window.addEventListener('scroll', revealOnScroll);
    revealOnScroll();

    return () => {
      sidebarMenu.remove();
      overlayMenu.remove();
      sidebarProfile.remove();
      overlayProfile.remove();
      window.removeEventListener('scroll', revealOnScroll);
    };
  }, []);

  return (
    <div className="homepage">
      <div className="hero-section">
        <video autoPlay loop muted playsInline className="hero-video">
          <source src="./images/video.mp4" type="video/mp4" />
          O seu navegador não suporta vídeo em HTML5.
        </video>
      </div>

      <h1 className="title">VERANI</h1>

      <div className="search-toggle collapsed" id="searchToggle">
        <div className="search-icon-img"></div>
        <div className="search-label">Pesquisar</div>
        <input type="text" placeholder="O que procuras?" />
      </div>

      <div className="menu-button">
        <div className="menu-text">Menu</div>
      </div>

      <div className="profile-button">
        <div className="profile-icon-img"></div>
      </div>
      <div className="cesto-button">
        <div className="cesto-icon-img"></div>
      </div>

      <div className="cards-container">
        <div className="card">
          <div className="card-title">Bikinis</div>
          <div className="card-image bikinis-image"></div>
        </div>

        <div className="card">
          <div className="card-title">Sandálias</div>
          <div className="card-image sandals-image"></div>
        </div>

        <div className="card">
          <div className="card-title">Óculos de Sol</div>
          <div className="card-image sunglasses-image"></div>
        </div>

        <div className="card">
          <div className="card-title">Toalhas</div>
          <div className="card-image towels-image"></div>
        </div>
      </div>

      {isAuthenticated && (
        <div className="authenticated-links">
          <button>Dados Pessoais</button>
          <button>Minhas Encomendas</button>

          {/* Botão de Logout */}
          <button onClick={logout} className="logout-button">
            Logout
          </button>
        </div>
      )}
    </div>
  );
}

export default App;
