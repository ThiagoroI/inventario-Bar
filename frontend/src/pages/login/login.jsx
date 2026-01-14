import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setError("");

    try {
      // 1️⃣ LOGIN → Obtener token
      const response = await fetch("http://127.0.0.1:8000/api/login/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
      });

      const data = await response.json();

      if (!response.ok) {
        setError(data.detail || "Usuario o contraseña incorrectos");
        return;
      }

      // 2️⃣ Guardar tokens
      localStorage.setItem("access", data.access);
      localStorage.setItem("refresh", data.refresh);

      // 3️⃣ Obtener datos del usuario desde /user-info/
      const userRes = await fetch("http://127.0.0.1:8000/api/user-info/", {
        method: "GET",
        headers: {
          "Authorization": `Bearer ${data.access}`,
        },
      });

      const userData = await userRes.json();

      if (!userRes.ok) {
        setError("No se pudo obtener la información del usuario.");
        return;
      }

      // Guardar usuario en localStorage
      localStorage.setItem("user", JSON.stringify(userData));

      const userRole = userData.role;

      // 4️⃣ Redireccionar por rol
      switch (userRole) {
        case "admin":
          navigate("/admin");
          break;
        case "mesero":
          navigate("/mesero");
          break;
        case "cajero":
          navigate("/cajero");
          break;
        default:
          setError("Rol no reconocido");
      }
    } catch (err) {
      setError("Error al conectar con el servidor");
      console.error(err);
    }
  };

  return (
    <div
      style={{
        maxWidth: "400px",
        margin: "60px auto",
        padding: "20px",
        border: "1px solid #ddd",
        borderRadius: "10px",
        boxShadow: "0 2px 5px rgba(0,0,0,0.1)",
      }}
    >
      <h2 style={{ textAlign: "center" }}>Iniciar sesión</h2>

      <form onSubmit={handleLogin}>
        <div style={{ marginBottom: "15px" }}>
          <label>Usuario:</label>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
            style={{
              width: "100%",
              padding: "8px",
              borderRadius: "5px",
              border: "1px solid #ccc",
            }}
          />
        </div>

        <div style={{ marginBottom: "15px" }}>
          <label>Contraseña:</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            style={{
              width: "100%",
              padding: "8px",
              borderRadius: "5px",
              border: "1px solid #ccc",
            }}
          />
        </div>

        <button
          type="submit"
          style={{
            width: "100%",
            padding: "10px",
            backgroundColor: "#007bff",
            color: "#fff",
            border: "none",
            borderRadius: "5px",
            cursor: "pointer",
          }}
        >
          Entrar
        </button>
      </form>

      {error && (
        <p style={{ color: "red", marginTop: "15px", textAlign: "center" }}>
          {error}
        </p>
      )}
    </div>
  );
}
