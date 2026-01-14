// src/App.jsx
import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Login from "./pages/login/login";
import Inventario from "./pages/inventario/inventario";
import AdminPage from "./pages/admin/adminPage";
import MeseroPage from "./pages/mesero/MeseroPage";
import CajeroPage from "./pages/cajero/CajeroPage";
import CrearUsuario from "./pages/admin/CrearUsuario";
import CrearPedido from "./pages/pedidos/CrearPedido";
import VerPedidos from "./pages/pedidos/VerPedidos";

function App() {
  return (
    <Router>
      <Routes>
        {/* Ruta principal: Login */}
        <Route path="/" element={<Login />} />

        {/* Rutas según roles */}
        <Route path="/admin" element={<AdminPage />} />
        <Route path="/mesero" element={<MeseroPage />} />
        <Route path="/cajero" element={<CajeroPage />} />

        {/* Inventario */}
        <Route path="/inventario" element={<Inventario />} />
        {/*creacion de usuarios */}
        <Route path="/crear-usuario" element={<CrearUsuario />} />

        <Route path="/crear-pedido" element={<CrearPedido />} />
        <Route path="/ver-pedidos" element={<VerPedidos />} />


      </Routes>
    </Router>
  );
}

export default App;
