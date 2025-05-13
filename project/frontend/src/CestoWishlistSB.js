import { useState, useEffect } from 'react';
import './Styles.css';

const CestoWishlist = () => {
  const [isSidebarActive, setIsSidebarActive] = useState(false);
  const [activeTab, setActiveTab] = useState('cesto');

  const cestoContent = (
    <div className="sidebar-cesto-body">
      <div className="cesto-item">
        <img src="./images/top-biquini.png" alt="Top biquini" />
        <div>
          <p>Top biquini tie-die</p>
          <p>15,99 €</p>
          <p>1 un. | M | Preto</p>
        </div>
      </div>
      <div className="cesto-item">
        <img src="./images/cuecas-biquini.png" alt="Cuecas biquini" />
        <div>
          <p>Cuecas biquini tie-die</p>
          <p>12,99 €</p>
          <p>1 un. | M | Preto</p>
        </div>
      </div>
      <div className="cesto-total">
        <strong>Total</strong>
        <span>27,98 €</span>
      </div>
      <button className="finalizar-encomenda">Finalizar encomenda</button>
    </div>
  );

  const wishlistContent = (
    <div className="sidebar-cesto-body">
      <div className="cesto-item">
        <p>Lista de desejos vazia</p>
      </div>
    </div>
  );

  useEffect(() => {
    const closeSidebar = () => {
      setIsSidebarActive(false);
    };
    const overlayCesto = document.querySelector('.overlay');
    overlayCesto?.addEventListener('click', closeSidebar);
    return () => {
      overlayCesto?.removeEventListener('click', closeSidebar);
    };
  }, []);

  return (
    <div>
      {}
      <div className="cesto-button" onClick={() => setIsSidebarActive(true)}>
        <div className="cesto-icon-img"></div>
      </div>

      {}
      <div className={`sidebar-cesto ${isSidebarActive ? 'active' : ''}`}>
        <div className="sidebar-cesto-header">
          <div
            className={`header-left ${activeTab === 'cesto' ? 'active-title' : ''}`}
            onClick={() => setActiveTab('cesto')}
          >
            Cesto
          </div>
          <div
            className={`header-right ${activeTab === 'wishlist' ? 'active-title' : ''}`}
            onClick={() => setActiveTab('wishlist')}
          >
            Wishlist
          </div>
          <button className="close-cesto" aria-label="Fechar" onClick={() => setIsSidebarActive(false)}>
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" stroke="currentColor"
              strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="feather feather-x">
              <line x1="18" y1="6" x2="6" y2="18" />
              <line x1="6" y1="6" x2="18" y2="18" />
            </svg>
          </button>
        </div>
        <div className="sidebar-content">
          {activeTab === 'cesto' ? cestoContent : wishlistContent}
        </div>
      </div>
      {}
      <div className={`overlay ${isSidebarActive ? 'active' : ''}`} onClick={() => setIsSidebarActive(false)}></div>
    </div>
  );
};

export default CestoWishlist;
