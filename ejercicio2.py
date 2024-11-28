def zona_a(inmueble):
    precio = (inmueble["metros"] * 1000 + inmueble["habitaciones"] * 5000 +
              inmueble["garaje"] * 15000) * (1 - (2024 - inmueble["año"]) / 100)
    return precio

def zona_b(inmueble):
    precio = (inmueble["metros"] * 1000 + inmueble["habitaciones"] * 5000 +
              inmueble["garaje"] * 15000) * (1 - (2024 - inmueble["año"]) / 100) * 1.5
    return precio

def calcular_precio_inmueble(funcion, inmueble):
    return funcion(inmueble)

def buscar_inmuebles(lista_inmuebles, presupuesto):
    inmuebles_encontrados = []
    for inmueble in lista_inmuebles:
        if(inmueble["zona"]=="A"):
            precio = calcular_precio_inmueble(zona_a, inmueble)
            if precio <= presupuesto:
                inmueble_encontrado = inmueble.copy()
                inmueble_encontrado["precio"] = precio
                inmuebles_encontrados.append(inmueble_encontrado)
        else:
            precio = calcular_precio_inmueble(zona_b, inmueble)
            if precio <= presupuesto:
                inmueble_encontrado = inmueble.copy()
                inmueble_encontrado["precio"] = precio
                inmuebles_encontrados.append(inmueble_encontrado)
    return inmuebles_encontrados

inmuebles = [
    {"año": 2000, "metros": 100, "habitaciones": 3, "garaje": True, "zona": "A"},
    {"año": 2012, "metros": 60, "habitaciones": 2, "garaje": True, "zona": "B"},
    {"año": 1980, "metros": 120, "habitaciones": 4, "garaje": False, "zona": "A"},
    {"año": 2005, "metros": 75, "habitaciones": 3, "garaje": True, "zona": "B"},
    {"año": 2015, "metros": 90, "habitaciones": 2, "garaje": False, "zona": "A"}
]

presupuesto = int(input("Ingrese su presupuesto: "))

inmuebles_disponibles = buscar_inmuebles(inmuebles, presupuesto)

print("Inmuebles disponibles dentro del presupuesto de", presupuesto, "USD:")
for inmueble in inmuebles_disponibles:
    print(inmueble)
