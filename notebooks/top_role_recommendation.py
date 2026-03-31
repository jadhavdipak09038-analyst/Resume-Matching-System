import pandas as pd

# Load matching results
df = pd.read_excel("dataset/candidate_role_match.xlsx")

# Sort roles by match percentage
df_sorted = df.sort_values(["Candidate_Name", "Match_Percentage"], ascending=[True, False])

# Get top 3 roles for each candidate
top_roles = df_sorted.groupby("Candidate_Name").head(3)

# Save results
top_roles.to_excel("dataset/top_role_recommendations.xlsx", index=False)

print("Top role recommendations created successfully!")