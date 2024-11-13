import math
import json

class Handle_Math:
    def __init__(self, cache):
        self.cache = cache 
        
    def handle_cache(self):
        try:
            # Salva o dicionário em um arquivo JSON
            with open("cache_new.json", "w") as json_file:
                json.dump(self.cache, json_file, indent=4)
            
        except ValueError:
            print("Erro: o formato de datetime fornecido é inválido.")

        try:
            # Abra o arquivo history.json para leitura
            with open("history.json", "r") as json_file:
                data = json.load(json_file)
        except (FileNotFoundError, json.JSONDecodeError):
            # Se o arquivo não existir ou estiver vazio, criamos um novo dicionário
            data = {}
        
        # Adiciona a nova entrada no dicionário
        data.update(self.cache)

        # Salva o arquivo com as novas informações
        with open("history.json", "w") as json_file:
            json.dump(data, json_file, indent=4)
            
    # Função de adição
    def add(self, x, y):
        # Atualiza o cache
        key = next(iter(self.cache))  # Pega a primeira chave do dicionário
        self.cache[key] = (x,y)
        
        return x + y

    # Função de cálculo que executa a operação especificada
    def calculate(self, operator, **args):
        x = float(args.get('x'))  # Converte x para float
        y = float(args.get('y')) if 'y' in args else None  # Converte y para float se estiver presente
        
        # Chama o operador diretamente
        if y is not None:
            return operator(x, y)
        else:
            return operator(x)

    # Função para arredondar
    def round(self, x, y):
        return round(x, y)
    
    # Função para chamar métodos dinamicamente
    def call_tools(self, tool, args):
        func = args['func']
        del args['func']
        
        # Converte x e y para números antes de chamar a função
        args['x'] = float(args['x'])
        if 'y' in args:
            args['y'] = float(args['y'])

        # Executa a função de cálculo com o operador correto
        return getattr(self, tool)(getattr(self, func), **args)

# Exemplo de uso
calc = Handle_Math(cache={'adicione 2 mais 3':{}})
resultado = calc.call_tools('calculate', {'func': 'add', 'x': '10', 'y': '20'})
print("Resultado:", resultado)  # Deve imprimir 30.0

# Salva o cache em JSON
calc.handle_cache()
