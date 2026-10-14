from langchain_core.tools import tool
from tavily import TavilyClient
from dotenv import load_dotenv
import requests
import numexpr
load_dotenv()

#                                                     Web Search Tool
@tool
def web_search(question:str)->str:
    '''
    Search the web for latest news, current events and real-time info.

    Args:
        question: The search query.
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



#                                                      Weather Tool
@tool
def weather_tool(city:str)->str:
    '''
    Get the current weather (temperature, wind speed, weather code) of a city.

    Args:
        city: Name of the city, e.g. "Meerut".
    '''
    try:
        # 1. Geocoding: city -> lat/lon
        geo = requests.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": city, "count": 1},
            timeout=10,
        ).json()

        # if city is not found then results key is not there
        if 'results' not in geo:
            return('city not found')

        # geo["results"][0] contains latitude, longitude and other information
        lat=geo['results'][0]['latitude']
        lon=geo['results'][0]['longitude']


        # 2. Forecast: lat/lon -> current weather
        weather = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": lat,
                "longitude": lon,
                "current": "temperature_2m,wind_speed_10m,weather_code",
            },
            timeout=10,
        ).json()

        temp=weather['current']['temperature_2m']
        wind_speed=weather['current']['wind_speed_10m']
        weather_code=weather['current']['weather_code']

        weather_condition=f'temp={temp}\n wind speed={wind_speed}\n weather_code= {weather_code}'

        return weather_condition

    except Exception as e:
        return (f'Weather tool failed ..{e}')


#                                                     Calculator Tool
@tool
def calculator(expression:str)->str:
    '''
    Evaluate a mathematical expression, e.g. "25 * 4 + 10".

    Args:
        expression: A math expression using numbers and operators only, no words.
    '''

    try:
        answer= numexpr.evaluate(expression).item()
        return str(answer)

    except Exception as e:
        return (f'error occured while solving the expression {e}')

