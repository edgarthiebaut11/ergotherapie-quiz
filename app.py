import streamlit as st
import pandas as pd
import random

# Charger les questions
df = pd.read_csv("questions.csv")

# Sélection catégorie et nombre
categories = df['category'].unique()
selected_category = st.selectbox("Choisir une catégorie", categories)
num_questions = st.slider("Nombre de questions", 1, 10, 3)

# Filtrage
questions = df[df['category'] == selected_category].sample(n=num_questions)

# Stats
score = 0

st.title("Quiz d'Ergothérapie")

for i, row in questions.iterrows():
    st.subheader(f"Q: {row['question']}")
    options = {
        'A': row['option_a'],
        'B': row['option_b'],
        'C': row['option_c'],
        'D': row['option_d'],
    }
    answer = st.radio("Choix :", list(options.items()), key=row['id'])
    if st.button(f"Valider la réponse à la question {row['id']}", key=f"btn_{row['id']}"):
        if answer[0] == row['correct']:
            st.success("✅ Bonne réponse !")
            score += 1
        else:
            st.error(f"❌ Mauvaise réponse. La bonne réponse était : {row['correct']} - {options[row['correct']]}")

st.markdown("---")
st.subheader(f"Score final : {score}/{num_questions}")
