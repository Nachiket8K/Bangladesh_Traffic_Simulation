from model import BangladeshModel, compute_average_driving, compute_worst_bridge, compute_worst_bridge_delay, \
    compute_traffic

"""
    Run simulation
    Print output at terminal
"""

# ---------------------------------------------------------------

# run time 5 x 24 hours; 1 tick 1 minute
run_length = 5 * 24 * 60

# run time 1000 ticks
# run_length = 1000

seed = 1234567

sim_model = BangladeshModel(seed=seed, prob_A=0.5, prob_B=0.5, prob_C=0.5, prob_D=0.5)

"""
# draw network
import networkx as nx
G = sim_model.network
pos = nx.get_node_attributes(G,'pos')
nx.draw(G, pos = pos, with_labels = False, node_size = 5)
"""

# Check if the seed is set
print("SEED " + str(sim_model._seed))

# One run with given steps
for i in range(run_length):
    sim_model.step()
    if 0 == i % (24 * 60):
        print(i)

# print metrics to console after model run
print(compute_average_driving(sim_model))

print(compute_worst_bridge(sim_model))

print(compute_worst_bridge_delay(sim_model))

print(compute_traffic(sim_model))
# save dictionaries with generated trucks per source and removed trucks per sink
generated, removed, delay_time_abs, delay_time_rel, delay_freq_abs, delay_freq_rel, \
        traffic_bridges, traffic_links = compute_traffic(sim_model)
print(len(generated))
