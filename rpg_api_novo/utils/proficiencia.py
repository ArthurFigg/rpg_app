def calcular_bonus_proficiencia(nivel):
  
    if 1 <= nivel <= 4:
        return 2
    elif 5 <= nivel <= 8:
        return 3
    elif 9 <= nivel <= 13:
        return 4
    elif 14 <= nivel <= 16:
        return 5
    elif nivel >= 17:
        return 6
    return 2  
