# Introduction

Nous présentons ici une approche pour la gestion de la mémoire à court terme dans les chatbots, en utilisant une combinaison de techniques de stockage et de résumé automatique pour optimiser le contexte conversationnel. La méthode introduite repose sur une structure de mémoire dynamique qui limite la taille des données tout en préservant les informations essentielles à travers des résumés intelligents. Cette approche permet non seulement d'améliorer la fluidité des interactions mais aussi d'assurer une continuité contextuelle lors de longues sessions de dialogue. En outre, l'utilisation de techniques asynchrones garantit que les opérations de gestion de la mémoire n'interfèrent pas avec la réactivité du chatbot.

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
