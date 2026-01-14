import { useEffect, useState } from "react";

function Inventario() {
  const [productos, setProductos] = useState([]);
  const [form, setForm] = useState({
    nombre: "",
    cantidad_nominal: "",
    unidad: "",
    precio: "",
    stock: "",
  });
  const [editando, setEditando] = useState(null);
  const [error, setError] = useState("");

  // JWT token
  const token = localStorage.getItem("token");

  // -------------------------------
  // Cargar productos
  // -------------------------------
  const cargarProductos = async () => {
    if (!token) {
      setError("No hay token. Inicia sesión.");
      return;
    }

    try {
      const res = await fetch("http://127.0.0.1:8000/api/productos/", {
        headers: { Authorization: `Bearer ${token}` }, // 🔥 FIX REAL
      });

      console.log("STATUS:", res.status);

      // Si falla la autenticación
      if (res.status === 401) {
        setError("Token inválido o expirado. Vuelve a iniciar sesión.");
        return;
      }

      const data = await res.json();
      console.log("DATA:", data);

      if (!res.ok) throw new Error();

      setProductos(data);
    } catch (err) {
      console.error(err);
      setError("No se pudieron cargar los productos");
    }
  };

  useEffect(() => {
    cargarProductos();
  }, []);

  // -------------------------------
  // Manejo del formulario
  // -------------------------------
  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  // -------------------------------
  // Crear o actualizar producto
  // -------------------------------
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    const method = editando ? "PUT" : "POST";
    const url = editando
      ? `http://127.0.0.1:8000/api/productos/${editando}/`
      : "http://127.0.0.1:8000/api/productos/";

    try {
      const res = await fetch(url, {
        method,
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`, // 🔥 FIX REAL
        },
        body: JSON.stringify(form),
      });

      if (!res.ok) throw new Error();

      setForm({
        nombre: "",
        cantidad_nominal: "",
        unidad: "",
        precio: "",
        stock: "",
      });

      setEditando(null);
      cargarProductos();
    } catch (err) {
      console.error(err);
      setError("Error al guardar el producto");
    }
  };

  // -------------------------------
  // Eliminar producto
  // -------------------------------
  const eliminarProducto = async (id) => {
    if (!window.confirm("¿Seguro que quieres eliminar este producto?")) return;

    try {
      await fetch(`http://127.0.0.1:8000/api/productos/${id}/`, {
        method: "DELETE",
        headers: { Authorization: `Bearer ${token}` },
      });

      cargarProductos();
    } catch {
      setError("Error al eliminar producto");
    }
  };

  // -------------------------------
  // Editar producto
  // -------------------------------
  const editarProducto = (p) => {
    setForm({
      nombre: p.nombre,
      cantidad_nominal: p.cantidad_nominal,
      unidad: p.unidad,
      precio: p.precio,
      stock: p.stock,
    });
    setEditando(p.id);
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>Inventario</h1>

      {/* Formulario */}
      <form
        onSubmit={handleSubmit}
        style={{
          display: "flex",
          gap: "10px",
          marginBottom: "20px",
          flexWrap: "wrap",
        }}
      >
        <input name="nombre" placeholder="Nombre" value={form.nombre} onChange={handleChange} required />
        <input name="cantidad_nominal" placeholder="Cantidad nominal" value={form.cantidad_nominal} onChange={handleChange} required />
        <input name="unidad" placeholder="Unidad" value={form.unidad} onChange={handleChange} required />
        <input name="precio" placeholder="Precio" value={form.precio} onChange={handleChange} required />
        <input name="stock" placeholder="Stock" value={form.stock} onChange={handleChange} required />

        <button
          type="submit"
          style={{
            backgroundColor: "#2563eb",
            color: "white",
            padding: "5px 10px",
            border: "none",
            borderRadius: "5px",
          }}
        >
          {editando ? "Actualizar" : "Crear"}
        </button>

        {editando && (
          <button
            type="button"
            onClick={() => {
              setForm({ nombre: "", cantidad_nominal: "", unidad: "", precio: "", stock: "" });
              setEditando(null);
            }}
            style={{
              backgroundColor: "#6b7280",
              color: "white",
              padding: "5px 10px",
              border: "none",
              borderRadius: "5px",
            }}
          >
            Cancelar
          </button>
        )}
      </form>

      {/* Tabla */}
      {error && <p style={{ color: "red" }}>{error}</p>}

      <table border="1" cellPadding="10" style={{ marginTop: "20px", width: "100%", borderCollapse: "collapse" }}>
        <thead style={{ background: "#f3f4f6" }}>
          <tr>
            <th>ID</th>
            <th>Nombre</th>
            <th>Cantidad Nominal</th>
            <th>Unidad</th>
            <th>Precio</th>
            <th>Stock</th>
            <th>Acciones</th>
          </tr>
        </thead>

        <tbody>
          {productos.map((p) => (
            <tr key={p.id}>
              <td>{p.id}</td>
              <td>{p.nombre}</td>
              <td>{p.cantidad_nominal}</td>
              <td>{p.unidad}</td>
              <td>{p.precio}</td>
              <td>{p.stock}</td>
              <td>
                <button
                  onClick={() => editarProducto(p)}
                  style={{
                    backgroundColor: "#facc15",
                    border: "none",
                    padding: "4px 8px",
                    marginRight: "6px",
                    borderRadius: "4px",
                  }}
                >
                  Editar
                </button>
                <button
                  onClick={() => eliminarProducto(p.id)}
                  style={{
                    backgroundColor: "#dc2626",
                    color: "white",
                    border: "none",
                    padding: "4px 8px",
                    borderRadius: "4px",
                  }}
                >
                  Eliminar
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Inventario;
