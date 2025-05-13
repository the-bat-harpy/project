import './Styles.css';
import { useState, useEffect } from 'react';
import Header from './Header';
import CestoWishlist from './CestoWishlistSB';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isCestoActive, setIsCestoActive] = useState(false);
  const [isWishlistActive, setIsWishlistActive] = useState(false);

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

    // Animação de scroll nos cards
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

  return (
    <div className="homepage">
      <div className="hero-section">
        <video autoPlay loop muted playsInline className="hero-video">
          <source src="./images/video.mp4" type="video/mp4" />
          O seu navegador não suporta vídeo em HTML5.
        </video>
      </div>

      <h1 className="title">VERANI</h1>

      <Header
        isAuthenticated={isAuthenticated}
        setIsAuthenticated={setIsAuthenticated}
        logout={logout}
        setIsCestoActive={setIsCestoActive}
        setIsWishlistActive={setIsWishlistActive}
      />

      <CestoWishlist
        isCestoActive={isCestoActive}
        isWishlistActive={isWishlistActive}
        close={() => {
          setIsCestoActive(false);
          setIsWishlistActive(false);
        }}
      />

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
