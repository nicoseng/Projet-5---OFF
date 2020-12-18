# Projet 5 : Utilisez les données publiques de l'OpenFoodFacts(OFF)

Dépot Github : (mettre le lien ici)
Programme rédigé sous Python3. Projet sous Virtual Env et Git

# I°) Préparez l’environnement virtuel de développement

1.	Installez un environnement virtuel de développement depuis votre terminal. (python3 –m venv env) ;
2.	Activez l’environnement virtuel en tapant source env/bin/activate. Une mention (env) s’affiche à gauche de votre console.

# II°) Configurez son projet 

1.	 Dans le fichier intitulé config.py, remplissez les constantes suivantes avec vos propres identifiants (conservez les guillemets ""):
	 - DB_HOST = "Nom de votre serveur abritant votre base de données" ;
	 - DB_USER = "Nom d'utilisateur" ;
	 - DB_PASSWORD = "Mot de passe d'accès à la base de données" ;
	 - DB_NAME = "Nom de la base de données".
2. 	 Dans une autre fenêtre de votre terminal, tapez mysql -u suivi de votre nom d'utilisateur(DB_USER) et de -p ;
3.	 Connectez-vous à votre base de données à l'aide de votre mot de passe d'accès choisi dans DB_PASSWORD.

# III°) Démarrez l'application Pur Beurre

1.	 Dans le terminal, entrez python3 pur_beurre_app.py. Ce dernier correspond au fichier principal de l'application ; 
2.	 Entrez votre nom.

# IV°) Utilisez l'application

L'application permet de proposer à l'utilisateur un aliment de substitut de meilleure qualité nutritionnelle que celui qu'il a choisi au départ. L'utilisateur se retrouve devant le terminal. Le programme lui affiche les choix suivants : 
 1. Quel aliment souhaitez-vous remplacer ? 
 2. Retrouver les aliments en question substitués.
L'utilisateur sélectionne le choix 1. Le programme pose alors les questions suivantes à l'utilisateur : 
- Sélectionnez une catégorie d'aliment (ex: desserts, sauces, conserves, etc.). Chaque catégorie est associée à un chiffre. L'utilisateur choisit alors un chiffre et appuie sur la touche entrée. 
- Sélectionnez l'aliment en question. Chaque aliment est associé à un chiffre. L'utilisateur choisit alors un chiffre et appuie sur la touche entrée.
- Le programme propose un substitut plus sain à l'aliment sélectionné et donne sa description, un magasin où l'acheter et un lien URL vers la page OFF concernant ce substitut.
- L'utilisateur a alors la possibilité d'enregistrer ou non le résultat dans la base de données.
-  Pour vérifier les substituts enregistrés, tapez 2 dans le menu principal.

## Fonctionnalités 
- Recherche d'aliments dans la base OFF;
- L'utilisateur interagit avec le programme soit via le terminal soit via une interface graphique (facultatif);
- Si l'utilisateur rentre par erreur ou s'amuse à rentrer un caractère qui n'est pas un nombre, le programme doit être capable de lui répéter la question; 
- La recherche doit s'effectuer sur une base MySQL.
