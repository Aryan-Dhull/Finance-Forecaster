from sklearn.cluster import KMeans

num_clusters = 4
kmeans = KMeans(n_clusters=num_clusters, random_state=42)
kmeans.fit(Dataset[columns_for_kmeans])

cluster_labels = kmeans.labels_
Dataset['Cluster'] = cluster_labels

print("Data points in each cluster:")
print(Dataset['Cluster'].value_counts())

feature1 = 'Low'
feature2 = 'High'

plt.figure(figsize=(8, 6))

for cluster_label in range(num_clusters):
    cluster_data = Dataset[Dataset['Cluster'] == cluster_label]
    plt.scatter(cluster_data[feature1], cluster_data[feature2], label=f'Cluster {cluster_label}', alpha=0.6)

cluster_centers = kmeans.cluster_centers_
plt.scatter(cluster_centers[:, columns_to_standardize.index(feature1)],
            cluster_centers[:, columns_to_standardize.index(feature2)],
            marker='x', s=200, linewidths=3, color='k', label='Cluster Centers')

plt.xlabel(feature1)
plt.ylabel(feature2)
plt.title('K-means Clustering')
plt.legend()
plt.show()
