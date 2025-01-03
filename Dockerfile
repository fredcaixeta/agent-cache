# Usar uma imagem base do AWS Lambda com Python
FROM public.ecr.aws/lambda/python:3.9

# Copiar os arquivos do projeto para o contêiner
COPY main.py gen_tools.py llm_gate.py history_math.json history_queries.txt token_usage.txt total_time.txt cache_new.json./

# Instalar as dependências
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Definir o handler (nome do arquivo + nome da função principal)
CMD ["main.lambda_handler"]
