import streamlit as st
import pandas as pd
import random

# Charger les questions
df = pd.read_csv("questions.csv")

# Sélection catégorie et nombre
categories = df['category'].unique()
selected_categories = st.multiselect("Choisir une ou plusieurs catégories", categories, default=list(categories)[:1])
filtered_df = df[df['category'].isin(selected_categories)]
max_questions = len(filtered_df)

if max_questions == 0:
    st.markdown("<span style='color:#2563eb; font-weight:bold;'>Aucune question disponible pour cette sélection.</span>", unsafe_allow_html=True)
    st.stop()
elif max_questions == 1:
    st.markdown("<span style='color:#2563eb; font-weight:bold;'>Une seule question disponible dans cette sélection.</span>", unsafe_allow_html=True)
    num_questions = 1
else:
    num_questions = st.slider("Nombre de questions", 1, max_questions, min(3, max_questions))

# Initialisation des questions dans la session
if 'questions' not in st.session_state or st.session_state.get('last_categories') != selected_categories or st.session_state.get('last_num_questions') != num_questions:
    if max_questions > 0:
        st.session_state.questions = filtered_df.sample(n=num_questions).reset_index(drop=True)
        st.session_state.last_categories = selected_categories.copy()
        st.session_state.last_num_questions = num_questions

questions = st.session_state.questions

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
    # Formatage plus lisible
    option_labels = [f"{key}. {value}" for key, value in options.items()]
    option_keys = list(options.keys())
    answer_label = st.radio("Choix :", option_labels, key=row['id'])
    answer = option_keys[option_labels.index(answer_label)]
    if st.button(f"Valider la réponse à la question {row['id']}", key=f"btn_{row['id']}", type="primary"):
        if answer == row['correct']:
            st.success("✅ Bonne réponse !")
            score += 1
        else:
            st.markdown(
                f"<span style='color:#2563eb; font-weight:bold;'>❌ Mauvaise réponse. "
                f"La bonne réponse était : {row['correct']} - {options[row['correct']]}</span>",
                unsafe_allow_html=True
            )

st.markdown("---")
st.subheader(f"Score final : {score}/{num_questions}")
