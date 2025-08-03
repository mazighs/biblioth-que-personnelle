
# Auteur : barache mazigh
# Projet : Bibliothèque CLI – Collège Boréal Été 2025

import json


def charger_donnees(fichier):
    try:
        with open(fichier, "r", encoding="utf-8") as f:
            bibliotheque = json.load(f)
            return bibliotheque if isinstance(bibliotheque, list) else []
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def sauvegarder_donnees(bibliotheque, fichier):
    try:
        with open(fichier, "w", encoding="utf-8") as f:
            json.dump(bibliotheque, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Erreur lors de la sauvegarde des données : {e}")


def generer_id(bibliotheque):
    return max((livre["ID"] for livre in bibliotheque), default=0) + 1


def afficher_tous_les_livres(bibliotheque):
    if not bibliotheque:
        print("Aucun livre dans la bibliothèque.")
        return
    print("\nListe complète des livres :")
    for livre in bibliotheque:
        ligne = f'ID {livre["ID"]} : "{livre["Titre"]}" par {livre["Auteur"]} ({livre["Annee"]}) - Lu : {"Oui" if livre["Lu"] else "Non"}'
        if livre["Lu"] and livre["Note"] is not None:
            ligne += f", Note : {livre['Note']}/10"
        print(ligne)
        if livre["Lu"] and livre.get("Commentaire"):
            print(f"    Commentaire : {livre['Commentaire']}")
    print()


def ajouter_livre(bibliotheque):
    print("\n*** Ajouter un nouveau livre ***")
    titre = input("Titre du livre : ").strip()
    if not titre:
        print("Le titre ne peut pas être vide. Ajout annulé.")
        return
    auteur = input("Auteur du livre : ").strip()
    if not auteur:
        print("L'auteur ne peut pas être vide. Ajout annulé.")
        return
    while True:
        annee_str = input("Année de publication : ").strip()
        try:
            annee = int(annee_str)
            break
        except ValueError:
            print("Année invalide. Réessayez.")
    nouveau_livre = {
        "ID": generer_id(bibliotheque),
        "Titre": titre,
        "Auteur": auteur,
        "Année": annee,
        "Lu": False,
        "Note": None,
        "Commentaire": None
    }
    bibliotheque.append(nouveau_livre)
    print(f"Livre ajouté avec succès (ID {nouveau_livre['ID']}).")


def supprimer_livre(bibliotheque):
    print("\n*** Supprimer un livre ***")
    while True:
        id_str = input("Entrez l'ID du livre à supprimer : ").strip()
        try:
            id_livre = int(id_str)
            break
        except ValueError:
            print("ID invalide. Réessayez.")
    livre = next((liv for liv in bibliotheque if liv["ID"] == id_livre), None)
    if livre:
        confirmation = input(
            f"Supprimer \"{livre['Titre']}\" ? (O/N) : ").lower()
        if confirmation == 'o':
            bibliotheque.remove(livre)
            print("Livre supprimé.")
        else:
            print("Suppression annulée.")
    else:
        print("Aucun livre trouvé avec cet ID.")


def rechercher_livre(bibliotheque):
    print("\n*** Rechercher un livre ***")
    mot_cle = input("Mot-clé : ").strip().lower()
    if not mot_cle:
        print("Recherche annulée.")
        return
    resultats = [
        liv for liv in bibliotheque
        if mot_cle in liv["Titre"].lower() or mot_cle in liv["Auteur"].lower()]
    if not resultats:
        print("Aucun résultat.")
        return
    for livre in resultats:
        ligne = f'ID {livre["ID"]} : "{livre["Titre"]}" par {livre["Auteur"]} ({livre["Annee"]}) - Lu : {"Oui" if livre["Lu"] else "Non"}'
        if livre["Lu"] and livre["Note"] is not None:
            ligne += f", Note : {livre['Note']}/10"
        print(ligne)
        if livre["Lu"] and livre.get("Commentaire"):
            print(f"    Commentaire : {livre['Commentaire']}")


def marquer_comme_lu(bibliotheque):
    print("\n*** Marquer un livre comme lu ***")
    while True:
        id_str = input("ID du livre : ").strip()
        try:
            id_livre = int(id_str)
            break
        except ValueError:
            print("ID invalide. Réessayez.")
    livre = next((liv for liv in bibliotheque if liv["ID"] == id_livre), None)
    if not livre:
        print("Livre introuvable.")
        return
    if livre["Lu"]:
        if input("Déjà lu. Modifier la note/commentaire ? (O/N) : "
                 ).lower() != 'o':
            print("Opération annulée.")
            return
    livre["Lu"] = True
    while True:
        note_str = input(
                         "note sur 10 (optionnel, taper Entrée pour ignorer) :"
                         ).strip()
        if not note_str:
            livre["Note"] = None
            break
        try:
            note = int(note_str)
            if 0 <= note <= 10:
                livre["Note"] = note
                break
            else:
                print("La note doit être entre 0 et 10.")
        except ValueError:
            print("Note invalide. Réessayez.")
    commentaire = input("Commentaire (optionnel) : ").strip()
    livre["Commentaire"] = commentaire if commentaire else None
    print(f"Livre \"{livre['Titre']}\" mis à jour.")


def afficher_par_statut(bibliotheque):
    print("\n*** Affichage par statut ***")
    choix = input("1. Livres lus\n2. Livres non lus\nVotre choix : ").strip()
    if choix == '1':
        livres = [liv for liv in bibliotheque if liv["Lu"]]
        titre = "Livres lus"
    elif choix == '2':
        livres = [liv for liv in bibliotheque if not liv["Lu"]]
        titre = "Livres non lus"
    else:
        print("Choix invalide.")
        return
    print(f"\n{titre} :")
    if not livres:
        print("Aucun livre correspondant.")
        return
    for liv in livres:
        ligne = f'ID {liv["ID"]} : "{liv["Titre"]}" par {liv["Auteur"]} ({liv["Annee"]}) - Lu : {"Oui" if liv["Lu"] else "Non"}'
        if liv["Lu"] and liv["Note"] is not None:
            ligne += f", Note : {liv['Note']}/10" 
        print(ligne)
        if liv["Lu"] and liv.get("Commentaire"):
            print(f"    Commentaire : {liv['Commentaire']}")


def trier_livres(bibliotheque):
    print("\n*** Trier les livres ***")
    print("1. Par année (croissant)")
    print("2. Par auteur (A-Z)")
    print("3. Par note (décroissant)")
    choix = input("Choix : ").strip()
    if choix == '1':
        livres_tries = sorted(bibliotheque, key=lambda liv: liv["Année"])
    elif choix == '2':
        livres_tries = sorted(bibliotheque,
                              key=lambda liv: liv["Auteur"].lower())
    elif choix == '3':
        livres_tries = sorted(
         bibliotheque, key=lambda liv: -1 if liv["Note"] is None else liv["Note"], reverse=True)
    else:
        print("Choix invalide.")
        return
    for liv in livres_tries:
        ligne = f'ID {liv["ID"]} : "{liv["Titre"]}" par {liv["Auteur"]} ({liv["Annee"]}) - Lu : {"Oui" if liv["Lu"] else "Non"}'
        if liv["Lu"] and liv["Note"] is not None:
            ligne += f", Note : {liv['Note']}/10"
        print(ligne)
        if liv["Lu"] and liv.get("Commentaire"):
            print(f"    Commentaire : {liv['Commentaire']}")


def main():
    bibliotheque = charger_donnees("bibliotheque.json")
    print("=== Application Bibliothèque Personnelle ===")
    while True:
        print("\nMenu :")
        print("1. Afficher tous les livres")
        print("2. Ajouter un livre")
        print("3. Supprimer un livre")
        print("4. Rechercher un livre")
        print("5. Marquer un livre comme lu")
        print("6. Afficher les livres lus/non lus")
        print("7. Trier les livres")
        print("8. Quitter")
        choix = input("Votre choix : ").strip()
        if choix == '1':
            afficher_tous_les_livres(bibliotheque)
        elif choix == '2':
            ajouter_livre(bibliotheque)
        elif choix == '3':
            supprimer_livre(bibliotheque)
        elif choix == '4':
            rechercher_livre(bibliotheque)
        elif choix == '5':
            marquer_comme_lu(bibliotheque)
        elif choix == '6':
            afficher_par_statut(bibliotheque)
        elif choix == '7':
            trier_livres(bibliotheque)
        elif choix == '8':
            sauvegarder_donnees(bibliotheque, "bibliotheque.json")
            print("Données sauvegardées. Au revoir !")
            break
        else:
            print("Choix invalide. Réessayez.")


if __name__ == "__main__":
    main()
    
