import json

def handle_json(cache, desc):
    """
    Atualiza o dicionário de cache adicionando a descrição da função chamada.
    
    Parâmetros:
        cache (dict): Dicionário que contém as descrições das funções.
        desc (str): Descrição da função a ser adicionada à lista na chave correspondente.
    
    Retorna:
        dict: O cache atualizado.
    """
    for key in cache:
        # Se a chave já existir no cache, adiciona a descrição na lista
    
        if isinstance(cache[key], list):
            cache[key].append(desc)
        else:
            cache[key] = [cache[key], desc]
                
    print(f"cache: {cache}")
    return cache

def soma(x, y, cache):
    # Chama handle_json para atualizar o cache com a descrição da função 'soma'
    cache = handle_json(cache, "soma")
    _ = x + y
    return _, cache

c_dict = {'some 3 mais 2':'divisão'}  # dicionário inicial com uma chave e valor

s, c = soma(3, 2, c_dict)
print(f"Resultado da soma: {s}")
print("Cache final:", c)
