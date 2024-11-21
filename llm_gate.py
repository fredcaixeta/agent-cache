import json
import os
from groq import Groq

import requests
import json
from dotenv import load_dotenv

from transformers import AutoTokenizer

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

class Gate_Cache():
    def __init__(self, query):
        self.query = query
        self.tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")  # Escolha um tokenizer adequado.

    def check_cache(self):
        print("Encontrando uma query semelhante no histórico de caches...")

        system_message = (
            "Você receberá um histórico de queries. O usuário entregará mais uma query. Preciso que você me diga com qual query do histórico a query do usuário se aproxima. Responda apenas com a query semelhante."
        )
        
        # Tokenizar o histórico previamente
        history = []
        with open("history_queries.txt", "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                # Tokenize e armazene o histórico como IDs de tokens
                tokenized_line = self.tokenizer(line, return_tensors="pt", truncation=True, padding=True)
                history.append(tokenized_line)

        # Vetorizar o histórico em uma string legível para a API (ou ajuste conforme necessário)
        history_text = "\n".join([self.tokenizer.decode(h["input_ids"][0]) for h in history])
        
        # Adicione o histórico ao system_message
        system_message = system_message + history_text
        
        # Chamada para o Groq
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

        # Tokenizar system_message e query
        system_message_tokenized = self.tokenizer(system_message, return_tensors="pt", truncation=True, padding=True)
        query_tokenized = self.tokenizer(query, return_tensors="pt", truncation=True, padding=True)

        # Vetores de tokens
        system_message_vectors = system_message_tokenized["input_ids"].tolist()[0]
        query_vectors = query_tokenized["input_ids"].tolist()[0]

        print(f"Vetores de tokens (System): {system_message_vectors}")
        print(f"Vetores de tokens (Query): {query_vectors}")

        # Decodificar os tokens para strings antes de enviar à API
        system_message_decoded = self.tokenizer.decode(system_message_vectors, skip_special_tokens=True)
        query_decoded = self.tokenizer.decode(query_vectors, skip_special_tokens=True)

        messages = [
            {
                "role": "system",
                "content": system_message_decoded
            },
            {
                "role": "user",
                "content": query_decoded
            }
        ]

        # Fazendo a chamada para obter a resposta do modelo
        chat_completion = client.chat.completions.create(messages=messages, model='llama-3.1-70b-versatile')

        print(f"Resposta: {chat_completion.choices[0].message.content}")
        print(f"Total de Tokens: {chat_completion.usage.total_tokens}")
        return chat_completion.choices[0].message.content

