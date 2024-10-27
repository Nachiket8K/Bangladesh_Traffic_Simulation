from model import BangladeshModel
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
"""
Verification test

This test runs the model for 10000 ticks, whereby all bridges are broken down to maximise the amount of data.
Every time a truck reaches a bridge, the delay hte truck will get at the bridge is calculated and saved in 
"delay_at_bridge", a new attribute of the model, along with the bridge's length and category

Here, we separate the bridges by the same length intervals as the assignment for deciding delays. We then plot
the delays of each length category in a histogram. The shape of that histogram allows a visual verification of the delay
distribution in each delay category, thus ensuring that the delays were programmed properly. 
"""

# ---------------------------------------------------------------

run_length = 10000

#set the seed to be the same as the model
seed = 1234567


sim_model = BangladeshModel(seed=seed, prob_A = 1, prob_B = 1, prob_C = 1, prob_D = 1)

# One run with given steps
for i in range(run_length):
    sim_model.step()


# Create dataframe with all delays had at any bridge
df = pd.DataFrame(sim_model.delay_at_bridge, columns=['unique_id','length', 'delay'])

# Divide it by bridge length intervals
df_short_length = df.loc[(df['length'] < 10)]
df_10_50 = df.loc[(df['length'] > 10) & (df['length'] < 50)]
df_50_200 = df.loc[(df['length'] > 50) & (df['length'] < 200)]
df_200_or_more = df.loc[(df['length'] > 200)]

fig, axs = plt.subplots(2,2,figsize=(10,10))

#shortest bridges should have a uniform distribution of delays between 10 and 20 minutes
out1 = pd.cut(df_short_length.delay, bins=[10, 12, 14, 16, 18, 20], include_lowest=True)
out1.value_counts(sort=False).plot(ax=axs[0,0], kind='bar')

#mid-short bridges should have a uniform distribution of delays between 15 and 60 minutes
out2 = pd.cut(df_10_50.delay, bins=np.arange(15,61, 9), include_lowest=True)
out2.value_counts(sort=False).plot(ax=axs[0,1], kind='bar')

#mid-long bridges should have a uniform distribution of delays between 45 and 90 minutes
out3 = pd.cut(df_50_200.delay, bins=np.arange(45,91,9), include_lowest=True)
out3.value_counts(sort=False).plot(ax=axs[1,0], kind='bar')

#long bridges should have a distribution of delays between 60 and 120 minutes, skewed towards 240
#(I think it's an error in the table in the assignment, it should be between 60 and 240, skewed towards 120 imo)
out4 = pd.cut(df_200_or_more.delay, bins=np.arange(60,241,30), include_lowest=True)
out4.value_counts(sort=False).plot(ax=axs[1,1], kind='bar')

# Making the axes nice
axs[0,0].set_xticklabels(['[10,12)', '[12,14)', '[14,16)', '[16,18)', '[18,20]'], rotation=0)
axs[0,0].tick_params(axis='x',labelsize=9)
axs[0,0].set(xlabel="Delay (minutes)", ylabel="Counts")
axs[0,1].set_xticklabels(['[15,24)', '[24,33)', '[33,42)', '[42,51)', '[51,60]'], rotation=0)
axs[0,1].tick_params(axis='x',labelsize=9)
axs[0,1].set(xlabel="Delay (minutes)", ylabel="Counts")
axs[1,0].set_xticklabels(['[45,54)', '[54,63)', '[63,72)', '[72,81)', '[81,90]'], rotation=0)
axs[1,0].tick_params(axis='x',labelsize=9)
axs[1,0].set(xlabel="Delay (minutes)", ylabel="Counts")
axs[1,1].set_xticklabels(['[60,90)', '[90,120)', '[120,150)', '[150,180)', '[180,210)', '[210,240]'], rotation=15)
axs[1,1].tick_params(axis='x',labelsize=9)
axs[1,1].set(xlabel="Delay (minutes)", ylabel="Counts")

plt.savefig("../report/figures/Verification.png")
plt.show()