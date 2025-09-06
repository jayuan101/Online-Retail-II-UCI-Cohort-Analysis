import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv('data/online_retail.csv', encoding='unicode_escape')

# Data preprocessing
df = df[df['CustomerID'].notnull()]
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
df['CohortMonth'] = df['InvoiceDate'].dt.to_period('M')

# Calculate cohort index
df['CohortIndex'] = (df['InvoiceDate'].dt.year - df['InvoiceDate'].dt.year.min()) * 12 + (df['InvoiceDate'].dt.month - df['InvoiceDate'].dt.month.min())

# Aggregate data
cohort_data = df.groupby(['CohortMonth', 'CohortIndex']).agg(
    active_customers=('CustomerID', 'nunique'),
    revenue=('UnitPrice', 'sum')
).reset_index()

# Calculate retention rates
cohort_sizes = cohort_data[cohort_data['CohortIndex'] == 0][['CohortMonth', 'active_customers']]
cohort_sizes.rename(columns={'active_customers': 'cohort_size'}, inplace=True)
cohort_data = cohort_data.merge(cohort_sizes, on='CohortMonth')
cohort_data['retention'] = cohort_data['active_customers'] / cohort_data['cohort_size']

# Pivot for heatmap
retention_matrix = cohort_data.pivot(index='CohortMonth', columns='CohortIndex', values='retention')

# Plot heatmap
plt.figure(figsize=(12, 8))
sns.heatmap(retention_matrix, annot=True, fmt='.0%', cmap='Blues')
plt.title('Customer Retention Cohort Analysis')
plt.xlabel('Months Since First Purchase')
plt.ylabel('Cohort Month')
plt.show()
