import pandas as pd
import networkx as nx

# Load datasets
names = ["merchant_zipcode", "date", "category", "client_zipcode", "merchants", "cards", "payments", "avg_payment", "max_payment", "min_payment", "std"]
customer = pd.read_csv("dataset/customer_zipcodes000", delim_whitespace=True, names= names)
customer = customer[customer["client_zipcode"] != "unknown"]

gcustomer = customer[["merchant_zipcode","client_zipcode"]].pivot_table(index=["merchant_zipcode"], columns=["client_zipcode"], aggfunc=len, fill_value=0)
gcustomer["merchant_zipcode"] = gcustomer.index

nodes = pd.melt(gcustomer, id_vars=["merchant_zipcode"])
nodes = nodes[["client_zipcode", "merchant_zipcode", "value"]]
nodes["client_zipcode"] = nodes.client_zipcode.map(int)
nodes = nodes[nodes["value"] != 0]
nodes = nodes.drop(nodes[nodes.merchant_zipcode == nodes.client_zipcode].index)

tuples = [tuple(x) for x in nodes.values]

DG=nx.DiGraph()
DG.add_weighted_edges_from(tuples)
#nx.draw(DG)

print "Number of connected components: ",  nx.number_connected_components(DG.to_undirected())

zipcodes_components = nx.connected_components(DG.to_undirected())
print [len(c) for c in zipcodes_components]

# Centrality
print "\nCentrality\n"
degree = nx.degree_centrality(DG)
# Once we are calculated degree centrality, we sort the results to see which nodes are more central.
print sorted(degree.items(), key=lambda x: x[1],reverse = True)[:3]
# indegree centrality sorting?. People going to this zipcodes to buy
# (8006, 0.3621621621621622), (8002, 0.2756756756756757), (8019, 0.24054054054054055)
# 8006 -> Gracia
# 8002 -> Gotic
# 8019 -> poblenou, forum

print "\nBetweenness\n"
betweenness = nx.betweenness_centrality(DG)
# And we sort the results to see which nodes are more central.
print sorted(betweenness.items(), key=lambda x: x[1],reverse = True)[:3]

print "\nCloseness\n"
# Let's compute the closeness centrality
closeness = nx.closeness_centrality(DG)
# And we sort the results to see which nodes are more central.
print sorted(closeness.items(), key=lambda x: x[1],reverse = True)[:3]

print "\nEigenVector centrality\n"
# Let's compute the closeness centrality
eigenvector = nx.eigenvector_centrality(DG)
# And we sort the results to see which nodes are more central.
print sorted(eigenvector.items(), key=lambda x: x[1],reverse = True)[:3]

#TODO graph partition? 