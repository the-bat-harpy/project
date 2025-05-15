import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

function SearchBar({ hideSearchIcon = false }) {
  const [term, setTerm] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const searchToggle = document.getElementById('searchToggle');
    const searchInput = searchToggle?.querySelector('input');

    if (!searchToggle) return;

    const handleToggleClick = (e) => {
      e.stopPropagation();
      const isExpanded = searchToggle.classList.contains('expanded');
      if (!isExpanded) {
        searchToggle.classList.remove('collapsed');
        searchToggle.classList.add('expanded');
        setTimeout(() => searchInput?.focus(), 100);
      }
    };

    const handleDocumentClick = (e) => {
      if (!searchToggle.contains(e.target)) {
        searchToggle.classList.remove('expanded');
        searchToggle.classList.add('collapsed');
      }
    };

    searchToggle.addEventListener('click', handleToggleClick);
    document.addEventListener('click', handleDocumentClick);

    return () => {
      searchToggle.removeEventListener('click', handleToggleClick);
      document.removeEventListener('click', handleDocumentClick);
    };
  }, []);

  const handleKeyDown = async (e) => {
    if (e.key === 'Enter') {
        console.log('Enter pressionado! Termo:', term);
      try {
const response = await axios.get(`http://localhost:8000/api/produtos/pesquisar?termo=${term}`);
        navigate('/pesquisa', { state: { resultados: response.data, termo: term } });
      } catch (error) {
        console.error("Erro ao pesquisar:", error);
      }
    }
  };

  return (
    <>
      {!hideSearchIcon && (
        <div className="search-bar">
          <div className="search-text">Pesquisar</div>
        </div>
      )}

<div className={`search-toggle ${hideSearchIcon ? 'collapsed' : ''}`} id="searchToggle">
        {!hideSearchIcon && <div className="search-icon-img"></div>}
        {!hideSearchIcon && <div className="search-label">Pesquisar</div>}
        <input
          type="text"
          placeholder="O que procuras?"
          value={term}
          onChange={(e) => setTerm(e.target.value)}
          onKeyDown={handleKeyDown}
        />
      </div>
    </>
  );
}

export default SearchBar;