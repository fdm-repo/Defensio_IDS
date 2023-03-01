import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import itertools

# Creazione del grafo vuoto
G = nx.Graph()

# Aggiunta dei nodi
network = [('192.168.1.1', ['192.168.1.2', '192.168.1.3']),
           ('192.168.1.2', ['192.168.1.1', '192.168.1.4']),
           ('192.168.1.3', ['192.168.1.1', '192.168.1.4']),
           ('192.168.1.4', ['192.168.1.2', '192.168.1.3'])]

for device in network:
    ip_address = device[0]
    G.add_node(ip_address)

# Aggiunta dei collegamenti tra i nodi
for device in network:
    source_ip = device[0]
    for destination_ip in device[1]:
        G.add_edge(source_ip, destination_ip)

# Definizione dei colori
colors = itertools.cycle(['r', 'g', 'b', 'c', 'm', 'y', 'k'])

# Funzione per animare il grafico
def animate(i):
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color=next(colors))

# Creazione dell'animazione
ani = animation.FuncAnimation(plt.gcf(), animate, interval=1000)

# Visualizzazione dell'animazione
plt.show()
