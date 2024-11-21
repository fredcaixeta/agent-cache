from groq import Groq
import os

client = Groq(
    api_key=os.environ.get("groq_key")    
)
system_message = (
    "Você receberá um histórico de queries. O usuário entregará mais uma query. Preciso que você me diga com qual query do histórico a query do usuário se aproxima. Responda apenas com a query semelhante."
)
# Lista para armazenar cada linha do histórico
history = []

with open("history_queries.txt", "r", encoding="utf-8") as file:
    for line in file:
        # Remove espaços extras e quebras de linha no final de cada linha
        line = line.strip()
        # Adiciona a linha ao histórico
        history.append(line)

# Exibe o conteúdo do histórico

history = ("\n".join(history))
#print(f"Histórico de consultas: {history}")
system_message = system_message + history

# Definindo a mensagem a ser enviada
messages = [
    {
        "role": "system",
        "content": system_message
    },
    {
        "role": "user",
        "content": "Quanto é 50 mais 30?"
    }
]

# Fazendo a chamada para obter a resposta do modelo
chat_completion = client.chat.completions.create(messages=messages, model='llama-3.1-70b-versatile')

print(f"response Groq: {chat_completion.choices[0].message.content}")
print(f"Total Tokens Groq: {chat_completion.usage.total_tokens}")

