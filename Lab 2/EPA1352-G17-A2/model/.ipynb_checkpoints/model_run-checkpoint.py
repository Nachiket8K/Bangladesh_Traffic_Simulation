from model import BangladeshModel, compute_average_driving, compute_worst_bridge, compute_worst_bridge_delay

"""
    Run simulation
    Print output at terminal
"""

# ---------------------------------------------------------------

# run time 
run_length = 5 * 24 * 60

seed = 1234567

sim_model = BangladeshModel(seed=seed, prob_A = 0, prob_B = 0, prob_C = 0, prob_D = 0)

# Check if the seed is set
print("SEED : " + str(sim_model._seed))

# One run with given steps
for i in range(run_length):
    sim_model.step()

# print the average driving time to console after model run
print(compute_average_driving(sim_model))

print(compute_worst_bridge(sim_model))

print(compute_worst_bridge_delay(sim_model))
