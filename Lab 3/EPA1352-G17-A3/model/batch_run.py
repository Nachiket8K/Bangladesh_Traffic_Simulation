from model import BangladeshModel, compute_average_driving, compute_worst_bridge, compute_worst_bridge_delay, get_probs
from mesa.batchrunner import FixedBatchRunner
import tensorflow as tf
import pandas as pd

# run settings
run_length = 5 * 24 * 60  # run the model for 5 * 24 hours, translated to minutes
seed = 1234567
iterations = 10

# parameters that remain constant for all runs
fixed_params = {
    # option for set seed "seed": seed,
}


parameter_list = [
    {"prob_A": 0, "prob_B": 0, "prob_C": 0, "prob_D": 0},
    {"prob_A": 0, "prob_B": 0, "prob_C": 0, "prob_D": 0.05},
    {"prob_A": 0, "prob_B": 0, "prob_C": 0.05, "prob_D": 0.10},
    {"prob_A": 0, "prob_B": 0.05, "prob_C": 0.10, "prob_D": 0.20},
    {"prob_A": 0.05, "prob_B": 0.10, "prob_C": 0.20, "prob_D": 0.40},
]


def callfunc():
    with tf.device('/GPU:0'):
        # configure the batch runner
        batch_run = FixedBatchRunner(BangladeshModel,
                                parameter_list,
                                fixed_params,
                                iterations=iterations,
                                max_steps=run_length,
                                model_reporters={"Average driving time": compute_average_driving, "Worst bridge name": compute_worst_bridge, "Worst bridge delay": compute_worst_bridge_delay, "Probs": get_probs}
                                )

        # run the batch run configuration and save to dataframe
        batch_run.run_all()

        run_data = batch_run.get_model_vars_dataframe()

        # save run data to csv
        run_data.to_csv('../data/experiment/all_scenarios.csv')

        # save every scenerio to seperate csv file
        start = 0
        end = iterations

        for scenario in range(len(parameter_list)):
            run_data[start:end].to_csv('../data/experiment/scenario{}.csv'.format(scenario))
            start += iterations
            end += iterations
