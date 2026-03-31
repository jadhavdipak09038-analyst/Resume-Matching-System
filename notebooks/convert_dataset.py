import pandas as pd

# Load your raw dataset
df = pd.read_excel("dataset/your_raw_dataset.xlsx")

data = []

for _, row in df.iterrows():

    # ---------- EDUCATION (FIXED) ----------
    degree = str(row["Degree"]).lower()

    if "b.tech" in degree or "bachelor of technology" in degree:
        education = "B.Tech"
    elif "bsc" in degree:
        education = "B.Sc"
    elif "bca" in degree:
        education = "BCA"
    elif "mca" in degree:
        education = "MCA"
    else:
        education = row["Degree"]

    # ---------- COMBINE SKILLS ----------
    skills = [
        str(row["Skill 1"]),
        str(row["Skill 2"]),
        str(row["Programming Language 1"]),
        str(row["Programming Language 2"]),
        str(row["Programming Language 3"]),
        str(row["Programming Language 4"]),
        str(row["Programming Language 5"])
    ]

    skills = [s.lower() for s in skills if s != "N/A" and s != "nan"]

    # ---------- COMBINE TOOLS ----------
    tools = [
        str(row["Tool 1"]),
        str(row["Tool 2"]),
        str(row["Tool 3"]),
        str(row["Tool 4"]),
        str(row["Tool 5"])
    ]

    tools = [t.lower() for t in tools if t != "N/A" and t != "nan"]

    # ---------- PROJECTS ----------
    projects = "mentioned" if pd.notna(row["Past Projects"]) else ""

    # ---------- EXPERIENCE ----------
    experience = "mentioned" if pd.notna(row["Experience"]) else ""

    # ---------- CERTIFICATION ----------
    certification = "mentioned" if pd.notna(row["Certifications"]) else ""

    # ---------- FINAL ROW ----------
    data.append({
        "Candidate_Name": row["Candidate Name"],
        "Education": education,
        "Skills": ", ".join(skills),
        "Tools": ", ".join(tools),
        "Past_Projects": projects,
        "Experience": experience,
        "Certification": certification
    })

# ---------- SAVE ----------
new_df = pd.DataFrame(data)
new_df.to_excel("dataset/resume_dataset.xlsx", index=False)

print("✅ Dataset converted successfully!")