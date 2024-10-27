from model import BangladeshModel, compute_average_driving, compute_worst_bridge, compute_worst_bridge_delay, get_probs, compute_traffic
from mesa.batchrunner import FixedBatchRunner
import pandas as pd

# run settings
run_length = 5 * 24* 60  # run the model for 5 * 24 hours, translated to minutes
seed = 1234567
iterations = 1

# parameters that remain constant for all runs
fixed_params = {
    # option for set seed "seed": seed,
}

# list with dictionaries with parameter values per scenario, loaded from the scenarios csv file
parameter_list = pd.read_csv('../data/experiments/scenarios_input.csv').drop(['scenario'], axis=1).to_dict('records')

# configure the batch runner
batch_run = FixedBatchRunner(BangladeshModel, 
                        parameter_list, 
                        fixed_params,
                        iterations=iterations,
                        max_steps=run_length,
                        model_reporters={"Average driving time": compute_average_driving, "Worst bridge name": compute_worst_bridge, "Worst bridge delay": compute_worst_bridge_delay, "Probs": get_probs, "Traffic": compute_traffic}
                        )

# run the batch run configuration and save to dataframe
batch_run.run_all()

run_data = batch_run.get_model_vars_dataframe()

# split traffic data
run_data['generated'], run_data['removed'], run_data['delay_time_abs'], run_data['delay_time_rel'], run_data['delay_freq_abs'], run_data['delay_freq_rel'], run_data['traffic_bridges'], run_data['traffic_links'] = zip(*run_data['Traffic'])

# save run data to csv
run_data.to_csv('../data/experiments/all_scenarios.csv')

# save every scenerio to seperate csv file
start = 0
end = iterations 

for scenario in range(len(parameter_list)):
    run_data[start:end].to_csv('../data/experiments/scenario{}.csv'.format(scenario))
    start += iterations
    end += iterations

