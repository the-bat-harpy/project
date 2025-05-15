import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Profile from './Profile';
import { AuthProvider } from './AuthContext';
import SidebarMenu from './MenuSB';
import CestoWishlistSB from './CestoWishlistSB';
import ProfileSB from './ProfileSB';
import ProdutosPage from './Produtos.js'
import FinalizarCompra from './FinalizarCompra.js'

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <AuthProvider>
      <BrowserRouter>
        <SidebarMenu />
        <CestoWishlistSB />
        <ProfileSB />
        <Routes>
          <Route path="/" element={<App />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/produtos/:tipoId" element={<ProdutosPage />} />
            <Route path="/finalizar-compra" element={<FinalizarCompra />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  </React.StrictMode>
);

reportWebVitals();
