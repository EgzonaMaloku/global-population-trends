from scipy.spatial.distance import minkowski

# Example: Two data points
point1 = [2, 4, 6]
point2 = [1, 3, 5]
p = 3  # Parameter p

# Calculate Minkowski distance
distance = minkowski(point1, point2, p)
print("Minkowski Distance (p=3):", distance)