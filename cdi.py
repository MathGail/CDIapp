import json
import tkinter as tk
from tkinter import messagebox, simpledialog

#valeur session open ou close
opens = 0
admin = 0
Aroot = 0

pw_minidoc = "change_this_password"
pw_admin = "change_this_password"
pw_root = "change_this_password"

# Fonction pour enregistrer les données dans un fichier JSON
def save_data(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

# Fonction pour charger les données depuis un fichier JSON
def load_data(filename):
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        confirmation = messagebox.showinfo("Confirmation", "Fichier livre non trouvé. Contacter l'oppérateur. Un mot de passe sera demandé. Si pas opérateur, cliquer sur cancel")
        password = simpledialog.askstring("Vérification", "Entrez le mot de passe OP : ")
        if password == pw_root:
            return []
        elif password is None:
            exit()
        else:
            messagebox.showerror("Vérification", "Mot de passe incorrect.")
            exit()
    
#chargement des livres
def reload():
    global books_manual, books_text, books, opens
    #books_manual = load_data('livres_manuels.json')
    #books_text = load_data('livres.txt')
    books = load_data('livres.json')
    if opens == 1:
        messagebox.showinfo("Gestions des livres", "Reload complété")
    else:
        return

#fenetre d'acceuil
def authentication():
    global aut, opens, admin, Aroot
    opens = 0
    admin = 0
    Aroot = 0
    aut = tk.Tk()
    aut.title("Authentification")

    role_label = tk.Label(aut, text="Rôle:")
    role_label.grid(row=0, column=0, padx=10, pady=5)

    user_button = tk.Button(aut, text="Utilisateur", command=user_interface)
    user_button.grid(row=0, column=1, padx=10, pady=5)

    admin_button = tk.Button(aut, text="Administrateur", command=lambda: admin_interface(aut))
    admin_button.grid(row=0, column=3, padx=10, pady=5)
    
    admin_button = tk.Button(aut, text="Minidoc", command=lambda: minidoc_interface(aut))
    admin_button.grid(row=0, column=2, padx=10, pady=5)
    
    aut.mainloop()

#fenêtre de fermeture de session
def close():
    global root
    root.destroy()
    authentication()

#gestions du CDI
def fen_epr():
    global root
    root = tk.Tk()
    root.title("Gestionnaire de réservations")

    #role_label = tk.Label(root, text="Action:")
    #role_label.grid(row=0, column=0, padx=10, pady=5)

    emp = tk.Button(root, text="Emprunter", command=emprun)
    emp.grid(row=0, column=1, padx=10, pady=5)
    
    rd = tk.Button(root, text="Rendre", command=rendre)
    rd.grid(row=0, column=2, padx=10, pady=5)
    
    root.mainloop()

def fenetre_livres_gestion():
    global root, admin, book_number
    root = tk.Tk()
    root.title("Gestionnaire de livres")

    #role_label = tk.Label(root, text="Gestionnaire de livre")
    #role_label.grid(row=0, column=1, padx=10, pady=5)

    ajm = tk.Button(root, text="Ajouter un livre manuellement", command=add_book_manually)
    ajm.grid(row=1, column=1, padx=10, pady=5)

    spm = tk.Button(root, text="supression de livre", command=remove_book_from_json)
    spm.grid(row=2, column=1, padx=10, pady=5)
    
    if admin == 1:
        aja = tk.Button(root, text="Ajouter une liste de livre", command=add_books_from_file)
        aja.grid(row=3, column=1, padx=10, pady=5)
    if Aroot == 1:
        rml = tk.Button(root, text="Rénitialiser les listes", command=rm_data)
        rml.grid(row=4, column=1, padx=10, pady=5)
    
    root.mainloop()

def rm_data():
    confirmation = messagebox.askquestion("Confirmation", "Êtes-vous sûr de vouloir supprimer la liste de livre ?")
    if confirmation == 'yes':
        with open('livres.json', 'r') as f:
            data = json.load(f)
            return []
def emprun():
    global book_number
    global root
    root.destroy()
    student_name = simpledialog.askstring("Emprunter un livre", "Entrez votre nom : ")
    if student_name is None:
        root.destroy()
        return
    
    for book in books:
        if book['numero'] == book_number:
            if book.get('emprunteur') is None:
                book['emprunteur'] = student_name
                save_data('livres.json', books)
                messagebox.showinfo("Emprunt de livre", f"Le livre \"{book['titre']}\" a été emprunté avec succès par {student_name}.")
                reload()
                return
            else:
                messagebox.showwarning("Emprunt de livre", f"Le livre \"{book['titre']}\" est déjà emprunté.")
                return
            messagebox.showwarning("Retour de livre", "Le livre avec ce numéro n'a pas été trouvé.")
        

def rendre():
    global book_number, root
    root.destroy()
    for book in books:
        if book['numero'] == book_number:
            if book.get('emprunteur') is not None:
                book.pop('emprunteur')
                save_data('livres.json', books)
                messagebox.showinfo("Retour de livre", f"Le livre \"{book['titre']}\" a été retourné avec succès.")
                return
            else:
                messagebox.showwarning("Retour de livre", f"Le livre \"{book['titre']}\" n'est pas emprunté.")
                return
    messagebox.showwarning("Retour de livre", "Le livre avec ce numéro n'a pas été trouvé.")
    
def borrow_or_return_book():
    global book_number
    book_number = simpledialog.askstring("Emprunter/Retourner un livre", "Entrez le numéro du livre : ")

    if book_number is None:
        return
    fen_epr()

def show_book_info():
    book_number = simpledialog.askstring("Voir les informations d'un livre", "Entrez le numéro du livre : ")

    for book in books:
        if book_number is None:
            return
        if book['numero'] == book_number:
            messagebox.showinfo("Informations du livre", f"Auteur: {book['auteur']}\nTitre: {book['titre']}\nNuméro: {book['numero']}\nEmprunteur: {book.get('emprunteur', 'Aucun')}")
            return
        
    messagebox.showwarning("Informations du livre", "Le livre avec ce numéro n'a pas été trouvé.")

def add_book_manually():
    global root
    author = simpledialog.askstring("Ajouter un livre", "Entrez l'auteur du livre : ")
    if author is None:
        root.destroy()
        return

    title = simpledialog.askstring("Ajouter un livre", "Entrez le titre du livre : ")
    if title is None:
        root.destroy()
        return

    number = simpledialog.askstring("Ajouter un livre", "Entrez le numéro du livre : ")
    if number is None:
        root.destroy()
        return
    
    books.append({"auteur": author, "titre": title, "numero": number})
    save_data('livres.json', books)
    
    root.destroy()
    messagebox.showinfo("Gestions des livres", "Ajout avec succes")

def add_books_from_file():
    file_path = simpledialog.askstring("Ajouter des livres", "Entrez le chemin du fichier texte contenant les livres : ")
    root.destroy()
    
    with open(file_path, 'r') as f:
        for line in f:
            author, title, number = line.strip().split(',')
            books.append({"auteur": author, "titre": title, "numero": number})

    save_data('livres.json', books)
    messagebox.showinfo("Gestions des livres", "Ajouts fini : penser a reload")
    
def remove_book_from_json():
    global books, book_number
    book_number = simpledialog.askstring("Gestionnaire de livre", "Entrez le numéro du livre : ")
    for book in books:
        if book['numero'] == book_number:
            if 'emprunteur' in book:
                messagebox.showwarning("Livre emprunté", "Ce livre est actuellement emprunté. Vous ne pouvez pas le supprimer.")
                root.destroy()
                return False

            confirmation = messagebox.askquestion("Confirmation", f"Êtes-vous sûr de vouloir supprimer le livre \"{book['titre']}\" ?")
            if confirmation == 'yes':
                books.remove(book)  
                save_data('livres.json', books) 
                messagebox.showinfo("Suppression de livre", f"Le livre \"{book['titre']}\" a été supprimé avec succès.")
                root.destroy()
                return True
            else:
                root.destroy()
                return False
            break

    messagebox.showwarning("Livre non trouvé", "Le livre avec ce numéro n'a pas été trouvé dans la liste.")
    return False

def delete_reservation():
    global root
    book_number = simpledialog.askstring("Supprimer la réservation", "Entrez le numéro du livre : ")
    if book_number is None:
        return
    for book in books:
        if book['numero'] == book_number:
            if book.get('emprunteur') is not None:
                book.pop('emprunteur')
                save_data('livres.json', books)
                messagebox.showinfo("Suppression de réservation", f"La réservation du livre \"{book['titre']}\" a été supprimée avec succès.")
                root.destroy()
            else:
                messagebox.showwarning("Suppression de réservation", f"Le livre \"{book['titre']}\" n'est pas réservé.")
            root.destroy()
            return
    messagebox.showwarning("Suppression de réservation", "Le livre avec ce numéro n'a pas été trouvé.")
    root.destroy()

def show_reservations():
    reservations = [f"Livre: {book['titre']}, Numéro: {book['numero']}, Emprunteur: {book.get('emprunteur', 'Aucun')}" for book in books]
    messagebox.showinfo("Réservations", "\n".join(reservations))

#fonctions des sessions
def admin_interface(aut):
    global Aroot
    password = simpledialog.askstring("Authentification", "Entrez le mot de passe : ")
    if password == pw_admin:
        Aroot = 0
        aut.destroy()
        admin_ui()
    elif password == pw_root:
        aut.destroy()
        Aroot = 1
        admin_ui()
    elif password is None:
        Aroot = 0
        return
    else:
        Aroot = 0
        messagebox.showerror("Authentification", "Mot de passe incorrect.")
        
def minidoc_interface(aut):
    global Aroot
    password = simpledialog.askstring("Authentification", "Entrez le mot de passe : ")
    if password == pw_minidoc:
        Aroot = 0
        aut.destroy()
        Minidoc_ui()
    elif password is None:
        return
    else:
        messagebox.showerror("Authentification", "Mot de passe incorrect.")

#interfaces
def admin_ui():
    global root, opens, admin
    admin = 1
    opens = 1
    root = tk.Tk()
    root.title("Interface Administrateur")

    borrow_button = tk.Button(root, text="Gestionnaire de réservations", command=borrow_or_return_book)
    borrow_button.pack(pady=10)

    add_manual_button = tk.Button(root, text="Gestionnaire de livre", command=fenetre_livres_gestion)
    add_manual_button.pack(pady=10)

    show_info_button = tk.Button(root, text="Voir les informations d'un livre", command=show_book_info)
    show_info_button.pack(pady=10)
    
    show_reservations_button = tk.Button(root, text="Afficher les réservations", command=show_reservations)
    show_reservations_button.pack(pady=10)
    
    reload_button = tk.Button(root, text="Reload les listes", command=reload)
    reload_button.pack(pady=10)
    
    deco_button = tk.Button(root, text="lock", command=close)
    deco_button.pack(pady=10)

    root.mainloop()
    
def Minidoc_ui():
    # Création de l'interface administrateur
    global root, opens, Aroot
    opens = 1
    admin = 0
    Aroot = 0
    root = tk.Tk()
    root.title("Interface Minidoc")

    borrow_button = tk.Button(root, text="Gestionnaire de réservations", command=borrow_or_return_book)
    borrow_button.pack(pady=10)

    add_manual_button = tk.Button(root, text="Gestionnaire de livre", command=fenetre_livres_gestion)
    add_manual_button.pack(pady=10)

    show_reservations_button = tk.Button(root, text="Afficher les réservations", command=show_reservations)
    show_reservations_button.pack(pady=10)
    
    show_info_button = tk.Button(root, text="Voir les informations d'un livre", command=show_book_info)
    show_info_button.pack(pady=10)
    
    reload_button = tk.Button(root, text="Reload les listes", command=reload)
    reload_button.pack(pady=10)
    
    deco_button = tk.Button(root, text="lock", command=close)
    deco_button.pack(pady=10)

    root.mainloop()

def user_interface():
    # Création de l'interface utilisateur
    global aut, root
    aut.destroy()
    root = tk.Tk()
    root.title("Interface Utilisateur")

    borrow_button = tk.Button(root, text="Emprunter/Retourner un livre", command=borrow_or_return_book)
    borrow_button.pack(pady=10)

    show_info_button = tk.Button(root, text="Voir les informations d'un livre", command=show_book_info)
    show_info_button.pack(pady=10)

    deco_button = tk.Button(root, text="lock", command=close)
    deco_button.pack(pady=10)
    
    root.mainloop()

reload()
authentication()
