from sklearn.metrics import jaccard_score

# Example: Two binary vectors
vec1 = [1, 0, 1, 0, 1]
vec2 = [1, 1, 1, 0, 0]

# Calculate Jaccard index
jaccard = jaccard_score(vec1, vec2, average='binary')
print("Jaccard Index:", jaccard)