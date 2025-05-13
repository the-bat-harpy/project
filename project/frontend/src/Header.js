import { useState } from 'react';
import SidebarMenu from './MenuSB';
import SearchBar from './SearchBar';
import ProfileSidebar from './ProfileSB';

function Header({
  isAuthenticated,
  setIsAuthenticated,
  logout,
  setIsCestoActive,
  setIsWishlistActive,
}) {
  const [isProfileActive, setIsProfileActive] = useState(false);

  return (
    <header className="header">
      <div className="menu-button">
        <div className="menu-text">Menu</div>
      </div>

      <SidebarMenu />

      <div className="search-bar">
        <div className="search-text">Pesquisar</div>
      </div>

      <SearchBar />

      <div className="profile-button" onClick={() => setIsProfileActive(true)}>
        <div className="profile-icon-img"></div>
      </div>

      <ProfileSidebar
        logout={logout}
        isAuthenticated={isAuthenticated}
        setIsAuthenticated={setIsAuthenticated}
        isProfileActive={isProfileActive}
        setIsProfileActive={setIsProfileActive}
      />

      <div className="cesto-button" onClick={() => setIsCestoActive(true)}>
        <div className="cesto-icon-img"></div>
      </div>

      <div className="wishlist-button" onClick={() => setIsWishlistActive(true)}>
        <div className="wishlist-icon-img"></div>
      </div>
    </header>
  );
}

export default Header;
