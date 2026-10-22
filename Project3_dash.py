import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import(accuracy_score,classification_report,confusion_matrix)

df = pd.read_csv(r"D:\Vscode\Project_3\Job_placement_cleaneddata.csv")

X=df.drop(columns=["status"])
y=df["status"]
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.20,random_state=42,stratify=y)
random_forest_model = RandomForestClassifier(n_estimators=100,max_depth=15,random_state=42)
random_forest_model.fit(X_train, y_train)
forest_predictions = random_forest_model.predict(X_test)
print("Random Forest completed")
forest_accuracy = accuracy_score(y_test,forest_predictions)
print("Random Forest Accuracy:", round(forest_accuracy, 4))
print("Accuracy Percentage:", round(forest_accuracy * 100, 2), "%")
print("Random Forest Classification Report")
print(classification_report(y_test,forest_predictions,labels=[0, 1],target_names=["Not Placed", "Placed"],zero_division=0))
forest_cm = confusion_matrix(y_test,forest_predictions,labels=[0, 1])
print("Random Forest Confusion Matrix")
print(forest_cm)

st.subheader("HR Job Placement Analytics Dashboard")
st.markdown("### Key Performance Indicators")

if "status" not in df.columns:
    st.error("The dataset does not contain a status column.")
    st.stop()

df["status"] = (df["status"].astype("string").str.strip().str.lower())
total_candidates = len(df)

if df["status"].isin(["placed", "not placed"]).any():
    placed_count = df["status"].eq("placed").sum()

elif df["status"].isin(["0", "1"]).all():
    placed_count = df["status"].eq("1").sum()

else:
    placed_count = 0
    st.warning("Check the status values. "
        "Some values may not match the expected labels.")
    st.write("Status values:",df["status"].value_counts(dropna=False).to_dict())
placement_rate = (placed_count / total_candidates * 100
    if total_candidates > 0 else 0)

if "job_offer_status" in df.columns:
    offer_status = (df["job_offer_status"].astype("string").str.strip().str.lower())
    valid_offers = offer_status.isin(["accepted", "rejected", "dropped", "declined"])
    accepted_count = offer_status.eq("accepted").sum()
    offer_count = valid_offers.sum()
    job_acceptance_rate = (accepted_count / offer_count * 100
        if offer_count > 0 else np.nan)
else:
    job_acceptance_rate = np.nan


score_columns = ["technical_score","aptitude_score","communication_score"]
average_score = (df[score_columns].apply(pd.to_numeric, errors="coerce").stack().mean())

if "skills_match_percentage" in df.columns:
    skills_match = pd.to_numeric(df["skills_match_percentage"], errors="coerce")
    avg_skills_match = skills_match.mean()
else:
    avg_skills_match = np.nan

if "job_offer_status" in df.columns:
    offer_status = (df["job_offer_status"].astype("string").str.strip().str.lower())
    decided_offers = offer_status.isin(["accepted", "dropped"])
    dropout_count = offer_status.eq("dropped").sum()
    decided_count = decided_offers.sum()
    offer_dropout_rate = (dropout_count / decided_count * 100
        if decided_count > 0 else np.nan)
else:
    offer_dropout_rate = np.nan

probabilities = random_forest_model.predict_proba(X_test)
classes = list(random_forest_model.classes_)
placed_class_index = classes.index(1)
placement_probabilities = probabilities[:, placed_class_index]
high_risk_count = (placement_probabilities < 0.30).sum()
high_risk_percentage = (high_risk_count / len(X_test) * 100
    if len(X_test) > 0 else np.nan)

def format_percent(value):
    return f"{value:.2f}%" if pd.notna(value) else "N/A"

def format_number(value):
    return f"{value:.2f}" if pd.notna(value) else "N/A"

kpi_values = [
    ("Total Candidates", f"{total_candidates:,}"),
    ("Placement Rate", format_percent(placement_rate)),
    ("Job Acceptance Rate", format_percent(job_acceptance_rate)),
    ("Average Interview Score", format_number(average_score)),
    ("Average Skills Match", format_percent(avg_skills_match)),
    ("Offer Dropout Rate", format_percent(offer_dropout_rate)),
    ("High-Risk Candidate Percentage",format_percent(high_risk_percentage))]

for start in range(0, len(kpi_values), 4):
    row = kpi_values[start:start + 4]
    cols = st.columns(len(row))

    for col, (label, value) in zip(cols, row):
        col.metric(label, value)

st.balloons()
st.write("Project completed Sucessfully")