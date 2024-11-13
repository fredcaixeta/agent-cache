import gen_tools as tools

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
    print(f"ai message: {ai_message}")
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
            agent_scratchpad = f"{agent_scratchpad}{req}\nObervation: {observation}\nThought:"
        count+=1  

if __name__ == "__main__":
    query = "Quanto é 5 mais 2? E o resultado multiplicado por 3.2?"
    query_dict = {query:{}}
    res, agent_scratchpad = myAgent(query=query, query_dict=query_dict)
    print(agent_scratchpad)
    calc = tools.Handle_Math(cache=query_dict)
    calc.handle_cache()