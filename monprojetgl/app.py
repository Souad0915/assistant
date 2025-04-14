import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Analyse des Notes des Étudiants")

# Bouton pour importer un fichier CSV
uploaded_file = st.file_uploader("Importer un fichier CSV contenant les notes", type=["csv"])

if uploaded_file is not None:
    # Lecture du fichier CSV
    df = pd.read_csv(uploaded_file)
    
    # Nettoyer la colonne 'Numero' si nécessaire (supprimer les virgules)
    df["Numero"] = df["Numero"].astype(str).str.replace(',', '', regex=False)
    
    # Vérification si la colonne 'Note' existe
    if "Note" in df.columns and "Nom" in df.columns and "Numero" in df.columns:
        # Comptage du nombre d'étudiants par note
        notes_distribution = df["Note"].value_counts().sort_index()

        # Calcul de la moyenne des notes des étudiants présents
        moyenne = df["Note"].mean()

        # Calcul de la meilleure note et de la note la plus basse
        meilleure_note = df["Note"].max()
        note_plus_basse = df["Note"].min()

        # Filtrer les étudiants ayant la meilleure note
        meilleurs_etudiants = df[df["Note"] == meilleure_note][["Numero", "Nom", "Note"]]

        # Filtrer les étudiants ayant la note la plus basse
        etudiants_basse_note = df[df["Note"] == note_plus_basse][["Numero", "Nom", "Note"]]

        # Affichage des données sous forme de tableau
        st.write("Nombre d'étudiants par note :", notes_distribution)

        # Affichage de la moyenne
        st.write(f"La moyenne des notes des étudiants présents est : {moyenne:.2f}")

        # Affichage de la meilleure note et des étudiants correspondants
        st.write(f"La meilleure note est : {meilleure_note}")
        if len(meilleurs_etudiants) == 1:
            st.write("L'étudiant ayant la meilleure note est :")
        else:
            st.write("Les étudiants ayant la meilleure note sont :")
        st.write(meilleurs_etudiants)

        # Affichage de la note la plus basse et des étudiants correspondants
        st.write(f"La note la plus basse est : {note_plus_basse}")
        if len(etudiants_basse_note) == 1:
            st.write("L'étudiant ayant la note la plus basse est :")
        else:
            st.write("Les étudiants ayant la note la plus basse sont :")
        st.write(etudiants_basse_note)

        # Création du graphique
        fig, ax = plt.subplots()
        ax.plot(notes_distribution.index, notes_distribution.values, marker="o", linestyle="-", color="b")
        ax.set_title("Évolution du Nombre d'Étudiants par Note")
        ax.set_xlabel("Note")
        ax.set_ylabel("Nombre d'Étudiants")
        ax.grid(True)

        # Affichage du graphique
        st.pyplot(fig)
    else:
        st.error("Le fichier CSV doit contenir les colonnes 'Numéro', 'Nom' et 'Note'.")
