from abc import ABC, abstractmethod
from collections import deque, defaultdict
from typing import List, Tuple, Optional

class Vertex(ABC):
    
    @abstractmethod
    def num_inputs(self) -> int:
        pass
    
    @abstractmethod
    def set_input(self, inp_idx: int, inp_val: float) -> None:
        pass
    
    @abstractmethod
    def num_outputs(self) -> int:
        pass
    
    @abstractmethod
    def get_output(self, out_idx: int) -> float:
        pass
    
    @abstractmethod
    def calc_value(self) -> None:
        pass

class Edge:
    
    def __init__(self, out_vertex_id: int, out_port_id: int, 
                 inp_vertex_id: int, inp_port_id: int):
        self.out_vertex_id = out_vertex_id
        self.out_port_id = out_port_id
        self.inp_vertex_id = inp_vertex_id
        self.inp_port_id = inp_port_id

class CalcGraph(Vertex):
    
    def __init__(self):
        self.vertices: List[Vertex] = []
        self.edges: List[Edge] = []
        self.free_inputs: List[Tuple[int, int]] = []  
        self.free_outputs: List[Tuple[int, int]] = [] 
        self.execution_order: List[int] = []
        
        self.input_connected: List[List[bool]] = []
        self.output_connected: List[List[bool]] = []
    
    def set_data(self, vertices: List[Vertex], edges: List[Edge]) -> None:
        self.vertices = vertices
        self.edges = edges
        self._build_execution_order()
    
    def _build_execution_order(self) -> None:
        n = len(self.vertices)
        
        adj = [[] for _ in range(n)]
        in_degree = [0] * n
        
        self.input_connected = [[False] * vertex.num_inputs() for vertex in self.vertices]
        self.output_connected = [[False] * vertex.num_outputs() for vertex in self.vertices]
        
        for edge in self.edges:
            if (edge.out_vertex_id < 0 or edge.out_vertex_id >= n or
                edge.inp_vertex_id < 0 or edge.inp_vertex_id >= n):
                raise IndexError(f"Invalid vertex ID in edge: {edge.out_vertex_id} -> {edge.inp_vertex_id}")
            
            if (edge.out_port_id < 0 or edge.out_port_id >= self.vertices[edge.out_vertex_id].num_outputs() or
                edge.inp_port_id < 0 or edge.inp_port_id >= self.vertices[edge.inp_vertex_id].num_inputs()):
                raise IndexError(f"Invalid port ID in edge")

            adj[edge.out_vertex_id].append(edge.inp_vertex_id)
            in_degree[edge.inp_vertex_id] += 1
            

            self.output_connected[edge.out_vertex_id][edge.out_port_id] = True
            self.input_connected[edge.inp_vertex_id][edge.inp_port_id] = True
        
        queue = deque()
        for i in range(n):
            if in_degree[i] == 0:
                queue.append(i)
        
        self.execution_order = []
        while queue:
            u = queue.popleft()
            self.execution_order.append(u)
            
            for v in adj[u]:
                in_degree[v] -= 1
                if in_degree[v] == 0:
                    queue.append(v)
        

        if len(self.execution_order) != n:
            raise RuntimeError("Graph contains cycles")
        

        self.free_inputs = []
        self.free_outputs = []
        
        for i, vertex in enumerate(self.vertices):
            for j in range(vertex.num_inputs()):
                if not self.input_connected[i][j]:
                    self.free_inputs.append((i, j))
            
            for j in range(vertex.num_outputs()):
                if not self.output_connected[i][j]:
                    self.free_outputs.append((i, j))
    

    def num_inputs(self) -> int:
        return len(self.free_inputs)
    
    def set_input(self, inp_idx: int, inp_val: float) -> None:
        if inp_idx < 0 or inp_idx >= len(self.free_inputs):
            raise IndexError(f"Input index {inp_idx} out of range [0, {len(self.free_inputs) - 1}]")
        
        vertex_id, port_id = self.free_inputs[inp_idx]
        self.vertices[vertex_id].set_input(port_id, inp_val)
    
    def num_outputs(self) -> int:
        return len(self.free_outputs)
    
    def get_output(self, out_idx: int) -> float:
        if out_idx < 0 or out_idx >= len(self.free_outputs):
            raise IndexError(f"Output index {out_idx} out of range [0, {len(self.free_outputs) - 1}]")
        
        vertex_id, port_id = self.free_outputs[out_idx]
        return self.vertices[vertex_id].get_output(port_id)
    
    def calc_value(self) -> None:
        for vertex_id in self.execution_order:
            self.vertices[vertex_id].calc_value()

class PlusOperator(Vertex):
    
    def __init__(self):
        self.m_inp_val = [0.0, 0.0]
        self.m_out_val = 0.0
    
    def num_inputs(self) -> int:
        return 2
    
    def set_input(self, inp_idx: int, inp_val: float) -> None:
        if inp_idx < 0 or inp_idx >= 2:
            raise IndexError(f"Bad inp idx {inp_idx} in PlusOperator::set_input")
        self.m_inp_val[inp_idx] = inp_val
    
    def calc_value(self) -> None:
        self.m_out_val = self.m_inp_val[0] + self.m_inp_val[1]
    
    def num_outputs(self) -> int:
        return 1
    
    def get_output(self, out_idx: int) -> float:
        if out_idx != 0:
            raise IndexError(f"Bad out idx {out_idx} in PlusOperator::get_output")
        return self.m_out_val

class MultiplyOperator(Vertex):
    
    def __init__(self):
        self.m_inp_val = [0.0, 0.0]
        self.m_out_val = 0.0
    
    def num_inputs(self) -> int:
        return 2
    
    def set_input(self, inp_idx: int, inp_val: float) -> None:
        if inp_idx < 0 or inp_idx >= 2:
            raise IndexError(f"Bad inp idx {inp_idx} in MultiplyOperator::set_input")
        self.m_inp_val[inp_idx] = inp_val
    
    def calc_value(self) -> None:
        self.m_out_val = self.m_inp_val[0] * self.m_inp_val[1]
    
    def num_outputs(self) -> int:
        return 1
    
    def get_output(self, out_idx: int) -> float:
        if out_idx != 0:
            raise IndexError(f"Bad out idx {out_idx} in MultiplyOperator::get_output")
        return self.m_out_val

class ConstantOperator(Vertex):
    
    def __init__(self, value: float = 0.0):
        self.value = value
    
    def num_inputs(self) -> int:
        return 0
    
    def set_input(self, inp_idx: int, inp_val: float) -> None:
        raise IndexError("ConstantOperator has no inputs")
    
    def calc_value(self) -> None:
        pass  
    
    def num_outputs(self) -> int:
        return 1
    
    def get_output(self, out_idx: int) -> float:
        if out_idx != 0:
            raise IndexError(f"Bad out idx {out_idx} in ConstantOperator::get_output")
        return self.value

