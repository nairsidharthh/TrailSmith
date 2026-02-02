# TrailSmith 🌍✈️

TrailSmith is an intelligent travel planning system powered by **LangGraph** and **CrewAI**. It orchestrates a team of specialized AI agents to generate comprehensive, personalized travel itineraries based on your preferences, budget, and schedule.

## 🚀 Project Overview

The system acts as a "Senior Travel Consultant" managed by a graph workflow. It coordinates multiple specialized agents to research and compile a complete travel document:

*   **Destination Research Specialist**: Finds attractions, hidden gems, and local customs.
*   **Local Cuisine Expert**: Recommends vegetarian-friendly restaurants (default preference), local dishes, and food experiences.
*   **Accommodation Specialist**: Finds stays across budget tiers (Budget, Mid-Range, Luxury).
*   **Transportation Logistics Expert**: Plans travel *to* the destination and *around* the city.
*   **Weather Advisor**: Provides forecasts and packing lists.
*   **Itinerary Planner**: Creates detailed day-by-day schedules.
*   **Budget Analyst**: Estimates total costs and provides money-saving tips.

The final output is a beautifully formatted Markdown travel plan saved to the `Travel Doc` folder.

## 🛠️ Tech Stack

*   **Language**: Python 3.11
*   **Orchestration**: [LangGraph](https://langchain-ai.github.io/langgraph/) & [CrewAI](https://crewai.com)
*   **LLM Provider**: Google Gemini (`gemini-1.5-flash`)
*   **Search Tool**: [SerperDev](https://serper.dev) (Google Search API)
*   **Environment Management**: `python-dotenv`

## ⚙️ How to Setup Locally

### Prerequisites
*   Python 3.11 or higher installed.
*   API Keys for:
    *   **Google Gemini**: [Get API Key](https://aistudio.google.com/app/apikey)
    *   **Serper Dev**: [Get API Key](https://serper.dev)

### Installation

1.  **Clone the repository**
    ```bash
    git clone <repository_url>
    cd travel_crew
    ```

2.  **Create and activate a virtual environment** (Recommended)
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables**
    Create a `.env` file in the root directory and add your API keys:
    ```env
    GOOGLE_API_KEY=your_google_api_key_here
    SERPER_API_KEY=your_serper_api_key_here
    ```

### Usage

Run the main travel planner script:

```bash
python main.py
```

The script will:
1.  Initialize the agent workflow.
2.  Research your destination (this may take a few minutes).
3.  Generate a detailed travel plan.
4.  Save the plan as a Markdown file in the `Travel Doc/` directory.

To customize the trip (origin, destination, dates, etc.), currently, you can modify the `main()` function in `main.py`.


# main.py -> inputs 
origin = "Dhanbad,India"
destination = "Delhi, India"
travel_dates = "2026-03-20 to 2026-03-24"

