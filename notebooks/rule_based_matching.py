import pandas as pd

# Load datasets
candidate_df = pd.read_excel("dataset/resume_dataset.xlsx")
role_df = pd.read_excel("dataset/role_skill_matrix.xlsx")

results = []

for _, candidate in candidate_df.iterrows():

    candidate_name = candidate["Candidate_Name"]
    candidate_skills = str(candidate["Skills"]).lower().split(",")

    candidate_skills = [skill.strip() for skill in candidate_skills]

    for _, role in role_df.iterrows():

        role_name = role["Role"]
        role_skills = role["Required_Skills"].lower().split(",")

        role_skills = [skill.strip() for skill in role_skills]

        matched = len(set(candidate_skills) & set(role_skills))
        total = len(role_skills)

        match_percentage = round((matched / total) * 100, 2)

        # Fit category thresholds
        if match_percentage >= 70:
            fit_category = "Strong Fit"
        elif match_percentage >= 40:
            fit_category = "Moderate Fit"
        else:
            fit_category = "Low Fit"

        results.append({
            "Candidate_Name": candidate_name,
            "Role": role_name,
            "Match_Percentage": match_percentage,
            "Fit_Category": fit_category
        })

result_df = pd.DataFrame(results)

# Save results
result_df.to_excel("dataset/candidate_role_match.xlsx", index=False)

print("Rule-based matching with fit categories completed!")