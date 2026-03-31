import os
import pandas as pd

resume_folder = "resumes_text"

data = []

for file in os.listdir(resume_folder):

    path = os.path.join(resume_folder, file)

    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read().lower()

    # ---------- Extract Candidate Name ----------
    lines = text.split("\n")
    candidate_name = ""

    for line in lines[:10]:
        line = line.strip()

        if len(line) > 3 and len(line) < 40:
            if not any(word in line for word in ["resume","cv","email","phone","contact"]):
                candidate_name = line
                break

    if candidate_name == "":
        candidate_name = file.replace(".txt","")

    # ---------- Skills ----------
    skills_keywords = [
        "python","sql","excel","power bi","tableau",
        "html","css","javascript","react","node",
        "photoshop","figma","illustrator","canva"
    ]

    skills_found = [skill for skill in skills_keywords if skill in text]

    # ---------- Tools ----------
    tools_keywords = [
        "power bi","tableau","figma","canva",
        "photoshop","excel","git"
    ]

    tools_found = [tool for tool in tools_keywords if tool in text]

    # ---------- Education ----------
    education = ""

    if "b.tech" in text or "btech" in text:
        education = "B.Tech"
    elif "bca" in text:
        education = "BCA"
    elif "mca" in text:
        education = "MCA"
    elif "bsc" in text:
        education = "B.Sc"

    # ---------- Projects ----------
    projects = "mentioned" if "project" in text else ""

    # ---------- Experience ----------
    experience = "mentioned" if "experience" in text or "internship" in text else ""

    # ---------- Certification ----------
    certification = "mentioned" if "certification" in text or "certificate" in text else ""

    data.append({
        "Candidate_Name": candidate_name,
        "Education": education,
        "Skills": ", ".join(skills_found),
        "Tools": ", ".join(tools_found),
        "Past_Projects": projects,
        "Experience": experience,
        "Certification": certification
    })

df = pd.DataFrame(data)

# Ensure dataset folder exists
os.makedirs("dataset", exist_ok=True)

df.to_excel("dataset/resume_dataset.xlsx", index=False)

print("✅ Dataset created successfully!")