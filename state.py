"""State schema for the travel planner graph."""
from typing import TypedDict, Optional


class TravelState(TypedDict):
    """Shared state across all nodes in the travel planning graph."""
    
    # Input parameters
    origin: str
    destination: str
    travel_dates: str
    interests: str
    num_travelers: int
    
    # Research outputs (populated by nodes)
    destination_research: Optional[str]
    cuisine_info: Optional[str]
    transportation_info: Optional[str]
    local_transport_info: Optional[str]
    accommodation_info: Optional[str]
    weather_info: Optional[str]
    daily_itinerary: Optional[str]
    budget_info: Optional[str]
    
    # Final output
    final_plan: Optional[str]
    
    # Status tracking
    current_step: str
    errors: list[str]
