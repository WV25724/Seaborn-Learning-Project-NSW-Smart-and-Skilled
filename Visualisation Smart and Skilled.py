import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Read Excel
df = pd.read_excel(
    'smart-skilled-commencements.xlsx',
    sheet_name=8,
    skiprows=2
)

# Clean column names
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

# Remove duplicate rows
df = df.drop_duplicates()

# Melt the data 
df_melted = df.melt(id_vars='gender', var_name='year', value_name='commencements')

# Remove commas, dollar signs, spaces, and convert to numeric
df_melted['commencements'] = (
    df_melted['commencements']
    .astype(str)                    
    .str.replace(',', '', regex=False)
    .str.replace('$', '', regex=False)
    .str.strip()
)

# Convert to number (NaN if invalid)
df_melted['commencements'] = pd.to_numeric(df_melted['commencements'], errors='coerce')

# Make sure year is string (for x-axis labels)
df_melted['year'] = df_melted['year'].astype(str)

# Drop any rows where we couldn't convert commencements
df_melted = df_melted.dropna(subset=['commencements'])

# --- PLOT ---
plt.figure(figsize=(12, 6))
sns.barplot(
    x='year',
    y='commencements',
    hue='gender',
    data=df_melted,
    palette='Set2'
)
plt.title('Commencements by Gender and Year')
plt.xlabel('Year')
plt.ylabel('Number of Commencements')
plt.xticks(rotation=45)
plt.legend(title='Gender')
plt.ylim(0, df_melted['commencements'].max() * 1.1) 
plt.yticks(range(0, int(df_melted['commencements'].max()) + 25000, 25000))

plt.tight_layout()
plt.show()


