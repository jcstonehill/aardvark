from aardvark.base.log import Log

import numpy as np


class Mesh1D:
    @property
    def nodes(self) -> np.ndarray:
        return self._nodes
    
    @nodes.setter
    def nodes(self, new_nodes: np.ndarray):
        new_nodes = np.array(new_nodes)

        self._cells = self.get_cells_from_nodes(new_nodes)
        self._dx = self.get_dx_from_nodes(new_nodes)

        self._nodes = np.array(new_nodes)

    @property
    def cells(self) -> np.ndarray:
        return self._cells
    
    @cells.setter
    def cells(self, new_cells: np.ndarray):
        Log.error("Mesh1D :: Tried to set cells directly. Only nodes can be set directly.")

    @property
    def dx(self) -> np.ndarray:
        return self._dx
    
    @cells.setter
    def dx(self, new_dx: np.ndarray):
        Log.error("Mesh1D :: Tried to set dx directly. Only nodes can be set directly.")

    
    def __init__(self, start_x: float = None, end_x: float = None, N: int = None, node_x = None):
        if(node_x is not None):
            self.nodes = node_x
        
        else:
            self.nodes = np.linspace(start_x, end_x, N)

    def get_cells_from_nodes(self, nodes: np.ndarray) -> np.ndarray:
        return np.array([0.5*nodes[i+1] + 0.5*nodes[i] for i in range(nodes.size - 1)])
    
    def get_dx_from_nodes(self, nodes: np.ndarray) -> np.ndarray:
        return np.array([nodes[i+1] - nodes[i] for i in range(nodes.size - 1)])
    
    