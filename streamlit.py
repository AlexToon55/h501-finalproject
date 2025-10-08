import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
df = pd.read_csv("mxmh_survey_results.csv")

# --- Select relevant columns ---
health_cols = ["Anxiety", "Depression", "Insomnia", "OCD"]
genre_cols = [c for c in df.columns if c.startswith("Frequency [")]

# Drop rows with missing key values
df_clean = df.dropna(subset=health_cols + ["Hours per day", "Exploratory", "Music effects"])

# --- Convert frequency columns to numeric (force errors to NaN) ---
df_clean[genre_cols] = df_clean[genre_cols].apply(pd.to_numeric, errors="coerce")

# Convert health columns to numeric as well
df_clean[health_cols] = df_clean[health_cols].apply(pd.to_numeric, errors="coerce")

# --- Create metrics ---
# Variety of genres listened to (count genres with freq > 0)
df_clean["Variety"] = (df_clean[genre_cols] > 0).sum(axis=1)

# Average mental health score (higher = worse problems)
df_clean["Avg_health"] = df_clean[health_cols].mean(axis=1)

# ------------------------------
# 2. Hours Listening vs Health
# ------------------------------
plt.figure(figsize=(8,6))
sns.scatterplot(data=df_clean, x="Hours per day", y="Avg_health", alpha=0.6)
sns.regplot(data=df_clean, x="Hours per day", y="Avg_health", scatter=False, color="red")
plt.title("Does the number of hours listening to music affect health problems?")
plt.xlabel("Hours per day")
plt.ylabel("Average mental health score")
plt.show()

# ------------------------------
# 3. Exploratory vs Mental Health Effects
# ------------------------------
plt.figure(figsize=(8,6))
sns.countplot(data=df_clean, x="Music effects", hue="Exploratory")
plt.title("Exploring new genres/artists vs reported effects on mental health")
plt.xlabel("Reported effects of music")
plt.ylabel("Number of respondents")
plt.xticks(rotation=20)
plt.show()
