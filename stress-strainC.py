import pandas as pd
import matplotlib.pyplot as plt

# User input for Test Number
test_num = int(input("Enter Test Number [e.g., 2, 3, 4...]: "))

# Reading data from CSV file
file_path = f'/Users/parshvamehta/Downloads/testC/{test_num}C.csv'
df = pd.read_csv(file_path)
df.drop(df.index[:1], inplace=True)


L = 0.0467  
b = 0.0508
original_length_mm = 46.7 
thickness_tracker = [0.124,0.163,0.035,0.31,0.286,0.286,0,0,0,0.154,0,0.158,0.164,0.284,0.289,0,0.3,0.31,0.299,0.288,0.325,0.299,0.283,0,0.283,0.274,0,0.307,0,0.101,0,0.03,0.035,0,0.031,0.022,0,0,0,0,0.05,0.046,0.049]
t = thickness_tracker[test_num-1]

# Normalize displacement and force
df['Displacement'] = pd.to_numeric(df['Displacement'], errors='coerce')
df['Displacement'] -= df['Displacement'].iloc[0]

df['Force'] = pd.to_numeric(df['Force'], errors='coerce')
df['Force'] -= df['Force'].iloc[0]

df['Stress'] = ((3 * df['Force'] * L) / (2 * b * t**2)) / 1e6
df['Strain'] = df['Displacement'] / original_length_mm

max_stress_Pa = df['Stress'].max()
max_stress_MPa = max_stress_Pa / 1e6
strain_at_break = df.loc[df['Stress'].idxmax(), 'Strain']
elastic_modulus_GPa = (max_stress_MPa / strain_at_break) / 1000

print("--------------------------------------------------")
print("Thickness Used: " + str(t))
print(f"Maximum Stress (MPa) - Flexural strength: {max_stress_MPa}")
print(f"Strain at Break - Epsilon Fracture: {strain_at_break}")
print(f"Flexural Elastic Modulus (GPa): {elastic_modulus_GPa}")
print("--------------------------------------------------")

plt.figure(figsize=(10, 6))
plt.plot(df['Strain'], df['Stress'], marker='o', color='b')
plt.title(f"Stress-Strain Curve: Test-{test_num}C")
plt.xlabel('Strain')
plt.ylabel('Stress (MPa)')
plt.grid(True)
plt.show()

