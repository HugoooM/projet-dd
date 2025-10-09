-- Créer l'utilisateur
CREATE USER blog_user WITH PASSWORD 'postgresql';

-- Créer la base de données
CREATE DATABASE blog_db;

-- Se connecter à la base de données
\c blog_db

-- Donner tous les droits sur toutes les tables à blog_user
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO blog_user;

-- Donner les droits pour créer de nouvelles tables (optionnel)
GRANT ALL PRIVILEGES ON SCHEMA public TO blog_user;

-- Donner les droits pour les futures tables
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL PRIVILEGES ON TABLES TO blog_user;

-- Création de la table Utilisateur
CREATE TABLE Utilisateur
(
    id_utilisateur   SERIAL PRIMARY KEY,
    nom              VARCHAR(255) NOT NULL,
    email            VARCHAR(255) NOT NULL UNIQUE,
    date_inscription DATE         NOT NULL,
    bio              TEXT,
    role             VARCHAR(50)  NOT NULL
);

-- Création de la table Article
CREATE TABLE Article
(
    id_article       SERIAL PRIMARY KEY,
    titre            VARCHAR(255) NOT NULL,
    contenu          TEXT         NOT NULL,
    date_publication TIMESTAMP    NOT NULL,
    vue              INT DEFAULT 0,
    id_utilisateur   INT          NOT NULL,
    FOREIGN KEY (id_utilisateur) REFERENCES Utilisateur (id_utilisateur) ON DELETE CASCADE
);

-- Création de la table Tag
CREATE TABLE Tag
(
    id_tag  SERIAL PRIMARY KEY,
    libelle VARCHAR(255) NOT NULL UNIQUE
);

-- Création de la table Article_Tag (relation N:M)
CREATE TABLE Article_Tag
(
    id_article INT NOT NULL,
    id_tag     INT NOT NULL,
    PRIMARY KEY (id_article, id_tag),
    FOREIGN KEY (id_article) REFERENCES Article (id_article) ON DELETE CASCADE,
    FOREIGN KEY (id_tag) REFERENCES Tag (id_tag) ON DELETE CASCADE
);

-- Création de la table Commentaire
CREATE TABLE Commentaire
(
    id_commentaire VARCHAR(50) PRIMARY KEY,
    contenu        TEXT      NOT NULL,
    date           TIMESTAMP NOT NULL,
    id_article     INT       NOT NULL,
    id_utilisateur INT       NOT NULL,
    id_parent      VARCHAR(50),
    FOREIGN KEY (id_article) REFERENCES Article (id_article) ON DELETE CASCADE,
    FOREIGN KEY (id_utilisateur) REFERENCES Utilisateur (id_utilisateur) ON DELETE CASCADE,
    FOREIGN KEY (id_parent) REFERENCES Commentaire (id_commentaire) ON DELETE CASCADE
);

-- Insertion des données dans la table Utilisateur
INSERT INTO Utilisateur (nom, email, date_inscription, bio, role)
VALUES ('Hugo', 'hugo@example.com', '2023-10-01', 'Passionné de bases de données', 'auteur'),
       ('Evan', 'evan@example.com', '2024-05-15', 'Passionné de Mariette', 'auteur'),
       ('Elisia', 'elisia@example.com', '2025-10-08', 'Git breaker', 'auteur'),
       ('Mathis', 'mathis@example.com', '2022-04-10', 'Mathis aka le tigre fou', 'auteur'),
       ('Alice', 'alice@example.com', '2022-04-10', NULL, 'lecteur'),
       ('Bob', 'bob@example.com', '2022-04-10', NULL, 'lecteur');

-- Insertion des données dans la table Tag
INSERT INTO Tag (libelle)
VALUES ('mongodb'),
       ('nosql'),
       ('blog'),
       ('bases de données'),
       ('nourriture'),
       ('mariette'),
       ('culture'),
       ('2025'),
       ('git'),
       ('développement'),
       ('outils'),
       ('bonnes pratiques'),
       ('agile'),
       ('méthodologie'),
       ('humour');

-- Insertion des données dans la table Article
INSERT INTO Article (titre, contenu, date_publication, vue, id_utilisateur)
VALUES ('Pourquoi MongoDB est idéal pour les blogs modernes',
        'Dans cet article, nous explorons les avantages de MongoDB pour gérer le contenu d''un blog. Sa flexibilité permet de stocker des articles, des commentaires et des métadonnées de manière efficace, sans avoir à définir un schéma rigide à l''avance. Nous verrons aussi comment optimiser les requêtes pour une expérience utilisateur fluide.',
        '2025-10-01 10:00:00',
        250,
        (SELECT id_utilisateur FROM Utilisateur WHERE email = 'hugo@example.com')),
       ('Mariette : une révolution culinaire ?',
        'Mariette a marqué l''année 2025 avec son dernier tacos. Dans cet article, nous analysons son impact sur la scène universitaire française et pourquoi ses sandwichs résonnent autant avec le public. Une plongée dans l''univers d''une artiste qui ne laisse personne indifférent.',
        '2025-09-28 09:15:00',
        420,
        (SELECT id_utilisateur FROM Utilisateur WHERE email = 'evan@example.com')),
       ('Git : les commandes qui sauvent la mise',
        'Git est un outil puissant, mais il peut parfois sembler complexe. Dans cet article, je partage les commandes Git qui m''ont sauvé la mise à plusieurs reprises, que ce soit pour annuler des changements, retrouver un commit perdu ou résoudre des conflits. Parce que même les meilleurs développeurs font des erreurs !',
        '2025-10-05 16:00:00',
        310,
        (SELECT id_utilisateur FROM Utilisateur WHERE email = 'elisia@example.com')),
       ('Le tigre fou : une métaphore du développement agile ?',
        'Dans cet article un peu décalé, je compare la méthodologie agile à un tigre fou : rapide, imprévisible, mais incroyablement efficace quand on sait l''apprivoiser. Je partage mes expériences en tant que développeur et comment j''ai appris à dompter cette bête pour livrer des projets dans les temps.',
        '2025-09-25 08:30:00',
        180,
        (SELECT id_utilisateur FROM Utilisateur WHERE email = 'mathis@example.com'));

-- Insertion des données dans la table Article_Tag
-- MongoDB article
INSERT INTO Article_Tag (id_article, id_tag)
VALUES ((SELECT id_article FROM Article WHERE titre = 'Pourquoi MongoDB est idéal pour les blogs modernes'),
        (SELECT id_tag FROM Tag WHERE libelle = 'mongodb')),
       ((SELECT id_article FROM Article WHERE titre = 'Pourquoi MongoDB est idéal pour les blogs modernes'),
        (SELECT id_tag FROM Tag WHERE libelle = 'nosql')),
       ((SELECT id_article FROM Article WHERE titre = 'Pourquoi MongoDB est idéal pour les blogs modernes'),
        (SELECT id_tag FROM Tag WHERE libelle = 'blog')),
       ((SELECT id_article FROM Article WHERE titre = 'Pourquoi MongoDB est idéal pour les blogs modernes'),
        (SELECT id_tag FROM Tag WHERE libelle = 'bases de données'));

-- Mariette article
INSERT INTO Article_Tag (id_article, id_tag)
VALUES ((SELECT id_article FROM Article WHERE titre = 'Mariette : une révolution culinaire ?'),
        (SELECT id_tag FROM Tag WHERE libelle = 'nourriture')),
       ((SELECT id_article FROM Article WHERE titre = 'Mariette : une révolution culinaire ?'),
        (SELECT id_tag FROM Tag WHERE libelle = 'mariette')),
       ((SELECT id_article FROM Article WHERE titre = 'Mariette : une révolution culinaire ?'),
        (SELECT id_tag FROM Tag WHERE libelle = 'culture')),
       ((SELECT id_article FROM Article WHERE titre = 'Mariette : une révolution culinaire ?'),
        (SELECT id_tag FROM Tag WHERE libelle = '2025'));

-- Git article
INSERT INTO Article_Tag (id_article, id_tag)
VALUES ((SELECT id_article FROM Article WHERE titre = 'Git : les commandes qui sauvent la mise'),
        (SELECT id_tag FROM Tag WHERE libelle = 'git')),
       ((SELECT id_article FROM Article WHERE titre = 'Git : les commandes qui sauvent la mise'),
        (SELECT id_tag FROM Tag WHERE libelle = 'développement')),
       ((SELECT id_article FROM Article WHERE titre = 'Git : les commandes qui sauvent la mise'),
        (SELECT id_tag FROM Tag WHERE libelle = 'outils')),
       ((SELECT id_article FROM Article WHERE titre = 'Git : les commandes qui sauvent la mise'),
        (SELECT id_tag FROM Tag WHERE libelle = 'bonnes pratiques'));

-- Agile article
INSERT INTO Article_Tag (id_article, id_tag)
VALUES ((SELECT id_article FROM Article WHERE titre = 'Le tigre fou : une métaphore du développement agile ?'),
        (SELECT id_tag FROM Tag WHERE libelle = 'agile')),
       ((SELECT id_article FROM Article WHERE titre = 'Le tigre fou : une métaphore du développement agile ?'),
        (SELECT id_tag FROM Tag WHERE libelle = 'développement')),
       ((SELECT id_article FROM Article WHERE titre = 'Le tigre fou : une métaphore du développement agile ?'),
        (SELECT id_tag FROM Tag WHERE libelle = 'méthodologie')),
       ((SELECT id_article FROM Article WHERE titre = 'Le tigre fou : une métaphore du développement agile ?'),
        (SELECT id_tag FROM Tag WHERE libelle = 'humour'));

-- Insertion des données dans la table Commentaire
-- MongoDB article comments
INSERT INTO Commentaire (id_commentaire, contenu, date, id_article, id_utilisateur, id_parent)
VALUES ('cmt_001',
        'Super article Hugo ! J''ai appris plein de choses sur MongoDB. Est-ce que tu pourrais faire un tutoriel sur l''indexation ?',
        '2025-10-01 12:30:00',
        (SELECT id_article FROM Article WHERE titre = 'Pourquoi MongoDB est idéal pour les blogs modernes'),
        (SELECT id_utilisateur FROM Utilisateur WHERE email = 'alice@example.com'),
        NULL),
       ('cmt_001_rep_001',
        'Oui, un tutoriel sur l''indexation serait vraiment utile !',
        '2025-10-01 14:15:00',
        (SELECT id_article FROM Article WHERE titre = 'Pourquoi MongoDB est idéal pour les blogs modernes'),
        (SELECT id_utilisateur FROM Utilisateur WHERE email = 'bob@example.com'),
        'cmt_001'),
       ('cmt_001_rep_002',
        'Merci pour vos retours ! Je vais préparer ça pour la semaine prochaine.',
        '2025-10-01 15:45:00',
        (SELECT id_article FROM Article WHERE titre = 'Pourquoi MongoDB est idéal pour les blogs modernes'),
        (SELECT id_utilisateur FROM Utilisateur WHERE email = 'hugo@example.com'),
        'cmt_001');

-- Mariette article comments
INSERT INTO Commentaire (id_commentaire, contenu, date, id_article, id_utilisateur, id_parent)
VALUES ('cmt_002',
        'Evan, tu as parfaitement capté l''essence de son offre ! Mon produit préféré reste le café allongé !',
        '2025-09-28 11:20:00',
        (SELECT id_article FROM Article WHERE titre = 'Mariette : une révolution culinaire ?'),
        (SELECT id_utilisateur FROM Utilisateur WHERE email = 'bob@example.com'),
        NULL),
       ('cmt_002_rep_001',
        'Je suis d''accord avec Bob, le café allongé est une pépite !',
        '2025-09-28 13:05:00',
        (SELECT id_article FROM Article WHERE titre = 'Mariette : une révolution culinaire ?'),
        (SELECT id_utilisateur FROM Utilisateur WHERE email = 'alice@example.com'),
        'cmt_002'),
       ('cmt_002_rep_002',
        'Merci à vous deux ! C''est vrai que ce café est magique.',
        '2025-09-28 15:30:00',
        (SELECT id_article FROM Article WHERE titre = 'Mariette : une révolution culinaire ?'),
        (SELECT id_utilisateur FROM Utilisateur WHERE email = 'evan@example.com'),
        'cmt_002');

-- Git article comments
INSERT INTO Commentaire (id_commentaire, contenu, date, id_article, id_utilisateur, id_parent)
VALUES ('cmt_003',
        'Elisia, ton article est une vraie bouée de sauvetage ! J''ai déjà perdu des heures à cause de mauvaises manipulations Git. Merci pour ces astuces !',
        '2025-10-05 17:30:00',
        (SELECT id_article FROM Article WHERE titre = 'Git : les commandes qui sauvent la mise'),
        (SELECT id_utilisateur FROM Utilisateur WHERE email = 'alice@example.com'),
        NULL),
       ('cmt_003_rep_001',
        'Je plussoie ! La commande `git reflog` m''a sauvé plus d''une fois.',
        '2025-10-05 18:45:00',
        (SELECT id_article FROM Article WHERE titre = 'Git : les commandes qui sauvent la mise'),
        (SELECT id_utilisateur FROM Utilisateur WHERE email = 'bob@example.com'),
        'cmt_003'),
       ('cmt_003_rep_002',
        'Ravi que ça vous aide ! N''hésitez pas si vous avez d''autres questions.',
        '2025-10-05 19:10:00',
        (SELECT id_article FROM Article WHERE titre = 'Git : les commandes qui sauvent la mise'),
        (SELECT id_utilisateur FROM Utilisateur WHERE email = 'elisia@example.com'),
        'cmt_003');

-- Agile article comments
INSERT INTO Commentaire (id_commentaire, contenu, date, id_article, id_utilisateur, id_parent)
VALUES ('cmt_004',
        'Mathis, ton article est hilarant ET instructif ! J''adore la comparaison avec le tigre fou. Est-ce que tu as des conseils pour les équipes qui débutent en agile ?',
        '2025-09-25 10:15:00',
        (SELECT id_article FROM Article WHERE titre = 'Le tigre fou : une métaphore du développement agile ?'),
        (SELECT id_utilisateur FROM Utilisateur WHERE email = 'bob@example.com'),
        NULL),
       ('cmt_004_rep_001',
        'Oui, Mathis, des conseils pour éviter de se faire ''manger'' par le tigre ?',
        '2025-09-25 11:20:00',
        (SELECT id_article FROM Article WHERE titre = 'Le tigre fou : une métaphore du développement agile ?'),
        (SELECT id_utilisateur FROM Utilisateur WHERE email = 'alice@example.com'),
        'cmt_004'),
       ('cmt_004_rep_002',
        'Merci pour vos retours ! Mon premier conseil : ne jamais tourner le dos au tigre (aka toujours faire des rétrospectives). Je ferai un article plus détaillé sur le sujet !',
        '2025-09-25 12:00:00',
        (SELECT id_article FROM Article WHERE titre = 'Le tigre fou : une métaphore du développement agile ?'),
        (SELECT id_utilisateur FROM Utilisateur WHERE email = 'mathis@example.com'),
        'cmt_004');
