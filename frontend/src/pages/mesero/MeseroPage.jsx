import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";

const MeseroPage = () => {
  const [tasks, setTasks] = useState([]);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    const fetchTasks = async () => {
      try {
        const response = await fetch("http://127.0.0.1:8000/api/mesero_tasks/", {
          headers: {
            "Content-Type": "application/json",
          },
          credentials: "include", // Si usas cookies o sesión
        });

        if (!response.ok) throw new Error("No autorizado o error en la petición");

        const data = await response.json();
        setTasks(data.tasks);
      } catch (err) {
        setError(err.message);
      }
    };

    fetchTasks();
  }, []);

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <h1 className="text-3xl font-bold mb-6 text-gray-800">Panel del Mesero</h1>

      {/* Panel de control */}
      <Card className="max-w-md shadow-lg p-4">
        <CardContent className="flex flex-col gap-4">
          <h3 className="font-semibold text-xl mb-2 text-gray-700">Panel de Control</h3>
          <Button variant="outline" onClick={() => navigate("/inventario")}>
            Ver Inventario
          </Button>
          <Button variant="outline" onClick={() => navigate("/pedidos")}>
            Lista de Pedidos
          </Button>
          <Button variant="outline" onClick={() => navigate("/mesas")}>
            Mesas Disponibles
          </Button>
        </CardContent>
      </Card>

      {/* Mostrar tareas si el backend las envía */}
      <div className="mt-8">
        <h2 className="text-2xl font-semibold mb-4 text-gray-700">Tareas del mesero</h2>
        {error && <p className="text-red-500">{error}</p>}
        <ul className="list-disc pl-6">
          {tasks.map((task, index) => (
            <li key={index} className="text-gray-700">
              {task}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default MeseroPage;
