import './Styles.css';
import { useEffect } from 'react';
import Header from './Header';
import { useNavigate } from 'react-router-dom';
import { useAuth } from './AuthContext';

function App() {
  const { isAuthenticated, logout } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
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
      window.removeEventListener('scroll', revealOnScroll);
    };
  }, []);

  const handleCardClick = (tipoId) => {
    navigate(`/produtos/${tipoId}`);
  };

  return (
    <div className="homepage">
      <div className="hero-section">
        <video autoPlay loop muted playsInline className="hero-video">
          <source src="./images/video.mp4" type="video/mp4" />
          O seu navegador não suporta vídeos em HTML5.
        </video>
      </div>

      <h1 className="title">VERANI</h1>

      <Header
        isAuthenticated={isAuthenticated}
        logout={logout}
      />

      <div className="cards-container">
        <div className="card" onClick={() => handleCardClick(1)}>
          <div className="card-title">Bikinis</div>
          <div className="card-image bikinis-image"></div>
        </div>
        <div className="card" onClick={() => handleCardClick(2)}>
          <div className="card-title">Sandálias</div>
          <div className="card-image sandals-image"></div>
        </div>
        <div className="card" onClick={() => handleCardClick(3)}>
          <div className="card-title">Óculos de Sol</div>
          <div className="card-image sunglasses-image"></div>
        </div>
        <div className="card" onClick={() => handleCardClick(4)}>
          <div className="card-title">Pareos</div>
          <div className="card-image pareo-image"></div>
        </div>
      </div>
    </div>
  );
}

export default App;
