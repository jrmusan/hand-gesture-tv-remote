import pandas as pd
df = pd.read_csv("model/keypoint_classifier/keypoint.csv", header=None)
print(df[0].value_counts())  # shows class balance
