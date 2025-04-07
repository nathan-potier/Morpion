import random

def print_plateau(plateau):
    t_pos = ["A", "B", "C"]
    print(" 0 1 2 ")
    for i in range(3):
        ligne =  ""
        ligne += t_pos[i]
        for j in range(3):
            ligne += plateau[i][j]
            if j < 2:
                ligne += "|"
        print(ligne)
        if i < 2:
            print(" -----")
        
def init_plateau():
    tableau = [[" "for _ in range(3)]for _ in range(3)]
    return tableau

def case_valide(x, y, plateau) -> bool:
    if plateau[y][x] == " ":
        return True
    else:
        return False

def demander_position():
    try:
        choix = input("choisir une position (ex : A2)")
        col = convert(choix[0])
        ligne = int(choix[1])
        return (col, ligne)
    except:
        print("forrmat invalide")
        return demander_position()
    
def placer_symbole(x, y, symbole, plateau):
    if case_valide(x,y,plateau) == True:
        plateau[y][x] = symbole
        return True, plateau
    else:
        return False, plateau

def gagner(plateau: list) -> bool:
    for i in range(3):
        if plateau[i][0] == plateau[i][1] == plateau[i][2] and plateau[i][0] != " ":
            return True 
        if plateau[0][i] == plateau[1][i] == plateau[2][i] and plateau[0][i] != " ":
            return True
    if plateau[0][0] == plateau[1][1] == plateau[2][2] and plateau[2][2] != " ":
        return True
    if plateau[0][2] == plateau[1][1] == plateau[2][0] and plateau[1][1] != " ":
        return True
    return False

def match_nul(plateau):
    if gagner(plateau) == True:
        return False
    for y in range(3):
        for x in range(3):
            if case_valide(x, y, plateau) == True:
                return False
    return True

def convert(e : str) -> int: 
    t = ["A", "B", "C"]

    for i in range(len(t)):
        if t[i] == e:
            return i
    raise ValueError

def verif_victoir_potentiel(j, plateau):
    for y in range(3):
        for x in range(3):
            if case_valide(x,y, plateau) :
                p_cpy = [ligne[:] for ligne in plateau]
                placer_symbole(x, y, j, p_cpy)
                if gagner(p_cpy):
                    return (y, x)
    
def best_coup_bot(plateau:list)  ->tuple:
    
    #vérifie si le bot peut gagner actuellement
    res = verif_victoir_potentiel("O", plateau)
    if res != None:
        return res
    
    # Vérifie si le joueur adverse peut gagner
    res = verif_victoir_potentiel("X", plateau)
    if res != None:
        return res

    #4. Jouer mid
    if case_valide(1, 1, plateau):
        return (1, 1)
    
    
    #5. Jouer coins
    coins = [(0,0), (0,2), (2,0), (2,2)]
    for x , y in coins :
        if case_valide(x, y, plateau):
            return (y, x)  
        
    #6. Jouer cotes 
    cotes = [(0,1), (1,0), (1,2), (2,1)]
    for x , y in cotes :
        if case_valide(x, y, plateau):
            return (y, x)  
        
    
    return None

def best_coup_bot_ai(plateau):
    best_score = -float('inf')
    coup = None
    
    for y in range(3):
        for x in range(3):
            if case_valide(x, y, plateau):
                plateau[y][x] = "O"
                score = minimax(plateau, 0, False)
                plateau[y][x] = " "
                if score > best_score :
                    best_score = score
                    coup = (y, x)
    return coup
    
# Fonction minimax : permet à l'IA de choisir le meilleur coup possible
# plateau : le tableau de jeu actuel
# profondeur : la profondeur dans l'arbre de décision (on peut l'utiliser pour améliorer plus tard)
# is_bot_playing : True si c’est au tour du bot (IA), False si c’est au tour du joueur

def minimax(plateau, profondeur, is_bot_playing):
    # Vérifie si quelqu'un a gagné
    if gagner(plateau):
        if is_bot_playing == True:
            # Si c’est le tour du bot, mais le plateau indique une victoire => le joueur a gagné
            return -1  # Mauvais score pour le bot
        else:
            # Si c’est le tour du joueur, mais le plateau indique une victoire => le bot a gagné
            return 1   # Bon score pour le bot
    
    # Si personne n’a gagné et le plateau est plein => match nul
    if match_nul(plateau):
        return 0  # Égalité, score neutre

    # Tour de l'IA : elle veut maximiser le score
    if is_bot_playing == True:
        best_score = -float('inf')  # On part d'un score très bas

        # Parcours de toutes les cases du plateau
        for y in range(3):
            for x in range(3):
                if case_valide(x, y, plateau):  # Si la case est vide
                    plateau[y][x] = "O"  # L'IA joue son coup (temporairement)

                    # Appel récursif : maintenant c’est au tour du joueur
                    score = minimax(plateau, profondeur + 1, False)

                    # Annule le coup (backtracking)
                    plateau[y][x] = " "

                    # On garde le score le plus élevé (car l'IA veut maximiser ses chances)
                    best_score = max(score, best_score)

        return best_score  # On retourne le meilleur score trouvé à ce niveau

    # Tour du joueur : il veut minimiser le score de l'IA
    else:
        best_score = float('inf')  # On part d’un score très haut

        for y in range(3):
            for x in range(3):
                if case_valide(x, y, plateau):  # Si la case est vide
                    plateau[y][x] = "X"  # Le joueur joue son coup (temporairement)

                    # Appel récursif : maintenant c’est au tour de l'IA
                    score = minimax(plateau, profondeur + 1, True)

                    # Annule le coup (backtracking)
                    plateau[y][x] = " "

                    # On garde le score le plus bas (car le joueur veut que l'IA perde)
                    best_score = min(score, best_score)

        return best_score  # On retourne le pire score du point de vue de l'IA
               
    
    
    
def jouer():
    t = init_plateau()
    print_plateau(t)
    j_actu = "X"
    while True:
        print(j_actu)
        
        
        if j_actu == "X":
            y, x =  demander_position()
        else:
            y, x = best_coup_bot_ai(t)
        
        empiler = placer_symbole(x, y, j_actu, t)
        if empiler[0] == False:
            continue
        print_plateau(t)
        if gagner(t):
            print("Bravo", j_actu, "a gagné !")
            break
        if j_actu == "X":
            j_actu = "O"
        else:
            j_actu = "X"
            
        if match_nul(t):
            print("match nul !")
            break


jouer()