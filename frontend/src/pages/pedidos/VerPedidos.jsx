import { useEffect, useState } from "react";
import Header from "../Header"; // Ajusta ruta según tu proyecto
import "./pedidos.css";

export default function Pedidos() {
  const [pedidos, setPedidos] = useState([]);
  const [estadoSeleccionado, setEstadoSeleccionado] = useState({});
  const token = localStorage.getItem("token");
  const ESTADOS = [
    { value: "pendiente", label: "Pendiente" },
    { value: "en_proceso", label: "En proceso" },
    { value: "pagado", label: "Pagado" },
    { value: "cancelado", label: "Cancelado" },
  ];

  const fetchPedidos = async () => {
    try {
      const res = await fetch("http://127.0.0.1:8000/api/pedidos/listar/", {
        headers: { Authorization: `Bearer ${token}` },
      });
      const data = await res.json();
      setPedidos(data);
      const inicial = {};
      data.forEach((p) => (inicial[p.id] = p.estado));
      setEstadoSeleccionado(inicial);
    } catch (err) { console.log(err); }
  };

  useEffect(() => { fetchPedidos(); }, []);

  const actualizarEstado = async (pedidoId) => {
    try {
      await fetch(`http://127.0.0.1:8000/api/pedidos/${pedidoId}/estado/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ estado: estadoSeleccionado[pedidoId] }),
      });
      fetchPedidos();
    } catch (err) { console.log(err); }
  };

  const eliminarPedido = async (pedidoId) => {
    if (!confirm("¿Seguro que deseas eliminar este pedido?")) return;
    try {
      await fetch(`http://127.0.0.1:8000/api/pedidos/${pedidoId}/eliminar/`, {
        method: "DELETE",
        headers: { Authorization: `Bearer ${token}` },
      });
      fetchPedidos();
    } catch (err) { console.log(err); }
  };

  return (
    <div className="pedidos-container">
      <Header />
      <h1 className="titulo">Pedidos Registrados</h1>

      <div className="tabla-contenedor">
        <table className="tabla">
          <thead>
            <tr>
              <th>ID</th><th>Mesa</th><th>Usuario</th><th>Productos</th>
              <th>Estado</th><th>Total</th><th>Fecha</th><th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            {pedidos.map((p) => (
              <tr key={p.id}>
                <td>{p.id}</td>
                <td>Mesa {p.mesa_numero}</td>
                <td>{p.usuario_username || "—"}</td>
                <td>
                  {p.detalles.map((d) => (
                    <div key={d.id}>{d.producto_nombre} — <strong>{d.cantidad}u</strong></div>
                  ))}
                </td>
                <td>
                  <select
                    className="select-estado"
                    value={estadoSeleccionado[p.id]}
                    onChange={(e) =>
                      setEstadoSeleccionado({ ...estadoSeleccionado, [p.id]: e.target.value })
                    }
                  >
                    {ESTADOS.map((e) => (
                      <option key={e.value} value={e.value}>{e.label}</option>
                    ))}
                  </select>
                </td>
                <td>${p.total}</td>
                <td>{new Date(p.fecha_creacion).toLocaleString()}</td>
                <td>
                  <button className="btn" onClick={() => actualizarEstado(p.id)}>Actualizar</button>
                  <button className="btn-danger" onClick={() => eliminarPedido(p.id)}>Eliminar</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
