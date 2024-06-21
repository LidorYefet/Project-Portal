import networkx as nx
import matplotlib.pyplot as plt

tree = {
    'root': {
        'count': 0,
        'keywords': {},
        'children': {
            'Blockchain': {
                'count': 0,
                'keywords': {'blockchain'},
                'children': {}
            },
            'Cryptocurrency': {
                'count': 0,
                'keywords': {'cryptocurrency', 'bitcoin', 'ethereum'},
                'children': {}
            },
            'Cyber Security': {
                'count': 0,
                'keywords': {'cyber security', 'malware', 'phishing'},
                'children': {}
            },
            'Artificial Intelligence': {
                'count': 0,
                'keywords': {'artificial intelligence', 'machine learning', 'neural network'},
                'children': {}
            }
        }
    }
}

def add_edges(graph, node_dict, parent=None):
    for name, child_node in node_dict.items():
        if parent is not None:
            graph.add_edge(parent, name)
        add_edges(graph, child_node['children'], parent=name)

graph = nx.DiGraph()

add_edges(graph, tree['root']['children'], parent='root')

plt.figure(figsize=(8, 6))
pos = nx.spring_layout(graph)
nx.draw(graph, pos, with_labels=True, font_size=12, node_size=3000, node_color="skyblue")
plt.show()
