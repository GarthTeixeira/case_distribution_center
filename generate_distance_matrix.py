import googlemaps
import pandas as pd
from dotenv import load_dotenv
import os
from ortools.constraint_solver import pywrapcp, routing_enums_pb2


load_dotenv()

# Sua API Key
API_KEY = os.getenv("API_KEY_GOOGLE")
cities = [
    "Recife, PE",
    "Salvador, BA",
    "Fortaleza, CE",
    "Natal, RN",
    "João Pessoa, PB",
    "Maceió, AL",
    "Aracaju, SE",
    "Teresina, PI"
]
# =================================


# --- Função para montar matriz de distâncias e tempos ---
def build_matrices(cities, mode="driving"):
    n = len(cities)
    dist_matrix = [[0]*n for _ in range(n)]
    dur_matrix = [[0]*n for _ in range(n)]

    gmaps = googlemaps.Client(key=API_KEY)

    for i, origin in enumerate(cities):
        result = gmaps.distance_matrix(origins=[origin],
                                       destinations=cities,
                                       mode=mode,
                                       units="metric",
                                       region="br")
        for j, row in enumerate(result["rows"][0]["elements"]):
            if row["status"] == "OK":
                dist_matrix[i][j] = row["distance"]["value"] // 1000  # km
                dur_matrix[i][j] = row["duration"]["value"] // 60     # minutos
            else:
                dist_matrix[i][j] = None
                dur_matrix[i][j] = None

    return dist_matrix, dur_matrix


# --- Solver com OR-Tools ---
def solve_vrp(distance_matrix, depot_index):
    data = {}
    data['distance_matrix'] = distance_matrix
    data['num_vehicles'] = 1
    data['depot'] = depot_index

    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                           data['num_vehicles'],
                                           data['depot'])
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    solution = routing.SolveWithParameters(search_parameters)
    if solution is None:
        return None, None

    index = routing.Start(0)
    route = []
    route_distance = 0
    while not routing.IsEnd(index):
        node = manager.IndexToNode(index)
        route.append(node)
        previous_index = index
        index = solution.Value(routing.NextVar(index))
        route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
    route.append(manager.IndexToNode(index))
    return route, route_distance


# --- Impressão da rota ---
def pretty_print(route, dist, cities, label):
    if route is None:
        print(f"{label}: sem solução.")
        return
    names = [cities[i] for i in route]
    print(f"\n{label}")
    print(" -> ".join(names))
    print(f"Distância total: {dist} km")


def compare_cd(dist_matrix, dur_matrix, cities):
    depot_rec = 0  # Recife
    depot_sal = 1  # Salvador

    rec_dist = dist_matrix[depot_rec]
    sal_dist = dist_matrix[depot_sal]
    rec_dur = dur_matrix[depot_rec]
    sal_dur = dur_matrix[depot_sal]

    df = pd.DataFrame({
        "Cidade": cities,
        "De Recife (km)": rec_dist,
        "De Salvador (km)": sal_dist,
        "De Recife (min)": rec_dur,
        "De Salvador (min)": sal_dur,
    })

    # excluir as linhas do próprio CD (distância 0)
    df = df[~df["Cidade"].isin(["Recife, PE", "Salvador, BA"])]

    # salvar CSV
    df.to_csv("comparacao_cds.csv", index=False, encoding="utf-8")

    print(df)
    print("\nResumo (distâncias):")
    print(f"Total Recife → capitais: {df['De Recife (km)'].sum()} km")
    print(f"Total Salvador → capitais: {df['De Salvador (km)'].sum()} km")
    print(f"Média Recife: {df['De Recife (km)'].mean():.1f} km")
    print(f"Média Salvador: {df['De Salvador (km)'].mean():.1f} km")

    print("\nResumo (tempos):")
    print(f"Total Recife → capitais: {df['De Recife (min)'].sum()} min")
    print(f"Total Salvador → capitais: {df['De Salvador (min)'].sum()} min")
    print(f"Média Recife: {df['De Recife (min)'].mean():.1f} min")
    print(f"Média Salvador: {df['De Salvador (min)'].mean():.1f} min")


if __name__ == "__main__":
    print("🔄 Consultando Google Maps API...")
    dist_matrix, dur_matrix = build_matrices(cities)

    print("✅ Matrizes coletadas. Gerando comparação...\n")
    compare_cd(dist_matrix, dur_matrix, cities)
    print("\n📊 Resultados salvos em comparacao_cds.csv")
