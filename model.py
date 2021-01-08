import pandas as pd
import pickle
from sklearn.cluster import KMeans
import math


latlong_df = pd.read_csv("./latlongfinal.csv")

features = latlong_df.iloc[:, [2,3]]

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

