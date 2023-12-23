import random, string
import database

list_nom = [f'personne_{i}' for i in range(800)]
list_mail = [f'personne_{i}@gmail.com' for i in range(800)]
list_password = ["".join([random.choice(string.ascii_lowercase)+random.choice(string.punctuation) for _ in range(4)]) for _ in range(800)]
personnes = [
    {
        "name" : name,
        "mail" : mail,
        "password" : password,
        "age" : random.randint(10, 40)      
    }  for (name,password, mail) in zip(list_nom, list_password, list_mail)
]         
"""for pers in personnes :
    database.User.addUser(**pers)   """