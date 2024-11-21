import gen_tools as tools
from llm_gate import Gate_Cache

import json

from langchain_core.prompts import PromptTemplate
from langchain_core.messages import AIMessage
from langchain_groq import ChatGroq

from dotenv import load_dotenv
load_dotenv()
import os

template = '''Answer the following questions as best you can. 
You have access to the following tools:{tools}
Use the following format strictly:
Question: the input question you must answer. Do not repeat this.
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action comma seperated
Then return "PAUSE". Do not perform any action on your own.
Observation: the result of the action
... (this Thought/Action/Action Input/PAUSE/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question
Begin!
Question: {input}
Thought: {agent_scratchpad}'''

prompt = PromptTemplate.from_template(template)

tool_desc = f"""calculate: this tool is useful for calculating the mathematical 
              expressions such as add, subtract, divide, multiply, power, 
              square_root, sine, cosine, tagent. There is also round for reasonable number of decimal places. This tool expects the 
              operation needed and the numbers are parameters"""
              
client = ChatGroq(
    api_key=os.environ.get("groq_key"),
    model_name='llama-3.1-70b-versatile'
)

def parse(ai_message: AIMessage) -> str:
    """Parse the AI message."""
    #print("Using parse")
    tokens = []
    times = []
    tokens.append(ai_message.response_metadata.get('token_usage').get('total_tokens'))
    times.append(ai_message.response_metadata.get('token_usage').get('total_time'))
    with open("token_usage.txt", "w", encoding="utf-8") as file:
        token = 0
        for token in tokens:
            token = token + token 
        token = str(token)
        file.write(token)
    
    with open("total_time.txt", "w", encoding="utf-8") as file:
        time = 0
        for time in times:
            time = time + time 
        time = str(time)
        file.write(time)
        
    #print(f"Usage: {ai_message.response_metadata.get('token_usage').get('total_tokens')} tokens")
    #print(f"Total time: {ai_message.response_metadata.get('token_usage').get('total_time')} seconds")
    result = ai_message.content
    if result.lower().startswith("thought"):
        result = result[8:].strip()
    #print(result)
    return result

def post_process_response(result):
    lines = result.split("\n")
    tool, parameters = None, None
    answer_found = False
    for line in lines:
        if len(line)> 0:
            if line.lower().startswith("thought"):
                continue
            elif line.lower().startswith("final answer:"):
                answer_found = True
                return answer_found, line.split(":")[-1].strip()
            elif line.lower().startswith("action:"):
                tool = line.split(":")[-1].strip()
            elif line.lower().startswith("action input:"):
                parameters = line.split(":")[-1].strip()
    
    if tool is None:
        raise Exception("tool not detected by model")
    
    if parameters is None:
        raise Exception("parameters not detected by model")
    else:
        params_list = parameters.split(",")
        #print(f"params_list: {params_list}")
        func = params_list[0].strip()
        args = {}
        args["func"] = func
        args["x"] = params_list[1].strip()
        if len(params_list)>2:
            args["y"]=params_list[2].strip()  
    
    return answer_found, (tool, args)

def myAgent(query, query_dict):
    agent_scratchpad = ""
    chain = prompt | client | parse
    #print(f"This is the chain: {chain}")
    count, max_loop = 0, 10 
    #print("Thought: ", end=" ")

    while count<max_loop:
        #print(f"count: {count}")
        req = chain.invoke({"input":query, "tools":tool_desc, "tool_names": "calculate", "agent_scratchpad" : agent_scratchpad})
        #print(f"agent_scratchpad: {agent_scratchpad}")
        #print("Request: ")
        #print(req, end =" ")
        answer_found, response = post_process_response(req)
        
        #print(f"response: {response}")
        if answer_found:
            # print("\n")
            # print(f"agent_scratchpad: {agent_scratchpad}")
            # print(f"req: {req}")
            agent_scratchpad = f"{agent_scratchpad}{req}"
            return response, agent_scratchpad
        else:
            calc = tools.Handle_Math(cache=query_dict)
            observation = calc.call_tools(response[0], response[1])
            
            # print(f"\nObervation: {observation}\nThought:", end=" ")
            agent_scratchpad = f"{agent_scratchpad}{req}\nObservation: {observation}\nThought:"
            
        count+=1
        
def handle_str_json(dado):
    data_str = dado.replace("'", "\"")  # Substitui aspas simples por aspas duplas
    try:
        data_json = data_str
        data_dict = json.loads(data_json)
    except:
        data_json = "{" + data_str + "}"
        data_dict = json.loads(data_json)
    # Convertendo para JSON
    data_dict = json.loads(data_json)
    return data_dict
        
def myAgent_Cache(llm_query):
    with open("history_math.json", "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
    #print(f"todas as queries com os calculos: {data}")
    #print(f"nova query formulada pela llm: {llm_query}")
    
    for key in data:
        #print(key)
        if str(key).strip() == str(llm_query).strip():
            print("match!") # match! aqui foi encontrado a query que coincide com a query do historico
            pass
            break
    
    llm_data = Gate.llm_new_query(str(data)) # entregar à LLM a query "correta", mas receber de volta ajustada - com os numeros da atual query ajustados no dicionario
    llm_data = handle_str_json(llm_data)
    
    key = next(iter(llm_data)) #pegando a nova key do novo json da nova query
    
    actions_keys = llm_data[key]
    length = len(actions_keys)
    for i, action_dict in enumerate(actions_keys):  # Itera com índice e item
        # Extrai a ação (chave) e os valores (lista de números)
        for action, values in action_dict.items():
            calc = tools.Handle_Math(cache=False)  # False -> do not store info for cache - would be duplicated

            # Configura os argumentos para a função de cálculo
            args = {
                'func': action,
                'x': values[0],
            }

            # Inclui `y` se houver dois valores
            if len(values) > 1:
                args['y'] = values[1]

            # Chama a função e obtém o resultado
            observation = calc.call_tools('calculate', args)

            # Verifica se é a última operação
            if i == length - 1:  # O índice do último item é len(actions_keys) - 1
                print(f"Cache Observation: {action} Final Response - {observation}")
            else:
                print(f"Cache Observation: {action} Response - {observation}")

        
if __name__ == "__main__":
    cache = True # True or False - Either go with strategy of cache, or not
    query = "If I settle my $1,000 debt now, what would the total be with a 10% discount?"
    
    
    print("******************************")
    if cache: # encontrada uma query parecida do .txt pela LLM
        Gate = Gate_Cache(query=query)
        # Check if a similar query is found in History of Queries
        llm_query = Gate.check_chache()
        if llm_query:
            print("Cache Strategy: ON")
            myAgent_Cache(llm_query=llm_query)
        else:
            print("No Similar Query found in History. Cancelling Cache Strategy.")

    else:
        print("Cache Strategy: OFF")
        query_dict = {query:[]}
        res, agent_scratchpad = myAgent(query=query, query_dict=query_dict)
        
        #print(f"Query: {query}")
        write_file_history = tools.Handle_Math(query=query)
        _ = write_file_history.handle_history_queries()
        _ = tools.Handle_Math(cache=query_dict)
        print(agent_scratchpad)
        
    print("******************************")
        # calc = tools.Handle_Math(cache=query_dict)
        # calc.handle_cache()
      