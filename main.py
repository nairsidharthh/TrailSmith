"""Travel Planner - LangGraph Edition"""
import os
from datetime import datetime
from dotenv import load_dotenv
from graph import run_travel_planner

load_dotenv()


def save_plan(content: str, destination: str) -> str:
    """Save the travel plan to a markdown file."""
    folder = "Travel Doc"
    os.makedirs(folder, exist_ok=True)
    
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"TravelPlan_{destination.replace(' ', '_').replace(',', '')}_{date_str}.md"
    filepath = os.path.join(folder, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return filepath


def main():
    print("=" * 60)
    print("   TRAVEL PLANNER - LangGraph Edition")
    print("=" * 60)
    print()
    
    # Trip parameters
    origin = "Dhanbad, Jharkhand, India"
    destination = "Delhi, India"
    travel_dates = "1st October, 2025 - 5th October, 2025"
    interests = "Historical monuments, famous landmarks, local street food, photography spots"
    num_travelers = 3
    
    print(f"📍 From: {origin}")
    print(f"📍 To: {destination}")
    print(f"📅 Dates: {travel_dates}")
    print(f"👥 Travelers: {num_travelers}")
    print(f"❤️ Interests: {interests}")
    print()
    print("-" * 60)
    print("Starting travel planning workflow...")
    print("(This will take a few minutes due to rate limiting)")
    print("-" * 60)
    
    try:
        # Run the planner
        final_plan = run_travel_planner(
            origin=origin,
            destination=destination,
            travel_dates=travel_dates,
            interests=interests,
            num_travelers=num_travelers
        )
        
        # Save to file
        filepath = save_plan(final_plan, destination)
        
        print()
        print("=" * 60)
        print("✅ TRAVEL PLAN COMPLETE!")
        print(f"📁 Saved to: {filepath}")
        print("=" * 60)
        print()
        print(final_plan)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        raise


if __name__ == "__main__":
    main()
