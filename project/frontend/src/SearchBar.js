import { useEffect } from 'react';

function SearchBar() {
  useEffect(() => {
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

    return () => {
      searchToggle?.removeEventListener('click', () => {});
      document.removeEventListener('click', () => {});
    };
  }, []);

  return (
    <>
      <div className="search-bar">
        <div className="search-text">Pesquisar</div>
      </div>

      <div className="search-toggle collapsed" id="searchToggle">
        <div className="search-icon-img"></div>
        <div className="search-label">Pesquisar</div>
        <input type="text" placeholder="O que procuras?" />
      </div>
    </>
  );
}

export default SearchBar;
