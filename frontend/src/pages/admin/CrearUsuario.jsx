import React, { useState } from "react";

export default function CrearUsuario() {
  const [formData, setFormData] = useState({
    username: "",
    password: "",
    email: "",
    role: "mesero",
  });
  const [mensaje, setMensaje] = useState("");
  const [error, setError] = useState("");

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMensaje("");
    setError("");

    try {
      const token = localStorage.getItem("token");
      if (!token) {
        setError("No hay token de autenticación. Inicia sesión nuevamente.");
        return;
      }

      const response = await fetch("http://127.0.0.1:8000/api/usuarios/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Token ${token}`,
        },
        body: JSON.stringify(formData),
      });

      // Intenta leer la respuesta como JSON
      let data;
      try {
        data = await response.json();
      } catch {
        data = {};
      }

      if (!response.ok) {
        setError(
          data.detail ||
            data.error ||
            "Error al crear el usuario (verifica permisos o datos)."
        );
        return;
      }

      setMensaje("✅ Usuario creado exitosamente.");
      setFormData({
        username: "",
        password: "",
        email: "",
        role: "mesero",
      });
    } catch (err) {
      console.error("Error al conectar con el servidor:", err);
      setError("Error al conectar con el servidor.");
    }
  };

  return (
    <div className="max-w-md mx-auto mt-12 p-6 bg-white shadow-md rounded-lg">
      <h2 className="text-2xl font-bold mb-4">Crear Nuevo Usuario</h2>

      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        <input
          name="username"
          placeholder="Nombre de usuario"
          value={formData.username}
          onChange={handleChange}
          className="border p-2 rounded"
          required
        />

        <input
          name="email"
          type="email"
          placeholder="Correo electrónico"
          value={formData.email}
          onChange={handleChange}
          className="border p-2 rounded"
          required
        />

        <input
          name="password"
          type="password"
          placeholder="Contraseña"
          value={formData.password}
          onChange={handleChange}
          className="border p-2 rounded"
          required
        />

        <select
          name="role"
          value={formData.role}
          onChange={handleChange}
          className="border p-2 rounded"
        >
          <option value="admin">Administrador</option>
          <option value="mesero">Mesero</option>
          <option value="cajero">Cajero</option>
        </select>

        <button
          type="submit"
          className="bg-blue-600 text-white p-2 rounded hover:bg-blue-700 transition"
        >
          Crear Usuario
        </button>
      </form>

      {mensaje && <p className="text-green-600 mt-3">{mensaje}</p>}
      {error && <p className="text-red-600 mt-3">{error}</p>}
    </div>
  );
}
