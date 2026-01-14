import React, { useState, useEffect } from "react";
import Header from "../Header"; // Ajusta la ruta según tu estructura
import "./crearPedido.css";

export default function CrearPedido() {
  const [mesas, setMesas] = useState([]);
  const [productos, setProductos] = useState([]);
  const [mesaSeleccionada, setMesaSeleccionada] = useState("");
  const [detalles, setDetalles] = useState([]);
  const [mensaje, setMensaje] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchData = async () => {
      try {
        const token = localStorage.getItem("token");
        if (!token) throw new Error("Usuario no autenticado");

        const headers = { Authorization: `Bearer ${token}` };

        const resMesas = await fetch("http://127.0.0.1:8000/api/mesas/", { headers });
        if (!resMesas.ok) throw new Error("Error cargando mesas");
        setMesas(await resMesas.json());

        const resProductos = await fetch("http://127.0.0.1:8000/api/productos/", { headers });
        if (!resProductos.ok) throw new Error("Error cargando productos");
        setProductos(await resProductos.json());
      } catch (err) {
        setError(err.message);
      }
    };
    fetchData();
  }, []);

  const agregarDetalle = (producto) => {
    const index = detalles.findIndex((d) => d.producto_id === producto.id);
    if (index !== -1) {
      const nuevos = [...detalles];
      nuevos[index].cantidad += 1;
      setDetalles(nuevos);
    } else {
      setDetalles([...detalles, { producto_id: producto.id, nombre: producto.nombre, cantidad: 1 }]);
    }
  };

  const actualizarCantidad = (index, cantidad) => {
    const nuevos = [...detalles];
    nuevos[index].cantidad = parseInt(cantidad);
    setDetalles(nuevos);
  };

  const eliminarDetalle = (index) => {
    setDetalles(detalles.filter((_, i) => i !== index));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMensaje("");
    setError("");
    if (!mesaSeleccionada) return setError("Debes seleccionar una mesa");
    if (detalles.length === 0) return setError("Debes agregar al menos un producto");

    try {
      const token = localStorage.getItem("token");
      if (!token) throw new Error("No hay token de autenticación.");

      const response = await fetch("http://127.0.0.1:8000/api/pedidos/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          mesa_id: mesaSeleccionada,
          detalles: detalles.map((d) => ({ producto_id: d.producto_id, cantidad: d.cantidad })),
        }),
      });

      const text = await response.text();
      let data;
      try { data = JSON.parse(text); } catch { throw new Error("El servidor devolvió una respuesta no válida."); }

      if (!response.ok) throw new Error(data.error || "Error creando pedido");

      setMensaje("✅ Pedido creado correctamente");
      setMesaSeleccionada("");
      setDetalles([]);
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="crear-pedido-container">
      <Header />
      <div className="form-container">
        <h2 className="titulo-crear">Crear Pedido</h2>
        <form onSubmit={handleSubmit}>
          <label className="subtitulo-crear">Mesa:</label>
          <select
            value={mesaSeleccionada}
            onChange={(e) => setMesaSeleccionada(e.target.value)}
            className="select-mesa"
          >
            <option value="">Seleccionar Mesa</option>
            {mesas.map((m) => (
              <option key={m.id} value={m.id}>
                Mesa {m.numero} — {m.estado}
              </option>
            ))}
          </select>

          <h3 className="subtitulo-crear">Productos</h3>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-4 mb-8">
            {productos.map((p) => (
              <button
                key={p.id}
                type="button"
                onClick={() => agregarDetalle(p)}
                className="producto-btn"
              >
                <p className="font-bold">{p.nombre}</p>
                <p>${p.precio}</p>
              </button>
            ))}
          </div>

          <h3 className="subtitulo-crear">Resumen del Pedido</h3>
          {detalles.length === 0 && <p className="mensaje-error">No hay productos añadidos.</p>}
          {detalles.length > 0 && (
            <table className="tabla-resumen">
              <thead>
                <tr>
                  <th>Producto</th>
                  <th>Cantidad</th>
                  <th>Acción</th>
                </tr>
              </thead>
              <tbody>
                {detalles.map((d, index) => (
                  <tr key={index}>
                    <td>{d.nombre}</td>
                    <td>
                      <input
                        type="number"
                        min="1"
                        value={d.cantidad}
                        onChange={(e) => actualizarCantidad(index, e.target.value)}
                        className="input-cantidad"
                      />
                    </td>
                    <td>
                      <button
                        type="button"
                        onClick={() => eliminarDetalle(index)}
                        className="producto-btn"
                        style={{ backgroundColor: "#b23434", color: "#fff", borderColor: "#d14747" }}
                      >
                        Eliminar
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}

          <button type="submit" className="btn-crear-pedido">Crear Pedido</button>
        </form>

        {mensaje && <p className="mensaje-exito">{mensaje}</p>}
        {error && <p className="mensaje-error">{error}</p>}
      </div>
    </div>
  );
}
