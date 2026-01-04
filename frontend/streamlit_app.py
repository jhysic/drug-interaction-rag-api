import requests
import streamlit as st

API_URL = "http://localhost:8000/analyze"

st.title("Drug–Genetics Interaction RAG Demo")

meds = st.text_area("Medications (comma-separated)")
genotype = st.text_area("Genotype / variants (free text or JSON)")
question = st.text_input("Question", "Is this regimen safe?")

if st.button("Analyze"):
    payload = {
        "medications": [m.strip() for m in meds.split(",") if m.strip()],
        "genotype": genotype,
        "question": question,
    }
    resp = requests.post(API_URL, json=payload)
    # 응답(JSON)을 요약, 테이블 등으로 표시
