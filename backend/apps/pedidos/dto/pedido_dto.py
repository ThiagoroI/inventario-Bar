from dataclasses import dataclass
from typing import List

@dataclass
class DetallePedidoDTO:
    producto_id: int
    cantidad: int


@dataclass
class PedidoDTO:
    mesa_id: int
    detalles: List[DetallePedidoDTO]
