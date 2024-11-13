import math
import json

# Advanced calculator in Python
class Handle_Math:
    def __init__(self, cache=None):
        self.cache = cache
        
    def handle_cache(self):
        try:
            # Salva o dicionário em um arquivo JSON sem usar Unicode para caracteres especiais
            with open("cache_new.json", "w", encoding="utf-8") as json_file:
                json.dump(self.cache, json_file, indent=4, ensure_ascii=False)

            
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
        with open("history.json", "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, indent=4, ensure_ascii=False)
        
    # Function to perform addition
    def add(self, x, y):
        key = next(iter(self.cache))  # Pega a primeira chave do dicionário
        print(f"self.cache: {self.cache}")
        self.cache[key]['add'] = (x,y)
        return x + y
    
    # Function to perform subtraction
    def subtract(x, y):
        return x - y
    
    # Function to perform multiplication
    def multiply(x, y):
        return x * y
    
    # Function to perform division
    def divide(x, y):
        if y == 0:
            return "Error! Division by zero."
        else:
            return x / y
        
    # Function to perform power calculation (x^y)
    def power(x, y):
        return math.pow(x, y)
    
    # Function to calculate square root
    def square_root(x):
        if x < 0:
            return "Error! Negative number cannot have a real square root."
        return math.sqrt(x)
    
    # Function to calculate logarithm (base 10)
    def logarithm(x):
        if x <= 0:
            return "Error! Logarithm undefined for zero or negative numbers."
        return math.log10(x)
    
    # Function to calculate sine of an angle (in degrees)
    def sine(x):
        return math.sin(math.radians(x))
    
    # Function to calculate cosine of an angle (in degrees)
    def cosine(x):
        return math.cos(math.radians(x))
    
    # Function to calculate tangent of an angle (in degrees)
    def tangent(x):
        return math.tan(math.radians(x))

    # Função de cálculo que executa a operação especificada
    def calculate(self, operator, **args):
        x = float(args.get('x'))  # Converte x para float
        y = float(args.get('y')) if 'y' in args else None  # Converte y para float se estiver presente
        
        # Chama o operador diretamente
        if y is not None:
            return operator(x, y)
        else:
            return operator(x)
        
    def round(x, y):
        return round(x, y)    
                
    def call_tools(self, tool, args):
        func = args['func']
        del args['func']
        
        # Converte x e y para números antes de chamar a função
        args['x'] = float(args['x'])
        if 'y' in args:
            args['y'] = float(args['y'])

        # Executa a função de cálculo com o operador correto
        return getattr(self, tool)(getattr(self, func), **args)

if __name__ == "__main__":
    """
    calculate
    {'func': 'add', 'x': '10', 'y': '20'}

    """

    o = Handle_Math.call_tools('calculate', {'x': '10', 'func':'add', 'y': '20'})