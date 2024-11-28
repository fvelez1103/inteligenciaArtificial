class Node():
    def __init__(self, state, parent, action):
        """
        Representa un nodo en el grafo de búsqueda.
        - state: El estado actual.
        - parent: Nodo desde el cual se alcanzó este nodo.
        - action: Acción que llevó a este nodo (película en este caso).
        """
        self.state = state
        self.parent = parent
        self.action = action


class StackFrontier():
    def __init__(self):
        """
        Frontera para búsqueda basada en pila (LIFO).
        """
        self.frontier = []

    def add(self, node):
        """
        Agrega un nodo a la frontera.
        """
        self.frontier.append(node)

    def contains_state(self, state):
        """
        Verifica si la frontera contiene un estado específico.
        """
        return any(node.state == state for node in self.frontier)

    def empty(self):
        """
        Verifica si la frontera está vacía.
        """
        return len(self.frontier) == 0

    def remove(self):
        """
        Remueve el nodo más reciente (último en entrar).
        """
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node


class QueueFrontier(StackFrontier):
    def remove(self):
        """
        Remueve el nodo más antiguo (primero en entrar), usado para BFS.
        """
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node
