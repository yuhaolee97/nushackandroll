import pandas as pd
import pickle
from sklearn.cluster import KMeans
import math


latlong_df = pd.read_csv("./latlongs.csv")

latlong_df = pd.concat([latlong_df[['Address']], latlong_df['Cusines'], latlong_df['Restaurant'], latlong_df['Coordinates'].str.split(', ', expand=True)], axis=1)
latlong_df.rename(columns={0: 'Latitude', 1: 'Longitude'}, inplace=True)
latlong_df.head()

latlong_df.isnull().sum()

features = latlong_df.iloc[:, [3,4]]

new_features = pd.DataFrame()

new_features['Latitude'] = features['Latitude'].astype(float)
new_features['Longitude'] = features['Longitude'].astype(float)


km = KMeans(n_clusters = 50, init = 'k-means++', max_iter = 300, random_state = 234)
y_means = km.fit_predict(new_features)
print(y_means)

latlong_df['Clusters'] = y_means.astype(str)

pickle.dump(km, open("save.pkl", "wb"))

latlong_df.to_csv("updatedlatlong.csv")


# import plotly.graph_objects as go
# import plotly_express as px

# fig = px.scatter(latlong_df, x="Longitude", y="Latitude", color='Clusters')

# fig.add_trace(go.Scatter(x=km.cluster_centers_[:,0], y=km.cluster_centers_[:, 1],
#                     mode='markers',
#                     name='Centroid', 
#                     marker_color='rgba(0, 0, 0, .9)'))

# fig.show()

