"""Planning nodes for the travel planner graph."""
import os
import time
import json
import requests
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage

load_dotenv()

# Initialize LLM with rate limit handling
def get_llm():
    return ChatGroq(
        api_key=os.getenv("GROQ_API_KEY"),
        model="llama-3.3-70b-versatile",
        temperature=0.7,
        max_retries=3,
    )

def search_web(query: str) -> str:
    """Search the internet using Serper API."""
    api_key = os.getenv('SERPER_API_KEY')
    if not api_key:
        return f"[Search unavailable - using general knowledge for: {query}]"
    
    try:
        response = requests.post(
            "https://google.serper.dev/search",
            headers={'X-API-KEY': api_key, 'content-type': 'application/json'},
            json={"q": query},
            timeout=10
        )
        data = response.json()
        
        if 'organic' not in data:
            return f"[No results for: {query}]"
        
        results = []
        for r in data['organic'][:3]:
            results.append(f"- {r.get('title', 'N/A')}: {r.get('snippet', 'N/A')}")
        return "\n".join(results)
    except Exception as e:
        return f"[Search failed: {str(e)}]"

def rate_limit_delay():
    """Add delay between LLM calls to avoid rate limits."""
    time.sleep(12)  # Groq free tier: 12K TPM, ~1 request per 12 seconds is safe

def call_llm(system_prompt: str, user_prompt: str) -> str:
    """Make LLM call with rate limiting and error handling."""
    llm = get_llm()
    
    try:
        response = llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ])
        rate_limit_delay()  # Wait after successful call
        return response.content
    except Exception as e:
        if "rate_limit" in str(e).lower():
            print("Rate limited, waiting 30 seconds...")
            time.sleep(30)
            return call_llm(system_prompt, user_prompt)  # Retry
        raise e


# ============== PLANNING NODES ==============

def research_destination(state: dict) -> dict:
    """Research destination attractions and experiences."""
    print("\n🔍 Researching destination...")
    
    search_results = search_web(f"{state['destination']} top attractions tourist places")
    
    prompt = f"""Research the best attractions and experiences in {state['destination']}.

Travel dates: {state['travel_dates']}
Traveler interests: {state['interests']}
Number of travelers: {state['num_travelers']}

Web search results:
{search_results}

Provide:
1. Top 5 must-see attractions with brief descriptions
2. 3 hidden gems or local favorites
3. Cultural experiences aligned with the traveler's interests
4. Any special events during the travel dates

Be specific with names and brief practical info."""

    result = call_llm(
        "You are a travel researcher. Provide concise, actionable travel information.",
        prompt
    )
    
    state['destination_research'] = result
    state['current_step'] = 'destination_research_complete'
    return state


def research_cuisine(state: dict) -> dict:
    """Research local cuisine and dining options."""
    print("\n🍜 Researching local cuisine...")
    
    search_results = search_web(f"{state['destination']} best restaurants local food")
    
    prompt = f"""Research dining options in {state['destination']}.

Web search results:
{search_results}

Provide:
1. 5 must-try local dishes
2. 3 restaurant recommendations (budget, mid-range, upscale)
3. Best areas for street food
4. Any food markets worth visiting

Include price ranges where possible."""

    result = call_llm(
        "You are a food and travel expert. Provide specific restaurant and cuisine recommendations.",
        prompt
    )
    
    state['cuisine_info'] = result
    state['current_step'] = 'cuisine_complete'
    return state


def plan_transportation(state: dict) -> dict:
    """Plan transportation to and within destination."""
    print("\n🚆 Planning transportation...")
    
    search_results = search_web(f"how to travel from {state['origin']} to {state['destination']}")
    
    prompt = f"""Plan transportation from {state['origin']} to {state['destination']}.

Travel dates: {state['travel_dates']}
Number of travelers: {state['num_travelers']}

Web search results:
{search_results}

Provide:
1. Available transport options (flights, trains, buses)
2. Estimated cost per person for each option
3. Travel duration for each
4. Your recommended best option and why
5. Local transportation options at destination

Be specific with prices and durations."""

    result = call_llm(
        "You are a transportation logistics expert. Provide practical travel advice with costs.",
        prompt
    )
    
    state['transportation_info'] = result
    state['current_step'] = 'transportation_complete'
    return state


def find_accommodation(state: dict) -> dict:
    """Find accommodation options."""
    print("\n🏨 Finding accommodation...")
    
    search_results = search_web(f"{state['destination']} best hotels accommodation")
    
    prompt = f"""Find accommodation in {state['destination']}.

Travel dates: {state['travel_dates']}
Number of travelers: {state['num_travelers']}

Web search results:
{search_results}

Provide 3 options across different budgets:
1. Budget option (hostel/budget hotel)
2. Mid-range option (standard hotel)
3. Splurge option (luxury hotel)

For each include: name, nightly rate, key amenities, location advantages."""

    result = call_llm(
        "You are an accommodation specialist. Provide specific hotel recommendations with prices.",
        prompt
    )
    
    state['accommodation_info'] = result
    state['current_step'] = 'accommodation_complete'
    return state


def get_weather(state: dict) -> dict:
    """Get weather forecast and packing recommendations."""
    print("\n🌤️ Getting weather info...")
    
    search_results = search_web(f"{state['destination']} weather {state['travel_dates']}")
    
    prompt = f"""Provide weather information for {state['destination']} during {state['travel_dates']}.

Web search results:
{search_results}

Include:
1. Expected temperature range (high/low)
2. Precipitation likelihood
3. General weather conditions
4. Packing recommendations based on weather

If exact forecast unavailable, provide typical weather for this time of year."""

    result = call_llm(
        "You are a travel weather advisor. Provide practical weather info and packing tips.",
        prompt
    )
    
    state['weather_info'] = result
    state['current_step'] = 'weather_complete'
    return state


def create_itinerary(state: dict) -> dict:
    """Create detailed daily itinerary."""
    print("\n📅 Creating daily itinerary...")
    
    prompt = f"""Create a day-by-day itinerary for a trip to {state['destination']}.

Trip details:
- From: {state['origin']}
- Dates: {state['travel_dates']}
- Interests: {state['interests']}
- Travelers: {state['num_travelers']}

Use this research:
ATTRACTIONS: {state.get('destination_research', 'N/A')[:500]}
DINING: {state.get('cuisine_info', 'N/A')[:300]}
WEATHER: {state.get('weather_info', 'N/A')[:200]}

Create a realistic daily plan:
- Day 1: Arrival + evening activity
- Middle days: Morning, lunch, afternoon, dinner, evening activities
- Last day: Morning activity + departure

Include specific timings, meal recommendations, and transport between sites."""

    result = call_llm(
        "You are an expert itinerary planner. Create detailed, realistic daily schedules.",
        prompt
    )
    
    state['daily_itinerary'] = result
    state['current_step'] = 'itinerary_complete'
    return state


def calculate_budget(state: dict) -> dict:
    """Calculate trip budget."""
    print("\n💰 Calculating budget...")
    
    prompt = f"""Calculate a budget for traveling to {state['destination']}.

Trip details:
- From: {state['origin']}
- Dates: {state['travel_dates']}
- Travelers: {state['num_travelers']}

Use this research:
TRANSPORT: {state.get('transportation_info', 'N/A')[:400]}
ACCOMMODATION: {state.get('accommodation_info', 'N/A')[:400]}
DINING: {state.get('cuisine_info', 'N/A')[:300]}

Create a budget table with:
| Category | Per Person | Total ({state['num_travelers']} travelers) |

Categories: Transportation, Accommodation, Food, Activities, Miscellaneous

Provide:
1. Budget estimate (minimum spend)
2. Comfortable mid-range estimate
3. 3-5 money-saving tips"""

    result = call_llm(
        "You are a travel budget analyst. Calculate realistic costs with actual numbers.",
        prompt
    )
    
    state['budget_info'] = result
    state['current_step'] = 'budget_complete'
    return state


def generate_final_plan(state: dict) -> dict:
    """Compile everything into final travel plan document."""
    print("\n📄 Generating final plan...")
    
    prompt = f"""Compile a complete travel plan document for a trip to {state['destination']}.

# Trip Overview
From: {state['origin']}
To: {state['destination']}
Dates: {state['travel_dates']}
Travelers: {state['num_travelers']}
Interests: {state['interests']}

# Research Data

## Destination Highlights
{state.get('destination_research', 'Not available')}

## Local Cuisine
{state.get('cuisine_info', 'Not available')}

## Transportation
{state.get('transportation_info', 'Not available')}

## Accommodation
{state.get('accommodation_info', 'Not available')}

## Weather & Packing
{state.get('weather_info', 'Not available')}

## Daily Itinerary
{state.get('daily_itinerary', 'Not available')}

## Budget
{state.get('budget_info', 'Not available')}

---

Create a beautiful, well-formatted markdown travel guide document.
Organize all the above information into clear sections.
Add a compelling introduction and helpful travel tips at the end.
The document should be ready to save and share."""

    result = call_llm(
        "You are a professional travel document writer. Create polished, comprehensive travel guides.",
        prompt
    )
    
    state['final_plan'] = result
    state['current_step'] = 'complete'
    return state
