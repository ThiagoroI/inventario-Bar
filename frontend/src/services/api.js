export async function getProductos() {
  const token = localStorage.getItem("token");

  const response = await fetch("http://127.0.0.1:8000/api/productos/", {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Token ${token}`,
    },
  });

  if (!response.ok) {
    throw new Error("Error al obtener productos");
  }

  return await response.json();
}
