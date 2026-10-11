from langchain_core.tools import tool
from tavily import TavilyClient
from dotenv import load_dotenv
load_dotenv()


@tool
def web_search(question:str)->str:
    '''
    This tool is used to search the web for latest news, current events, real-time info.
    '''

    try:
        tavily=TavilyClient()
        
        response=tavily.search(question,max_results=3)

        results=[]
        for r in response['results']:
            title=r['title']
            url=r['url']
            content=r['content']

            final_response=f'{title},{url},{content}'
            results.append(final_response)

        answer='\n\n'.join(results)
        return answer
        
    except Exception as e:
        return f'search failed ..{e}'
