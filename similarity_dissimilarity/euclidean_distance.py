from scipy.spatial.distance import euclidean

# Example: Two data points
point1 = [2, 4, 6]
point2 = [1, 3, 5]

# Calculate Euclidean distance
distance = euclidean(point1, point2)
print("Euclidean Distance:", distance)