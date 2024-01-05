import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

###
# This script calculates the maximum stress, strain at break, and tensile elastic modulus
# Test numbers: 1,2,3,4,21,22,23,25,26,28
# Test numbers 6-20 are not included because weight not given
# Changes with each test: thickness, original length, graph title
###


test_num = input("Enter Test Number [1,2,3,4,21,22,23,25,26,28]: ")
df = pd.read_csv(f'/Users/parshvamehta/Downloads/tests/{test_num}A/Test1/Test1.Stop.csv')
thickness_arr = [0.124, 0.163, 0.035, 0.31, 0.286, 0.286, 0, 0, 0, 0.154, 0, 0.158, 0.164, 0.284, 0.289, 0, 0.3, 0.31, 0.299, 0.288, 0.325, 0.299, 0.283, 0, 0.283, 0.274, 0, 0.307]


# Normalize Load and Position by subtracting their initial values
df['Load(8800 (0,3):Load) (kN)'] -= df['Load(8800 (0,3):Load) (kN)'].iloc[0]
df['Position(8800 (0,3):Position) (mm)'] -= df['Position(8800 (0,3):Position) (mm)'].iloc[0]

# Convert Load from kilonewtons to newtons
df['Load(8800 (0,3):Load) (kN)'] *= 1000

thickness = thickness_arr[int(test_num) - 1]
if(thickness == 0):
    print("Thickness Not Given") 
print("Thickness Used: " + str(thickness))
width = 1

# Convert cross-sectional area from square inches to square meters (1 inch = 0.0254 meters)
area = thickness * width * (0.0254**2)  # Area in square meters

# Convert Load values to Stress values (Pascals) --> MPa
df['Stress'] = (df['Load(8800 (0,3):Load) (kN)'] / area) / 1e6

original_length = 203.2

# Convert Position to Strain (in percent)
df['Strain'] = (df['Position(8800 (0,3):Position) (mm)'] / original_length)

# Extract the maximum stress value --> Convert to MPa
max_stress = df['Stress'].max()

# Find the strain at break (epsilon_frac)
strain_at_break = df.loc[df['Stress'].idxmax(), 'Strain']

# Calculate the approximate tensile elastic modulus (E) -->  GPa
elastic_modulus = (max_stress / strain_at_break) / 1000

print("--------------------------------------------------")
print("Maximum Stress (MPa):", max_stress)
print("Elastic Modulus (GPa):", elastic_modulus)
print("Strain at Break (%):", (strain_at_break * 100))
print("--------------------------------------------------")

# Graphing
plt.figure(figsize=(10, 6))
plt.plot(df['Strain'], df['Stress'], marker='o', color='b')
title = f"Stress-Strain Curve: Test-{test_num}A"
plt.title(title)
plt.xlabel('Strain')
plt.ylabel('Stress (MPa)')
plt.grid(True)
plt.show()