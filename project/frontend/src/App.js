import './Styles.css';
import { useEffect, useState } from 'react';
import { handleLoginOrSignup } from './Auth';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  const logout = () => {
    localStorage.removeItem('auth_token');
    localStorage.removeItem('user_data');
    setIsAuthenticated(false);
    alert('Logout efetuado com sucesso!');
    window.location.reload();
  };

  useEffect(() => {
    const token = localStorage.getItem('auth_token');
    if (token) setIsAuthenticated(true);

    const searchToggle = document.getElementById('searchToggle');
    const searchInput = searchToggle?.querySelector('input');

    searchToggle?.addEventListener('click', (e) => {
      e.stopPropagation();
      const isExpanded = searchToggle.classList.contains('expanded');
      if (!isExpanded) {
        searchToggle.classList.remove('collapsed');
        searchToggle.classList.add('expanded');
        setTimeout(() => searchInput?.focus(), 100);
      }
    });

    document.addEventListener('click', (e) => {
      if (!searchToggle?.contains(e.target)) {
        searchToggle?.classList.remove('expanded');
        searchToggle?.classList.add('collapsed');
      }
    });

    // SIDEBAR MENU
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

    overlayMenu.addEventListener('click', () => {
      sidebarMenu.classList.remove('active');
      overlayMenu.classList.remove('active');
    });
document.querySelector('.menu-button')?.addEventListener('click', () => {
  sidebarMenu.classList.add('active');
  overlayMenu.classList.add('active');
});

    // SIDEBAR CESTO
    const sidebarCesto = document.createElement('div');
    sidebarCesto.classList.add('sidebar-cesto');

    const overlayCesto = document.createElement('div');
    overlayCesto.classList.add('overlay');

    const cestoContent = `
      <div class="sidebar-cesto-body">
        <div class="cesto-item">
          <img src="./images/top-biquini.png" alt="Top biquini" />
          <div>
            <p>Top biquini tie-die</p>
            <p>15,99 €</p>
            <p>1 un. | M | Preto</p>
          </div>
        </div>
        <div class="cesto-item">
          <img src="./images/cuecas-biquini.png" alt="Cuecas biquini" />
          <div>
            <p>Cuecas biquini tie-die</p>
            <p>12,99 €</p>
            <p>1 un. | M | Preto</p>
          </div>
        </div>
        <div class="cesto-total">
          <strong>Total</strong>
          <span>27,98 €</span>
        </div>
        <button class="finalizar-encomenda">Finalizar encomenda</button>
      </div>
    `;

    const wishlistContent = `
      <div class="sidebar-cesto-body">
        <div class="cesto-item"></div>
      </div>
    `;

    sidebarCesto.innerHTML = `
      <div class="sidebar-cesto-header">
        <div class="header-left active-title" id="cestoTitle">Cesto</div>
        <div class="header-right" id="wishlistTitle">Wishlist</div>
        <button class="close-cesto" aria-label="Fechar">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" stroke="currentColor"
            stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-x">
            <line x1="18" y1="6" x2="6" y2="18" />
            <line x1="6" y1="6" x2="18" y2="18" />
          </svg>
        </button>
      </div>
      <div class="sidebar-content" id="sidebarContent">
        ${cestoContent}
      </div>
    `;

    document.body.appendChild(sidebarCesto);
    document.body.appendChild(overlayCesto);

    document.querySelector('.cesto-button')?.addEventListener('click', () => {
      sidebarCesto.classList.toggle('active');
      overlayCesto.classList.toggle('active');
    });

    sidebarCesto.querySelector('.close-cesto')?.addEventListener('click', () => {
      sidebarCesto.classList.remove('active');
      overlayCesto.classList.remove('active');
    });

    overlayCesto.addEventListener('click', () => {
      sidebarCesto.classList.remove('active');
      overlayCesto.classList.remove('active');
    });

    const cestoTitle = sidebarCesto.querySelector('#cestoTitle');
    const wishlistTitle = sidebarCesto.querySelector('#wishlistTitle');
    const sidebarContent = sidebarCesto.querySelector('#sidebarContent');

    cestoTitle?.addEventListener('click', () => {
      sidebarContent.innerHTML = cestoContent;
      cestoTitle.classList.add('active-title');
      wishlistTitle.classList.remove('active-title');
    });

    wishlistTitle?.addEventListener('click', () => {
      sidebarContent.innerHTML = wishlistContent;
      wishlistTitle.classList.add('active-title');
      cestoTitle.classList.remove('active-title');
    });

    // SIDEBAR PROFILE
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
        }
      });
    };

    if (!token) renderLoginForm();
    else {
      const userData = JSON.parse(localStorage.getItem('user_data')) || {};
      const greetingName = userData.username || userData.email || 'Utilizador';

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
      document.getElementById('gotoPage1')?.addEventListener('click', () => window.location.href = '/pagina1');
      document.getElementById('gotoPage2')?.addEventListener('click', () => window.location.href = '/pagina2');
    }

    document.querySelector('.profile-button')?.addEventListener('click', () => {
      sidebarProfile.classList.toggle('active');
      overlayProfile.classList.toggle('active');
    });

    overlayProfile.addEventListener('click', () => {
      sidebarProfile.classList.remove('active');
      overlayProfile.classList.remove('active');
    });

    // Scroll animation for cards
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
      sidebarCesto.remove();
      overlayCesto.remove();
      sidebarProfile.remove();
      overlayProfile.remove();
      sidebarMenu.remove();
      overlayMenu.remove();
      window.removeEventListener('scroll', revealOnScroll);
    };
  }, [isAuthenticated]);

  return (
    <div className="homepage">
      <div className="hero-section">
        <video autoPlay loop muted playsInline className="hero-video">
          <source src="./images/video.mp4" type="video/mp4" />
          O seu navegador não suporta vídeo em HTML5.
        </video>
      </div>

      <h1 className="title">VERANI</h1>

      <div className="search-bar">
        <div className="search-text">Pesquisar</div>
      </div>

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
    </div>
  );
}

export default App;
