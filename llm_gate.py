import json
import os
from groq import Groq

import requests
import json
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

class Gate_Cache():
    def __init__(self, query) -> None:
        self.query = query
    
    def check_cache(self):
        print("Encontrando uma query semelhante no histórico de caches...")
        
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
        
        system_message = system_message + history
        
        llm_query = self.GroqCompletion(system_message=system_message, query=self.query)
        
        print("The LLM found a similar query:\n")
        
        return llm_query
    
    def llm_new_query(self, old_query):
        print("Ajustando a cache-query para estar de acordo com os valores atuais...")
        
        system_message = (
            "Você receberá um histórico de query de usuário e a sequencia necessária para se fazer as contas matemáticas. O usuário irá entregar uma nova query. Preciso que você ajuste a query dele ao molde da query anterior. Retorne apenas a query ajustada."
        )
        
        system_message = system_message + old_query
                
        o = self.GroqCompletion(system_message=system_message, query=self.query)
        
        print("The LLM found a similar query:\n")
        
        return o

    # Função para criar uma conclusão usando a API da OpenAI
    def GroqCompletion(self, system_message, query):
        client = Groq(
            api_key=os.environ.get("groq_key")    
        )
        
        # Definindo a mensagem a ser enviada
        messages = [
            {
                "role": "system",
                "content": system_message
            },
            {
                "role": "user",
                "content": query
            }
        ]

        # Fazendo a chamada para obter a resposta do modelo
        chat_completion = client.chat.completions.create(messages=messages, model='llama-3.1-70b-versatile')

        print(f"{chat_completion.choices[0].message.content}")
        print(f"Total de Tokens: {chat_completion.usage.total_tokens}")
        
        return chat_completion.choices[0].message.content
-
