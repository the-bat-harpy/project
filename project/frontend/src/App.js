import './Styles.css';

function App() {
  return (
    <div className="homepage">
      <div className="hero-section"></div>
      <h1 className="title">VERANI</h1>

      <div className="search-bar">
        <div className="search-icon"></div>
        <div className="search-text">Pesquisar</div>
      </div>

      <div className="menu-button">
        <div className="menu-text">Menu</div>
      </div>

      {}
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
