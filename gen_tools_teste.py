import math
import json

class Handle_Math():
    def __init__(self, cache):
        self.cache = cache 
        
    def handle_cache(self):
        try:
            
            # Salva o dicionário em um arquivo JSON
            with open("cache_new.json", "w") as json_file:
                json.dump(self.cache, json_file, indent=4)
            
            return "Arquivo JSON criado com sucesso"

        except ValueError:
            return "Erro: o formato de datetime fornecido é inválido."

    # Advanced calculator in Python
    # Function to perform addition
    def add(self, x, y):
        self.cache = self.cache['add']=(x,y)
        return x + y

    def calculate(self, operator, **args):
        if "y" in args:
            return eval(f"{operator}({args['x']}, {args['y']})")
        else:
            return eval(f"{operator}({args['x']})")
        
    def round(x, y):
        return round(x, y)
        
    def call_tools(self, tool, args):
        func = args['func']
        del args['func']
        print(tool)
        
        observation = eval(f'{tool}("{func}", **args)')
        return observation

"""
calculate
{'func': 'add', 'x': '10', 'y': '20'}

"""
calc = Handle_Math(cache={'adicione 2 mais 3':{}})

o = calc.call_tools('calculate', {'func':'add', 'x': '10', 'y': '20'})

calc.handle_cache()
