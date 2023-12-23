def diviseurs(pol1, pol2) :
    if pol2 == 0 :
        raise ValueError("")
    
    deg_pol1 = len(pol1) - 1
    deg_pol2 = len(pol2) - 1
    
    if deg_pol2 > deg_pol1 :
        return False
    
    if pol1[0] % pol2[0] != 0 :
        return False
    

    for i in range(1, deg_pol2 + 1) :
        coef = pol1[i - 1] / pol2[i - 1]
        


print("Ils sont diviseurs" if diviseurs([1, 4, 6, 4, 1], [1, 7]) else 'Ils ne le sont pas')