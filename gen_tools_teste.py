import math
import json

def handle_cache(cache):
    try:
        # Cria um dicionário com a informação do datetime
        info_dict = {
            "data_hora": cache  # Armazena a data no formato ISO
        }
        
        # Salva o dicionário em um arquivo JSON
        with open("newjson.json", "w") as json_file:
            json.dump(info_dict, json_file, indent=4)
        
        return "Arquivo JSON criado com sucesso"

    except ValueError:
        return "Erro: o formato de datetime fornecido é inválido."

# Advanced calculator in Python
# Function to perform addition
def add(x, y, cache):
    return x + y
# Function to perform subtraction
def subtract(x, y, cache):
    return x - y
# Function to perform multiplication
def multiply(x, y, cache):
    return x * y
# Function to perform division
def divide(x, y, cache):
    if y == 0:
        return "Error! Division by zero."
    else:
        return x / y
# Function to perform power calculation (x^y)
def power(x, y, cache):
    return math.pow(x, y)
# Function to calculate square root
def square_root(x, cache):
    if x < 0:
        return "Error! Negative number cannot have a real square root."
    return math.sqrt(x)
# Function to calculate logarithm (base 10)
def logarithm(x, cache):
    if x <= 0:
        return "Error! Logarithm undefined for zero or negative numbers."
    return math.log10(x)
# Function to calculate sine of an angle (in degrees)
def sine(x, cache):
    return math.sin(math.radians(x))
# Function to calculate cosine of an angle (in degrees)
def cosine(x, cache):
    return math.cos(math.radians(x))
# Function to calculate tangent of an angle (in degrees)
def tangent(x, cache):
    return math.tan(math.radians(x))
def calculate(operator, cache, **args):
    if "y" in args:
        return eval(f"{operator}({args['x']}, {args['y']})")
    else:
        return eval(f"{operator}({args['x']})")
def round(x, y, cache):
    return round(x, y)
    
              
def call_tools(tool, args):
    func = args['func']
    del args['func']
    observation = eval(f'{tool}("{func}", **args)')
    return observation