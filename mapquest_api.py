import requests

API_KEY = "TU_API_KEY_AQUI"
BASE_URL = "https://www.mapquestapi.com/directions/v2/route"
KM_POR_LITRO = 12.0
FACTOR_MILLAS_KM = 1.60934


def calcular_ruta(origen, destino):
    params = {
        "key": API_KEY,
        "from": origen,
        "to": destino,
        "unit": "m",
    }

    try:
        resp = requests.get(BASE_URL, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
    except requests.RequestException as e:
        print(f"  Error de conexion: {e}\n")
        return

    if data["info"]["statuscode"] != 0:
        print(f"  Error MapQuest: {data['info']['messages']}\n")
        return

    route = data["route"]

    distancia_km = route["distance"] * FACTOR_MILLAS_KM
    tiempo_seg = route["time"]
    horas = tiempo_seg // 3600
    minutos = (tiempo_seg % 3600) // 60
    combustible = distancia_km / KM_POR_LITRO

    print(f"\n{'='*55}")
    print(f"  Ruta: {origen}  -->  {destino}")
    print(f"{'='*55}")
    print(f"  Distancia    : {distancia_km:.2f} km")

    if horas > 0:
        print(f"  Duracion     : {int(horas)} hora(s) y {int(minutos)} minuto(s)")
    else:
        print(f"  Duracion     : {int(minutos)} minuto(s)")

    print(f"  Combustible  : {combustible:.2f} litros  (rendimiento: {KM_POR_LITRO:.2f} km/L)")
    print(f"{'='*55}")

    print("\n  Narrativa paso a paso:")
    paso = 1
    for leg in route.get("legs", []):
        for maneuver in leg.get("maneuvers", []):
            print(f"  {paso}. {maneuver['narrative']}")
            paso += 1
    print()


def main():
    print("============================================")
    print("   Calculadora de Rutas - MapQuest API     ")
    print("   (ingresa 'q' en cualquier campo para    ")
    print("    salir del programa)                    ")
    print("============================================\n")

    while True:
        origen = input("  Origen  : ").strip()
        if origen.lower() == "q":
            print("\n  Hasta luego.\n")
            break

        destino = input("  Destino : ").strip()
        if destino.lower() == "q":
            print("\n  Hasta luego.\n")
            break

        if origen and destino:
            calcular_ruta(origen, destino)
        else:
            print("  Por favor ingresa origen y destino validos.\n")


if __name__ == "__main__":
    main()
