"""LangGraph workflow for travel planning."""
from langgraph.graph import StateGraph, END
from state import TravelState
from nodes import (
    research_destination,
    research_cuisine,
    plan_transportation,
    find_accommodation,
    get_weather,
    create_itinerary,
    calculate_budget,
    generate_final_plan
)


def create_travel_graph():
    """Create the travel planning graph."""
    
    # Initialize graph with state schema
    workflow = StateGraph(TravelState)
    
    # Add all planning nodes
    workflow.add_node("research_destination", research_destination)
    workflow.add_node("research_cuisine", research_cuisine)
    workflow.add_node("plan_transportation", plan_transportation)
    workflow.add_node("find_accommodation", find_accommodation)
    workflow.add_node("get_weather", get_weather)
    workflow.add_node("create_itinerary", create_itinerary)
    workflow.add_node("calculate_budget", calculate_budget)
    workflow.add_node("generate_final_plan", generate_final_plan)
    
    # Define the sequential flow
    workflow.set_entry_point("research_destination")
    
    workflow.add_edge("research_destination", "research_cuisine")
    workflow.add_edge("research_cuisine", "plan_transportation")
    workflow.add_edge("plan_transportation", "find_accommodation")
    workflow.add_edge("find_accommodation", "get_weather")
    workflow.add_edge("get_weather", "create_itinerary")
    workflow.add_edge("create_itinerary", "calculate_budget")
    workflow.add_edge("calculate_budget", "generate_final_plan")
    workflow.add_edge("generate_final_plan", END)
    
    return workflow.compile()


def run_travel_planner(
    origin: str,
    destination: str,
    travel_dates: str,
    interests: str,
    num_travelers: int
) -> str:
    """Run the travel planner graph and return the final plan."""
    
    # Create the graph
    graph = create_travel_graph()
    
    # Initialize state
    initial_state: TravelState = {
        "origin": origin,
        "destination": destination,
        "travel_dates": travel_dates,
        "interests": interests,
        "num_travelers": num_travelers,
        "destination_research": None,
        "cuisine_info": None,
        "transportation_info": None,
        "local_transport_info": None,
        "accommodation_info": None,
        "weather_info": None,
        "daily_itinerary": None,
        "budget_info": None,
        "final_plan": None,
        "current_step": "starting",
        "errors": []
    }
    
    # Run the graph
    final_state = graph.invoke(initial_state)
    
    return final_state.get("final_plan", "Error: No plan generated")
