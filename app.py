import streamlit as st
from itertools import combinations

st.title("Organisation des combats – Karaté (club)")

# ---------------------------
# 1. Saisie des participants
# ---------------------------

st.subheader("1. Participants")

noms_bruts = st.text_area(
    "Saisir les noms des enfants (un par ligne)",
    placeholder="Lucas\nAdam\nNoah\nLéo"
)

participants = [n.strip() for n in noms_bruts.splitlines() if n.strip()]

if len(participants) < 2:
    st.warning("Il faut au moins deux participants pour organiser des combats.")
    st.stop()

# ---------------------------
# 2. Initialisation des combats
# ---------------------------

if (
    "combats" not in st.session_state
    or st.session_state.get("participants") != participants
):
    st.session_state.participants = participants
    st.session_state.combats = [
        {
            "a": a,
            "b": b,
            "joue": False,
            "vainqueur": None
        }
        for a, b in combinations(participants, 2)
    ]

# ---------------------------
# 3. Affichage des combats
# ---------------------------

st.subheader("2. Liste des combats")

for i, c in enumerate(st.session_state.combats):
    if c["joue"]:
        st.write(
            f"{i} – {c['a']} vs {c['b']} → ✅ Gagnant : {c['vainqueur']}"
        )
    else:
        st.write(
            f"{i} – {c['a']} vs {c['b']} → ⏳ À JOUER"
        )

# ---------------------------
# 4. Saisie des résultats
# ---------------------------

st.subheader("3. Saisir un résultat")

combats_a_jouer = [
    i for i, c in enumerate(st.session_state.combats) if not c["joue"]
]

if combats_a_jouer:
    idx = st.selectbox(
        "Choisir un match non encore joué",
        combats_a_jouer
    )

    combat = st.session_state.combats[idx]

    gagnant = st.radio(
        "Vainqueur du match",
        [combat["a"], combat["b"]]
    )

    if st.button("Valider le résultat"):
        combat["vainqueur"] = gagnant
        combat["joue"] = True
        st.success("Résultat enregistré.")
else:
    st.success("Tous les combats ont été joués.")

# ---------------------------
# 5. Classement provisoire
# ---------------------------

st.subheader("4. Classement provisoire")

scores = {p: 0 for p in participants}
for c in st.session_state.combats:
    if c["joue"]:
        scores[c["vainqueur"]] += 1

classement = sorted(scores.items(), key=lambda x: x[1], reverse=True)

for nom, score in classement:
    st.write(f"{nom} : {score} victoire(s)")
