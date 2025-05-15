import { useState } from 'react';
import SidebarMenu from './MenuSB';
import SearchBar from './SearchBar';
import ProfileSidebar from './ProfileSB';
import CestoWishlist from './CestoWishlistSB';

function Header({ isAuthenticated, setIsAuthenticated, logout }) {
  const [isProfileActive, setIsProfileActive] = useState(false);
  const [isCestoActive, setIsCestoActive] = useState(false);
  const [isWishlistActive, setIsWishlistActive] = useState(false);

  return (
    <header className="header">
      <SidebarMenu />

      <div className="search-bar">
        <SearchBar />
      </div>

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

      <CestoWishlist
        isCestoActive={isCestoActive}
        isWishlistActive={isWishlistActive}
        close={() => {
          setIsCestoActive(false);
          setIsWishlistActive(false);
        }}
      />
    </header>
  );
}

export default Header;
