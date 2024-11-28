import csv
import sys

from util import Node, StackFrontier, QueueFrontier  # Importa clases definidas en util.py para la búsqueda

# Estructuras de datos globales para almacenar información de personas, nombres y películas
names = {}  # Mapea nombres a conjuntos de person_ids
people = {}  # Mapea person_ids a un diccionario con nombre, nacimiento y películas
movies = {}  # Mapea movie_ids a un diccionario con título, año y estrellas


def load_data(directory):
    """
    Carga datos desde archivos CSV al sistema de memoria.
    """
    # Carga los datos de people.csv
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)  # Lee el archivo CSV como diccionarios
        for row in reader:
            # Cada persona se mapea a un diccionario con nombre, nacimiento y películas
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            # Mapea los nombres a conjuntos de person_ids (maneja nombres duplicados)
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Carga los datos de movies.csv
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Cada película se mapea a un diccionario con título, año y estrellas
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Carga los datos de stars.csv (relaciones entre personas y películas)
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                # Relaciona a una persona con las películas que protagonizó
                people[row["person_id"]]["movies"].add(row["movie_id"])
                # Relaciona una película con las personas que actuaron en ella
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                # Si hay referencias inválidas, las ignora
                pass


def main():
    """
    Punto de entrada del programa.
    """
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")  # Verifica que no haya argumentos extraños
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"  # Define el directorio a usar

    # Carga los datos a memoria
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    # Solicita los nombres de origen y destino
    source = person_id_for_name(input("Name: "))  # Busca el ID de la persona
    if source is None:
        sys.exit("Person not found.")  # Termina si no se encuentra la persona

    target = person_id_for_name(input("Name: "))  # Busca el ID del objetivo
    if target is None:
        sys.exit("Person not found.")  # Termina si no se encuentra el objetivo

    # Encuentra el camino más corto
    path = shortest_path(source, target)

    # Imprime el resultado
    if path is None:
        print("Not connected.")  # Si no hay conexión, informa al usuario
    else:
        degrees = len(path)  # La longitud del camino es el número de grados de separación
        print(f"{degrees} degrees of separation.")
        # Desglosa el camino en formato legible
        path = [(None, source)] + path  # Añade el nodo inicial al camino
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]  # Nombre de la persona inicial
            person2 = people[path[i + 1][1]]["name"]  # Nombre de la persona conectada
            movie = movies[path[i + 1][0]]["title"]  # Película que conecta
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")


def shortest_path(source, target):
    """
    Retorna el camino más corto desde la persona con ID source hasta la persona con ID target.
    """
    # Frontera inicial para BFS
    frontier = QueueFrontier()
    start = Node(state=source, parent=None, action=None)  # Nodo inicial
    frontier.add(start)

    # Conjunto de estados explorados
    explored = set()

    while not frontier.empty():
        # Remueve el siguiente nodo de la frontera
        node = frontier.remove()

        # Si el nodo actual es el objetivo, construye el camino
        if node.state == target:
            path = []
            while node.parent is not None:
                path.append((node.action, node.state))
                node = node.parent
            path.reverse()  # Invierte el camino
            return path

        # Marca el nodo como explorado
        explored.add(node.state)

        # Agrega vecinos a la frontera
        for movie_id, person_id in neighbors_for_person(node.state):
            if person_id not in explored and not frontier.contains_state(person_id):
                child = Node(state=person_id, parent=node, action=movie_id)
                if person_id == target:
                    # Si el vecino es el objetivo, construye el camino y retorna
                    path = []
                    while child.parent is not None:
                        path.append((child.action, child.state))
                        child = child.parent
                    path.reverse()
                    return path
                frontier.add(child)

    # Si no hay camino, retorna None
    return None


def person_id_for_name(name):
    """
    Retorna el ID de una persona dado su nombre.
    """
    person_ids = list(names.get(name.lower(), set()))  # Obtiene todos los IDs asociados al nombre
    if len(person_ids) == 0:
        return None  # No encontrado
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")  # Solicita al usuario que aclare
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]  # Retorna el único ID asociado al nombre


def neighbors_for_person(person_id):
    """
    Retorna pares (movie_id, person_id) de personas que trabajaron con una persona dada.
    """
    movie_ids = people[person_id]["movies"]  # Obtiene las películas del actor
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:  # Agrega a las estrellas de esas películas
            neighbors.add((movie_id, person_id))
    return neighbors  # Conjunto de pares (movie_id, person_id)


if __name__ == "__main__":
    main()
