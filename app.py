import streamlit as st
import pandas as pd
import random

# Charger les questions
df = pd.read_csv("questions.csv")

# Sélection catégorie et nombre
categories = sorted(df['category'].unique())
selected_categories = st.multiselect(
    "Choisir une ou plusieurs catégories",
    categories,
    default=categories[:1]
)
filtered_df = df[df['category'].isin(selected_categories)]
max_questions = len(filtered_df)

if max_questions == 0:
    st.markdown("<span style='color:#2563eb; font-weight:bold;'>Aucune question disponible pour cette sélection.</span>", unsafe_allow_html=True)
    st.stop()
elif max_questions == 1:
    st.markdown("<span style='color:#2563eb; font-weight:bold;'>Une seule question disponible dans cette sélection.</span>", unsafe_allow_html=True)
    num_questions = 1
else:
    num_questions = st.slider("Nombre de questions", 1, max_questions, max_questions)

# Initialisation des questions dans la session
if 'questions' not in st.session_state or st.session_state.get('last_categories') != selected_categories or st.session_state.get('last_num_questions') != num_questions:
    if max_questions > 0:
        st.session_state.questions = filtered_df.sample(n=num_questions).reset_index(drop=True)
        st.session_state.last_categories = selected_categories.copy()
        st.session_state.last_num_questions = num_questions

# Initialisation de l'index de question dans la session
if 'question_idx' not in st.session_state:
    st.session_state.question_idx = 0

questions = st.session_state.questions
num_questions = len(questions)

# Navigation
col1, col2, col3 = st.columns([1, 6, 1])
with col1:
    if st.button("⬅️", key="prev") and st.session_state.question_idx > 0:
        st.session_state.question_idx -= 1
with col3:
    if st.button("➡️", key="next") and st.session_state.question_idx < num_questions - 1:
        st.session_state.question_idx += 1

row = questions.iloc[st.session_state.question_idx]
st.subheader(f"Question {st.session_state.question_idx + 1} / {num_questions} — {row['category']}")
st.write(f"**{row['question']}**")

options = {
    'A': row['option_a'],
    'B': row['option_b'],
    'C': row['option_c'],
    'D': row['option_d'],
}
option_labels = [f"{key}. {value}" for key, value in options.items()]
option_keys = list(options.keys())

correct_answers = [x.strip() for x in str(row['correct']).replace(',', ';').split(';') if x.strip()]
answered = st.session_state.get(f"answered_{st.session_state.question_idx}", None)
validated = st.session_state.get(f"validated_{st.session_state.question_idx}", False)

if len(correct_answers) == 1:
    # Question à réponse unique : boutons radio (ronds)
    answer_label = st.radio(
        "Choix :",
        option_labels,
        key=f"radio_{st.session_state.question_idx}",
        index=option_labels.index(f"{answered[0]}. {options[answered[0]]}") if answered else 0,
        disabled=validated
    )
    answer = option_keys[option_labels.index(answer_label)]
    selected_keys = [answer]
else:
    # Question à réponses multiples : cases à cocher (carrés)
    selected_keys = []
    for key, label in zip(option_keys, option_labels):
        checked = answered and key in answered
        st.checkbox(
            label,
            key=f"chk_{st.session_state.question_idx}_{key}",
            value=checked,
            disabled=validated
        )
        if st.session_state.get(f"chk_{st.session_state.question_idx}_{key}", False):
            selected_keys.append(key)

if not validated:
    if st.button(f"Valider la réponse à la question", key=f"btn_{st.session_state.question_idx}", type="primary"):
        st.session_state[f"answered_{st.session_state.question_idx}"] = selected_keys
        st.session_state[f"validated_{st.session_state.question_idx}"] = True
        if set(selected_keys) == set(correct_answers):
            st.session_state[f"score_{st.session_state.question_idx}"] = True
            st.rerun()
        else:
            st.session_state[f"score_{st.session_state.question_idx}"] = False
            st.rerun()
else:
    # Affiche la correction si déjà validé
    if st.session_state.get(f"score_{st.session_state.question_idx}", False):
        st.success("✅ Bonne réponse !")
    else:
        if len(correct_answers) == 1:
            bonne = correct_answers[0]
            st.markdown(
                f"<span style='color:#2563eb; font-weight:bold;'>❌ Mauvaise réponse. "
                f"La bonne réponse était : {bonne}. {options[bonne]}</span>",
                unsafe_allow_html=True
            )
        else:
            bonnes = ', '.join([f"{k}. {options[k]}" for k in correct_answers])
            st.markdown(
                f"<span style='color:#2563eb; font-weight:bold;'>❌ Mauvaise réponse. "
                f"Les bonnes réponses étaient : {bonnes}</span>",
                unsafe_allow_html=True
            )

score = sum(
    1 for i in range(num_questions)
    if st.session_state.get(f"score_{i}", False)
)
st.markdown("---")
st.subheader(f"Score : {score} / {num_questions}")
