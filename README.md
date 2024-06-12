# secured-chatroom
-- But
Développer une application de messagerie instantanée sécurisée utilisant une hiérarchie d’entités virtuelles de certification x509 avec OpenSSL et LDAP. L'objectif est de sécuriser les échanges électroniques entre entreprises, particuliers et administrations via une Infrastructure à Clef Publique (PKI).

-- Fonctionnalités
- Inscription et Connexion:
Enregistrement des utilisateurs avec des informations personnelles et des certificats numériques.
Authentification et vérification des utilisateurs via LDAP et PKI.
Gestion des utilisateurs actifs et non actifs.
- Messagerie Sécurisée:
Échange de messages chiffrés entre clients utilisant RSA.
Utilisation de hachage pour l'intégrité des messages.
Affichage de la date et de l'heure des messages.

-- Architecture
- Côté Client:
Inscription et saisie des informations d'identification.
Connexion avec authentification.
Affichage des utilisateurs actifs et sélection pour discussion.
Chiffrement/Déchiffrement des messages avec RSA.
Déconnexion et sortie de l'application.
- Côté Serveur:
Enregistrement des utilisateurs dans Active Directory via LDAP.
Création de PKI et certification x509.
Communication avec le serveur de messagerie RabbitMQ.
Vérification des informations d'identification et des certificats.

-- Outils Utilisés
RabbitMQ: Broker de messagerie basé sur le protocole AMQP.
pycryptodome: Bibliothèque Python pour le chiffrement/déchiffrement.
OpenSSL: Interface pour la génération de certificats X509.
Tkinter: Interface standard pour la création de GUI en Python.
cryptography: Bibliothèque pour les certificats X509.
OpenLDAP: Implémentation du protocole LDAP sous Ubuntu.
Pika: Client Python pour RabbitMQ.

-- Références
YouTube - Public Key Infrastructure (PKI): https://www.youtube.com/watch?v=x_OWvcC8YY0
PyOpenSSL Documentation : https://pyopenssl.org/en/stable/api.html
