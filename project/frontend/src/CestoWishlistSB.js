import { useState, useEffect } from 'react';
import './Styles.css';
import { useNavigate } from 'react-router-dom';

const CestoWishlist = () => {
  const [isSidebarActive, setIsSidebarActive] = useState(false);
  const [activeTab, setActiveTab] = useState('cesto');
  const [cestoProdutos, setCestoProdutos] = useState([]);
  const [wishlistProdutos, setWishlistProdutos] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    if (activeTab === 'cesto') {
      fetchCestoProdutos();
    } else {
      fetchWishlistProdutos();
    }
  }, [activeTab]);

  const fetchCestoProdutos = async () => {
    try {
      const response = await fetch('/api/cesto/', {
        credentials: 'include',
      });
      if (!response.ok) throw new Error('Erro ao carregar o cesto');
      const data = await response.json();
      setCestoProdutos(data);
    } catch (error) {
      console.error('Erro:', error);
    }
  };

  const fetchWishlistProdutos = async () => {
    try {
      const response = await fetch('/api/wishlist/', {
        credentials: 'include',
      });
      if (!response.ok) throw new Error('Erro ao carregar a wishlist');
      const data = await response.json();
      setWishlistProdutos(data);
    } catch (error) {
      console.error('Erro:', error);
    }
  };

  const calcularTotal = () => {
    return cestoProdutos
      .reduce((acc, produto) => acc + parseFloat(produto.preco) * produto.quantidade, 0)
      .toFixed(2);
  };

  const cestoContent = (
    <div className="sidebar-cesto-body">
      {cestoProdutos.length === 0 ? (
        <div className="cesto-item">
          <p>Cesto vazio</p>
        </div>
      ) : (
        <>
          {cestoProdutos.map((produto) => (
            <div key={produto.id} className="cesto-item">
              <img src={produto.imagens.frontImg_url} alt={produto.nome} />
              <div>
                <p>{produto.nome}</p>
                <p>{produto.preco} €</p>
                <p>{produto.quantidade} un. | {produto.tamanho} | {produto.cor}</p>
              </div>
            </div>
          ))}
          <div className="cesto-total">
            <strong>Total</strong>
            <span>{calcularTotal()} €</span>
          </div>
          <button className="finalizar-encomenda" onClick={() => navigate('/finalizar-compra')}>
            Finalizar encomenda
          </button>
        </>
      )}
    </div>
  );

  const wishlistContent = (
    <div className="sidebar-cesto-body">
      {wishlistProdutos.length === 0 ? (
        <div className="cesto-item">
          <p>Lista de desejos vazia</p>
        </div>
      ) : (
        wishlistProdutos.map((produto) => (
          <div key={produto.id} className="cesto-item">
            <img src={produto.imagens.frontImg_url} alt={produto.nome} />
            <div>
              <p>{produto.nome}</p>
              <p>{produto.preco} €</p>
            </div>
          </div>
        ))
      )}
    </div>
  );

  useEffect(() => {
    const closeSidebar = () => setIsSidebarActive(false);
    const overlayCesto = document.querySelector('.overlay');
    overlayCesto?.addEventListener('click', closeSidebar);
    return () => {
      overlayCesto?.removeEventListener('click', closeSidebar);
    };
  }, []);

  return (
    <div>
      <div className="cesto-button" onClick={() => setIsSidebarActive(true)}>
        <div className="cesto-icon-img"></div>
      </div>

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

      <div className={`overlay ${isSidebarActive ? 'active' : ''}`} onClick={() => setIsSidebarActive(false)}></div>
    </div>
  );
};

export default CestoWishlist;
