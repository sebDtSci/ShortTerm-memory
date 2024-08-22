# Introduction

We present here an approach for managing short-term memory in chatbots, using a combination of storage techniques and automatic summarization to optimize conversational context. The introduced method relies on a dynamic memory structure that limits data size while preserving essential information through intelligent summaries. This approach not only improves the fluidity of interactions but also ensures contextual continuity during long dialogue sessions. Additionally, the use of asynchronous techniques ensures that memory management operations do not interfere with the chatbot's responsiveness.

# How to Use the `shortterm-memory` Package

This section explains how to use the `shortterm-memory` package to manage a chatbot's memory.

## Installation
```bash
pip install torch transformers
```
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
## Usage Exemple
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

## Available Features

- **update_memory(user_input: str, bot_response: str)**: Updates the conversation history with a new question-response pair.

- **get_memory()**: Returns the complete conversation history as a list.

- **memory_counter(conv_hist: list) -> int**: Counts the total number of words in the conversation history.

- **compressed_memory(conv_hist: list) -> list**: Compresses the conversation history using a summarization model.

## Error Handling

Ensure that user inputs and bot responses are valid strings. If the history becomes too large, the package automatically compresses older conversations to save memory.

# Mathematical Modeling of Conversation Management

In this section, we mathematically formalize conversation memory management in the chatbot. The memory is structured as a list of pairs representing exchanges between the user and the bot.

## Conversation Memory Structure

The conversation memory can be defined as an ordered list of pairs $(u_i, d_i)$, where $u_i$ represents the user input and $d_i$ the bot response for the $i$-th exchange. This list is denoted by $\mathcal{C}$:

$$
\mathcal{C} = [(u_1, d_1), (u_2, d_2), \ldots, (u_n, d_n)]
$$

where $n$ is the total number of exchanges in the current history.

## Memory Update

When a new exchange occurs, a new pair $(u_{n+1}, d_{n+1})$ is added to the memory. If the size of $\mathcal{C}$ exceeds a predefined maximum limit $M_{\text{max}}$, the oldest exchange is removed:

$$
\mathcal{C} = 
\begin{cases} 
\mathcal{C} \cup \{(u_{n+1}, d_{n+1})\}, & \text{si } |\mathcal{C}| < M_{\text{max}} \\
(\mathcal{C} \setminus \{(u_1, d_1)\}) \cup \{(u_{n+1}, d_{n+1})\}, & \text{si } |\mathcal{C}| = M_{\text{max}}
\end{cases}
$$

## Word Count

To manage memory space and decide when compression is necessary, we calculate the total number of words $W(\mathcal{C})$ in memory:

$$
W(\mathcal{C}) = \sum_{(u_i, d_i) \in \mathcal{C}} (|u_i| + |d_i|)
$$

where $|u_i|$ and $|d_i|$ are respectively the number of words in $u_i$ and $d_i$.

## Memory Compression

When $W(\mathcal{C})$ exceeds a threshold $W_{\text{max}}$, the memory is compressed to maintain the relevance of the context. This compression is performed by a summarization model $\mathcal{S}$, such as BART:

$$
\mathcal{C}_{\text{compressed}} = \mathcal{S}(\mathcal{C})
$$

where $\mathcal{C}_{\text{compressed}}$ is the compressed version of the memory, reducing the total number of words while preserving the essence of past interactions.

## Integration into the Language Model

The language model uses the compressed context to generate relevant responses. The prompt $P$ used by the model is constructed as follows:

$$
P = f(\mathcal{C}_{\text{compressed}}, \text{context})
$$

where $\text{context}$ is additional context retrieved from a RAG pipeline, and $f$ is a concatenation function that prepares the text for the model.

This approach ensures that the chatbot always has an up-to-date conversational context, enabling more natural and engaging interactions with the user.