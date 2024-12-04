import numpy as np

# Example: Two binary vectors
vec1 = [1, 0, 1, 0, 1]
vec2 = [1, 1, 1, 0, 0]

# Calculate SMC
a = np.sum(np.logical_and(vec1, vec2))  # Both 1
d = np.sum(np.logical_not(np.logical_xor(vec1, vec2)))  # Both 0
smc = (a + d) / len(vec1)
print("Simple Matching Coefficient (SMC):", smc)