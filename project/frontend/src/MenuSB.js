import { useEffect } from 'react';

const SidebarMenu = () => {
  useEffect(() => {
    // SIDEBAR MENU
    const sidebarMenu = document.createElement('div');
    sidebarMenu.classList.add('sidebar');
    sidebarMenu.innerHTML = `
      <ul>
        <li>Bikinis</li>
        <li>Sandálias</li>
        <li>Toalhas</li>
        <li>Malas</li>
        <li>Óculos de sol</li>
        <li>Pareos</li>
        <li>Saias</li>
        <li>Vestidos</li>
      </ul>
    `;
    document.body.appendChild(sidebarMenu);

    const overlayMenu = document.createElement('div');
    overlayMenu.classList.add('overlay');
    document.body.appendChild(overlayMenu);

    overlayMenu.addEventListener('click', () => {
      sidebarMenu.classList.remove('active');
      overlayMenu.classList.remove('active');
    });

    document.querySelector('.menu-button')?.addEventListener('click', () => {
      sidebarMenu.classList.add('active');
      overlayMenu.classList.add('active');
    });

    return () => {
      sidebarMenu.remove();
      overlayMenu.remove();
    };
  }, []);

  return null;
};

export default SidebarMenu;
