import networkx as nx
import matplotlib.pyplot as plt
import random
import pandas as pd


#----------------------GERADOR-DO-GRAFO-------------------------

# Gerar grafo conectado com 20 vertices
G = nx.random_geometric_graph(20, radius=0.3, dim=2, pos=None, p=2)

for node in G.nodes():
    x = random.uniform(0, 1)
    y = random.uniform(0, 1)
    G.nodes[node]['pos'] = (x, y)

# Remover nos isolados
nos_isolados = list(nx.isolates(G))
G.remove_nodes_from(nos_isolados)

# Converter o grafo para um grafo direcionado
G = G.to_undirected()


# Adicionar capacidade e fluxo inicial para as arestas
for u, v in G.edges():
    capacidade = random.randint(1, 10)
    G.edges[u, v]['capacity'] = capacidade
    G.edges[u, v]['flow'] = 0
    
#---------------------------------------------------------
#--------------FORD-FULKERSON-----------------------------

# Funcao para encontrar um caminho aumentante
def buscaProfundidade(graph, source, target, path):
    if source == target:
        return path
    for proximo in graph.neighbors(source):
        capacidade_residual = graph[source][proximo]['capacity'] - graph[source][proximo]['flow']
        if capacidade_residual > 0 and proximo not in path:
            result = buscaProfundidade(graph, proximo, target, path + [proximo])
            if result is not None:
                return result

    return None


def fordFulkerson(graph, source, target):
    fluxo_maximo = 0
    path = buscaProfundidade(graph, source, target, [source])
    while path is not None:
        # Encontra a capacidade residual mínima ao longo do caminho aumentante
        capacidades_residuais = [graph[path[i]][path[i+1]]['capacity'] - graph[path[i]][path[i+1]]['flow']
                               for i in range(len(path)-1)]
        
        minima_capacidade_residual = min(capacidades_residuais)

        # Atualiza o fluxo ao longo do caminho aumentante
        for i in range(len(path)-1):
            graph[path[i]][path[i+1]]['flow'] += minima_capacidade_residual

        fluxo_maximo += minima_capacidade_residual

        # Encontra um novo caminho aumentante
        path = buscaProfundidade(graph, source, target, [source])

    return fluxo_maximo

# Chamada do algoritmo de Ford-Fulkerson para encontrar o fluxo máximo
source = 0
target = len(G)-1
fluxoMaximo = fordFulkerson(G, source, target)
print("Fluxo máximo:", fluxoMaximo)

#------------------------------------------------------------------
#-----------GRAFO-FLUXO-MAXIMO-------------------------------------
# Posicionamento dos nós em um círculo equidistante
pos = nx.circular_layout(G)

# Desenhar o grafo com diferenciação das arestas de fluxo máximo e fluxo residual
fluxos_arestas = {(u, v): f"{G.edges[u, v]['flow']}/{G.edges[u, v]['capacity']}" for (u, v) in G.edges()}

arestas_Dicionario = {"source": [], "target": [], "flow": []}
for (u, v) in G.edges():
    arestas_Dicionario["source"].append(u)
    arestas_Dicionario["target"].append(v)
    arestas_Dicionario["flow"].append(fluxos_arestas[(u, v)])

aresta_dataFrame = pd.DataFrame(arestas_Dicionario)

cores_arestas = ['red' if G.edges[u, v]['flow'] == G.edges[u, v]['capacity'] else 'blue' for (u, v) in G.edges()]

plt.figure(figsize=(12,12))
nx.draw(G, pos, with_labels=True, node_size=300, node_color='lightblue', font_weight='bold', font_size=8)
nx.draw_networkx_edge_labels(G, pos, edge_labels=fluxos_arestas)
nx.draw_networkx_edges(G, pos, edge_color=cores_arestas)

plt.title("Grafo de interseções entre ruas com fluxo máximo")
plt.show()

def display_full_dataframe(dataframe):
    pd.set_option('display.max_rows', None)
    print(dataframe)
    pd.reset_option('display.max_rows')

display_full_dataframe(aresta_dataFrame)
