import numpy as np # linear algebra
import pandas as pd
import os


df = pd.read_parquet ('/home/abhinab/Downloads/clean_data.parquet')
df = df.sample(25000)
df = df.reset_index(drop=True)
df = df.drop_duplicates()

df.to_csv('out.csv') 