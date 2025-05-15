import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
const SidebarMenu = () => {
  const [isMenuActive, setIsMenuActive] = useState(false);
  const navigate = useNavigate();

  const toggleMenu = () => {
    setIsMenuActive(!isMenuActive);
  };

  useEffect(() => {
    const handleClickOutside = (e) => {
      if (!e.target.closest('.sidebar') && !e.target.closest('.menu-button')) {
        setIsMenuActive(false);
      }
    };

    document.addEventListener('click', handleClickOutside);
    return () => {
      document.removeEventListener('click', handleClickOutside);
    };
  }, []);

  const handleNavigation = (tipoId) => {
    navigate(`/produtos/${tipoId}`);
    setIsMenuActive(false);
  };

  return (
    <>
      <div className="menu-button" onClick={toggleMenu}>
        <div className="menu-text">Menu</div>
      </div>

      {isMenuActive && (
        <div className="sidebar active">
          <div className="overlay" onClick={() => setIsMenuActive(false)}></div>
          <ul>
            <li onClick={() => handleNavigation(1)}>Bikinis</li>
            <li onClick={() => handleNavigation(2)}>Sandálias</li>
            <li onClick={() => handleNavigation(3)}>Óculos de sol</li>
            <li onClick={() => handleNavigation(4)}>Pareos</li>
          </ul>
        </div>
      )}
    </>
  );
};

export default SidebarMenu;