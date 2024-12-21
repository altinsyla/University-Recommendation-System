import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('universitites-dataset.csv')
df = pd.DataFrame(data)

pivot_df = df.pivot(index="year", columns="university_degree", values="number_of_students")

pivot_df.plot(kind="line", marker="o", figsize=(10, 6))

plt.title("Number of Students Over Years by University Degree")
plt.xlabel("Year")
plt.ylabel("Number of Students")
plt.legend(title="Degree")
plt.grid(True)

plt.show()