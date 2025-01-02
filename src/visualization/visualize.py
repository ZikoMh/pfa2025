import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from IPython.display import display

# --------------------------------------------------------------
# Load data
# --------------------------------------------------------------

df = pd.read_pickle("C:\Users\USER\desktop\pfa2025\dataScience\data\interim\data_resampled.pkl")
# --------------------------------------------------------------
# Plot single columns
# --------------------------------------------------------------
df_set = df[df["set"]==1]
plt.plot(df_set["acc_x"], label="acc_x")

# --------------------------------------------------------------
# Plot all exercises
# --------------------------------------------------------------
for label in df["label"].unique():
    subest = df[df["label"]==label]
    fig , ax = plt.subplots()
    plt.plot(subest["acc_y"].reset_index(drop=True), label=label)
    plt.legend()
    plt.show()
  
# --------------------------------------------------------------
# Adjust plot settings
# --------------------------------------------------------------
mpl.style.use["seaborn-v0_8-deep"]
mpl.rcParams["figure.figsize"] = (20,5)
mpl.rcParams["figure.dpi"] = 100

# --------------------------------------------------------------
# Compare medium vs. heavy sets
# --------------------------------------------------------------


# --------------------------------------------------------------
# Compare participants
# --------------------------------------------------------------


# --------------------------------------------------------------
# Plot multiple axis
# --------------------------------------------------------------


# --------------------------------------------------------------
# Create a loop to plot all combinations per sensor
# --------------------------------------------------------------


# --------------------------------------------------------------
# Combine plots in one figure
# --------------------------------------------------------------


# --------------------------------------------------------------
# Loop over all combinations and export for both sensors
# --------------------------------------------------------------