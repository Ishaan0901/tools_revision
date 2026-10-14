from tools import web_search,calculator,weather_tool
from langgraph.graph import StateGraph, END, START, add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from typing import TypedDict, Annotated
load_dotenv()


#   Model:
llm=ChatGroq(
    model='openai/gpt-oss-20b'
)
tools=[web_search,calculator,weather_tool]
llm_with_tools=llm.bind_tools(tools)


#  State:
class ChatState(TypedDict):
    messages: Annotated[list,add_messages]


#                                                Nodes:

def query_node(state:ChatState):
    query=input('Human: ')
    return {'messages': query}



def llm_node(state:ChatState):
    messages=state['messages']
    response=llm_with_tools.invoke(messages)

    if response.content:
        print('AI:', response.content)

    return {'messages':[response]}



tool_node=ToolNode(tools)


def route_after_query(state):
    last = state['messages'][-1].content
    return END if last.lower() in ('exit', 'quit') else 'llm'



#                                           Graph

builder=StateGraph(ChatState)

builder.add_node('query_node',query_node)
builder.add_node('llm',llm_node)
builder.add_node('tools',tool_node)

builder.add_edge(START,'query_node')
builder.add_conditional_edges('query_node', route_after_query)
builder.add_conditional_edges('llm', 
                              tools_condition, {'tools': 'tools', END: 'query_node'})
builder.add_edge('tools','llm')

graph=builder.compile()



response = graph.invoke({'messages': []}, config={'recursion_limit': 100})
