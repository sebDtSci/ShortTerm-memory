# Introduction

Nous présentons ici une approche pour la gestion de la mémoire à court terme dans les chatbots, en utilisant une combinaison de techniques de stockage et de résumé automatique pour optimiser le contexte conversationnel. La méthode introduite repose sur une structure de mémoire dynamique qui limite la taille des données tout en préservant les informations essentielles à travers des résumés intelligents. Cette approche permet non seulement d'améliorer la fluidité des interactions mais aussi d'assurer une continuité contextuelle lors de longues sessions de dialogue. En outre, l'utilisation de techniques asynchrones garantit que les opérations de gestion de la mémoire n'interfèrent pas avec la réactivité du chatbot.

# Utilisation du package `shortterm-memory`

Cette section explique comment utiliser le package `shortterm-memory` pour gérer la mémoire d'un chatbot.

## Installation
```bash
pip install shortterm-memory
```
```bash
pip show shortterm-memory
```
## Usage
```python
from shortterm_memory.ChatbotMemory import ChatbotMemory
```
## Exemple
```python	
from shortterm_memory.ChatbotMemory import ChatbotMemory

# Initialisation de la mémoire du chatbot
chat_memory = ChatbotMemory()

# Mettre à jour la mémoire avec un nouvel échange
user_input = "Bonjour, comment allez-vous?"
bot_response = "Je vais bien, merci ! Et vous ?"
chat_memory.update_memory(user_input, bot_response)

# Obtenir l'historique des conversations
historique = chat_memory.get_memory()
print(historique)
```

## Fonctionnalités disponibles
- **update_memory(user_input: str, bot_response: str)** : Met à jour l'historique des conversations avec une nouvelle paire question-réponse.

- **get_memory()** : Retourne l'historique complet des conversations sous forme de liste.

- **memory_counter(conv_hist: list) -> int** : Compte le nombre total de mots dans l'historique des conversations.

- **compressed_memory(conv_hist: list) -> list** : Comprime l'historique des conversations en utilisant un modèle de résumé.

## Gestion des erreurs
Assurez-vous que les entrées utilisateur et les réponses du bot sont des chaînes de caractères valides. Si l'historique devient trop grand, le package compresse automatiquement les anciennes conversations pour économiser de la mémoire.

# Modélisation Mathématique de la Gestion des Conversations

Dans cette section, nous formalisons mathématiquement la gestion de la mémoire de conversation dans le chatbot. La mémoire est structurée comme une liste de paires représentant les échanges entre l'utilisateur et le bot.

## Structure de la Mémoire de Conversation

La mémoire de conversation peut être définie comme une liste ordonnée de paires $(u_i, d_i)$, où $u_i$ représente l'entrée utilisateur et $d_i$ la réponse du bot pour le $i$-ième échange. Cette liste est notée $\mathcal{C}$ :

$$
\mathcal{C} = [(u_1, d_1), (u_2, d_2), \ldots, (u_n, d_n)]
$$

où $n$ est le nombre total d'échanges dans l'historique actuel.

## Mise à Jour de la Mémoire

Lorsqu'un nouvel échange se produit, une nouvelle paire $(u_{n+1}, d_{n+1})$ est ajoutée à la mémoire. Si la taille de $\mathcal{C}$ dépasse une limite maximale prédéfinie $M_{\text{max}}$, l'échange le plus ancien est retiré :

$$
\mathcal{C} = 
\begin{cases} 
\mathcal{C} \cup \{(u_{n+1}, d_{n+1})\}, & \text{si } |\mathcal{C}| < M_{\text{max}} \\
(\mathcal{C} \setminus \{(u_1, d_1)\}) \cup \{(u_{n+1}, d_{n+1})\}, & \text{si } |\mathcal{C}| = M_{\text{max}}
\end{cases}
$$

## Comptage des Mots

Pour gérer l'espace de mémoire et décider quand la compression est nécessaire, nous calculons le nombre total de mots $W(\mathcal{C})$ dans la mémoire :

$$
W(\mathcal{C}) = \sum_{(u_i, d_i) \in \mathcal{C}} (|u_i| + |d_i|)
$$

où $|u_i|$ et $|d_i|$ sont respectivement le nombre de mots dans $u_i$ et $d_i$.

## Compression de la Mémoire

Lorsque $W(\mathcal{C})$ dépasse un seuil $W_{\text{max}}$, la mémoire est compressée pour maintenir la pertinence du contexte. Cette compression est réalisée par un modèle de résumé $\mathcal{S}$, tel que BART :

$$
\mathcal{C}_{\text{compressed}} = \mathcal{S}(\mathcal{C})
$$

où $\mathcal{C}_{\text{compressed}}$ est la version résumée de la mémoire, réduisant le nombre total de mots tout en préservant l'essence des interactions passées.

## Intégration dans le Modèle de Langage

Le modèle de langage utilise le contexte compressé pour générer des réponses pertinentes. Le prompt $P$ utilisé par le modèle est construit comme suit :

$$
P = f(\mathcal{C}_{\text{compressed}}, \text{contexte})
$$

où $\text{contexte}$ est le contexte supplémentaire récupéré à partir d'un pipeline RAG, et $f$ est une fonction de concaténation qui prépare le texte pour le modèle.

Cette approche assure que le chatbot dispose toujours d'un contexte conversationnel à jour, permettant des interactions plus naturelles et engageantes avec l'utilisateur.
