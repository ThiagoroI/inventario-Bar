import React from "react";
import "./header.css"; // CSS específico del header

export default function Header({ onLogout }) {
  return (
    <header className="header-crear">
      <div className="logo-area-crear">
        <img src="/logo.png" alt="Logo" className="logo-img-crear" />
        <span className="logo-text-crear">Copa Nocturna</span>
      </div>

      <nav className="nav-crear">
        <a href="/crear-pedido" className="nav-btn">Crear Pedido</a>
        <a href="/crear-usuario" className="nav-btn">Crear Usuario</a>
        <a href="/inventario" className="nav-btn">Inventario</a>
        <a href="/pedidos" className="nav-btn ver-pedido-btn">Ver Pedido</a> {/* Apunta a VerPedidos.jsx */}
        <a
          href="#logout"
          className="nav-btn logout"
          onClick={(e) => {
            e.preventDefault();
            localStorage.removeItem("token");
            if (onLogout) onLogout();
          }}
        >
          Cerrar Sesión
        </a>
      </nav>
    </header>
  );
}
