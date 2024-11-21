from groq import Groq
import os

client = Groq(
    api_key=os.environ.get("groq_key")    
)
system_message = (
            "Você receberá um histórico de query de usuário e a sequencia necessária para se fazer as contas matemáticas. O usuário irá entregar uma nova query. Preciso que você ajuste a query dele ao molde da query anterior."
        )
old_query = """
{
    "Quanto é 5 mais 3? Depois divida o resultado por 2. Depois some 2": {
        "add": [
            5.0,
            3.0
        ],
        "divide": [
            8.0,
            2.0
        ]
        ,
        "add_": [
            4.0,
            2.0
        ]
    }
}
"""
system_message = system_message + old_query
                
new_query = "Quanto é 550 mais 300? Depois divida o resultado por 12. E some 30."

# Definindo a mensagem a ser enviada
messages = [
    {
        "role": "system",
        "content": system_message
    },
    {
        "role": "user",
        "content": new_query
    }
]

# Fazendo a chamada para obter a resposta do modelo
chat_completion = client.chat.completions.create(messages=messages, model='llama-3.1-70b-versatile')

print(f"response Groq: {chat_completion.choices[0].message.content}")
print(f"Total Tokens Groq: {chat_completion.usage.total_tokens}")

