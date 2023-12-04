import pandas as pd
import matplotlib.pyplot as plt
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler


def load_data(filepath):
    try:
        df = pd.read_csv(filepath)
        print(f'Dataframe shape: {df.shape}')
        print(f'Dataframe columns: {df.columns.tolist()}')
        df.info()
        return df

    except Exception as e:
        print(f'Error Loading data: {e}')
    return None

filepath = "data/attack-sample.csv"
df = load_data(filepath)

df = joblib.load('data/df_chosen_features.csv')

print(df.head(10))

# Checking for missing values
# Calculate the percentage of missing values for each column
missing_percentage = df.isnull().sum() * 100 / len(df)

# Categorize columns based on missing value percentages
missing_categories = {
    "0-20%": missing_percentage[(missing_percentage > 0) & (missing_percentage <= 20)].index.tolist(),
    "20-40%": missing_percentage[(missing_percentage > 20) & (missing_percentage <= 40)].index.tolist(),
    "40-60%": missing_percentage[(missing_percentage > 40) & (missing_percentage <= 60)].index.tolist(),
    "60-80%": missing_percentage[(missing_percentage > 60) & (missing_percentage <= 80)].index.tolist(),
    "80-100%": missing_percentage[(missing_percentage > 80) & (missing_percentage <= 100)].index.tolist()
}

# Print out the categorized lists
for category, features in missing_categories.items():
    print(f"{category} Missing Values: {features}")


# I would like to now gain more insight about the tcp and udp proportion in the df
# Check for rows where both udp.srcport and tcp.srcport are non-null
both_set = df[(df['udp.srcport'].notnull()) & (df['tcp.srcport'].notnull())]
print(f"Number of rows with both UDP and TCP source ports set: {len(both_set)}")

both_null_count = df[(df['udp.srcport'].isnull()) & (df['tcp.srcport'].isnull())].shape[0]
print(f"Number of rows with both TCP and UDP source ports null: {both_null_count}")

# Count of non-null values in udp.srcport
udp_srcport_count = df['udp.srcport'].notnull().sum()

# Count of non-null values in tcp.srcport
tcp_srcport_count = df['tcp.srcport'].notnull().sum()

# Print the counts
print(f"Number of rows with non-null UDP source port: {udp_srcport_count}")
print(f"Number of rows with non-null TCP source port: {tcp_srcport_count}")

# There is a feature called "frame.protocols" which has the list of all protocols used
# in the packet. I'd like to see the variety of protocols in the dataset. To visualize
# the frame.protocols feature from the dataset as a histogram, I first need to break
# down these lists into individual protocols and then count their occurrences.

# Split the 'frame.protocols' entries into individual protocols and stack them
protocols = df['frame.protocols'].str.split(':', expand=True).stack()

# Count the occurrences of each protocol
protocol_counts = protocols.value_counts()

# Plotting
plt.figure(figsize=(12, 6))
protocol_counts.plot(kind='bar')
# Format y-axis to show actual numbers
plt.title('Histogram of Protocols')
plt.xlabel('Protocol')
plt.ylabel('Count')
# plt.xticks(rotation=45)
plt.show()

# Print the top 10 protocols with their counts
print(protocol_counts.head(10))

columns_to_keep = ['tcp.srcport', 'tcp.dstport','tcp.len', 'tcp.window_size', 'tcp.flags.syn'  ]
df = df[columns_to_keep]

joblib.dump(df,'data/df_chosen_features.csv')

#  From now on I'll work on this df :
#  df = joblib.load('data/df_chosen_features.csv')

df.info()
#  Don't have missing data
#  Will need to visualise the distribution of the data

df.hist(bins=15, figsize=(15, 10))
plt.show()

features = df.columns.tolist()

for feature in features:
    plt.figure(figsize=(10, 6))
    sns.histplot(df[feature], kde=True, stat="density", linewidth=0)

    # Calculate mean and standard deviation
    mean_value = df[feature].mean()
    std_deviation = df[feature].std()

    # Plot vertical lines for mean and std deviation
    plt.axvline(mean_value, color='r', linestyle='--', label=f'Mean: {mean_value:.2f}')
    plt.axvline(mean_value + std_deviation, color='g', linestyle=':', label=f'Std Dev: {std_deviation:.2f}')
    plt.axvline(mean_value - std_deviation, color='g', linestyle=':')

    plt.title(f'Distribution of {feature}')
    plt.legend()
    plt.show()

#  I would like to scale the features then plot them again
scaler = StandardScaler()
df_scaled = pd.DataFrame(scaler.fit_transform(df[features]), columns = features)

for feature in features:
    plt.figure(figsize=(10, 6))
    sns.histplot(df[feature], kde=True, stat="density", linewidth=0)

    # Calculate mean and standard deviation
    mean_value = df[feature].mean()
    std_deviation = df[feature].std()

    # Plot vertical lines for mean and std deviation
    plt.axvline(mean_value, color='r', linestyle='--', label=f'Mean: {mean_value:.2f}')
    plt.axvline(mean_value + std_deviation, color='g', linestyle=':', label=f'Std Dev: {std_deviation:.2f}')
    plt.axvline(mean_value - std_deviation, color='g', linestyle=':')

    plt.title(f'Distribution of {feature}')
    plt.legend()
    plt.show()

#  I cannot see a clean Gaussian distribution in any of the features.

#  I would like to see the pairplot of the feature to see if anything stands out.
sns.pairplot(df)
plt.show()


# Boxplot for outlier detection
df.plot(kind='box', subplots=True, layout=(2,3), figsize=(15, 10))
plt.show()

#  Let's proceed with the corelation analysis of the features
# Correlation matrix
corr_matrix = df.corr()
plt.figure(figsize=(8, 6))
sns.heatmap(corr_matrix, annot=True, cmap='cividis')
plt.title('Correlation Matrix')
plt.show()