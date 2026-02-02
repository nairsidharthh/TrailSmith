from crewai import Task
from textwrap import dedent


class TravelTasks():
    def __tip_section(self):
        return "If you do your BEST WORK, I'll give you a $10,000 commission!"

    def __fallback_instruction(self):
        return dedent("""
            IMPORTANT: If the search tool fails or returns no results, DO NOT say "information unavailable".
            Instead, use your training knowledge to provide reasonable general information based on:
            - Common knowledge about the destination
            - Typical prices and options for similar destinations
            - Your expertise as a travel professional
            
            Always provide SOME useful information, even if it's general guidance.
        """)

    def Final_Trip_Plan(self, agent, context, origin, destination, travel_dates, interests, person, callback_function):
        """Final synthesis task for Trip Planner Agent."""
        return Task(
            description=dedent(f"""
                **Task**: Compile the final comprehensive travel plan document
                
                **Your Mission**:
                You will receive research from multiple specialized agents. Your job is to 
                synthesize ALL their findings into ONE cohesive, beautifully formatted markdown document.
                
                **Trip Parameters**:
                - From: {origin}
                - To: {destination}
                - Dates: {travel_dates}
                - Travelers: {person} person(s)
                - Interests: {interests}
                
                **Document Structure** (follow this EXACTLY):
                
                # Trip to [Destination]: [Dates]
                
                ## Trip Overview
                [2-3 sentence exciting summary of the trip]
                
                ## Getting There
                [Transportation options with costs and recommendations]
                
                ## Where to Stay
                [Accommodation recommendations with prices]
                
                ## Daily Itinerary
                [Day-by-day breakdown with activities, meals, timing]
                
                ## Local Cuisine & Dining
                [Food recommendations with restaurant suggestions]
                
                ## Weather & Packing
                [Weather forecast and what to pack]
                
                ## Budget Breakdown
                [Itemized costs with totals]
                
                ## Pro Tips
                [Cost-saving tips and travel advice]
                
                **CRITICAL RULES**:
                1. NEVER write "information unavailable" or "to be determined"
                2. NEVER include empty sections - every section must have content
                3. Fill in reasonable estimates if specific data is missing
                4. Calculate actual totals for the budget section
                5. Output ONLY the markdown document, no explanations
                
                {self.__tip_section()}
            """),
            agent=agent,
            context=context,
            callback=callback_function,
            expected_output=dedent("""
                A complete, well-formatted markdown travel document with all sections filled in.
                The document should be ready to share with the traveler with no placeholders or 
                missing information. Budget should include calculated totals.
            """),
        )

    def Research_Destination_Highlights(self, agent, origin, destination, travel_dates, interests, person):
        """Destination research task."""
        return Task(
            description=dedent(f"""
                **Task**: Research destination attractions and experiences
                
                Research the top attractions, experiences, and local customs for {destination}.
                Focus on what aligns with these interests: {interests}
                
                **Parameters**:
                - Destination: {destination}
                - Travel Dates: {travel_dates}
                - Number of Travelers: {person}
                - Interests: {interests}
                
                **What to Research**:
                1. Top 5-7 must-see attractions
                2. Hidden gems and local favorites
                3. Cultural experiences and customs
                4. Special events during {travel_dates}
                5. Activities matching "{interests}"
                
                **For Each Attraction, Include**:
                - Name and brief description
                - Why it's worth visiting
                - Estimated visit duration
                - Entry fee (if applicable)
                - Best time to visit
                
                {self.__fallback_instruction()}
                {self.__tip_section()}
            """),
            agent=agent,
            async_execution=False,
            expected_output=dedent("""
                A detailed list of 5-7 recommended attractions and experiences with:
                - Names and descriptions
                - Practical information (hours, prices, duration)
                - Why each is worth visiting
                All formatted in clear, readable sections.
            """),
        )

    def Discover_Local_Cuisine(self, agent, destination, travel_dates, person):
        """Local cuisine research task."""
        return Task(
            description=dedent(f"""
                **Task**: Research local cuisine and dining options
                
                Investigate {destination}'s culinary scene including must-try dishes and 
                recommended restaurants.
                
                **Parameters**:
                - Destination: {destination}
                - Travel Dates: {travel_dates}
                - Number of Travelers: {person}
                
                **What to Research**:
                1. 5+ Must-try local dishes with descriptions
                2. 3-5 Recommended restaurants across price ranges:
                   - Budget-friendly options
                   - Mid-range restaurants
                   - One special/upscale option
                3. Street food recommendations
                4. Food markets or food halls
                5. Dietary considerations (vegetarian options, etc.)
                
                **For Each Restaurant, Include**:
                - Name and cuisine type
                - Price range per person
                - Signature dishes
                - Location/neighborhood
                
                {self.__fallback_instruction()}
                {self.__tip_section()}
            """),
            agent=agent,
            async_execution=False,
            expected_output=dedent("""
                A comprehensive guide to local cuisine with:
                - List of must-try dishes with descriptions
                - Restaurant recommendations with prices and locations
                - Practical dining tips
            """),
        )

    def Find_Your_Perfect_Stay(self, agent, destination, travel_dates, person):
        """Accommodation research task."""
        return Task(
            description=dedent(f"""
                **Task**: Find accommodation options
                
                Find suitable accommodation in {destination} for {person} traveler(s) 
                during {travel_dates}.
                
                **Parameters**:
                - Destination: {destination}
                - Travel Dates: {travel_dates}
                - Number of Travelers: {person}
                
                **Provide Options in 3 Tiers**:
                
                1. **Budget** (hostels, budget hotels, basic stays)
                2. **Mid-Range** (standard hotels, nice Airbnbs)
                3. **Splurge** (luxury hotels, unique experiences)
                
                **For Each Option, Include**:
                - Name and type of accommodation
                - Nightly price (for {person} person(s))
                - Total estimated cost for stay
                - Key amenities
                - Location advantages
                - Why you recommend it
                
                {self.__fallback_instruction()}
                {self.__tip_section()}
            """),
            agent=agent,
            async_execution=False,
            expected_output=dedent("""
                3-5 accommodation options across budget tiers, each with:
                - Name, type, and pricing
                - Key amenities and location info
                - Clear recommendation rationale
            """),
        )

    def Transportation_Between_Destinations(self, agent, origin, destination, travel_dates, person):
        """Inter-city transportation planning task."""
        return Task(
            description=dedent(f"""
                **Task**: Plan transportation from origin to destination
                
                Research how to get from {origin} to {destination} for {person} traveler(s).
                
                **Parameters**:
                - From: {origin}
                - To: {destination}
                - Travel Dates: {travel_dates}
                - Travelers: {person}
                
                **Research These Options** (as applicable):
                1. **Flights**: Airlines, duration, price range
                2. **Trains**: Duration, classes, price range
                3. **Buses**: Duration, comfort level, price range
                4. **Driving**: Distance, time, considerations
                
                **For Each Option, Include**:
                - Mode of transport
                - Estimated duration
                - Price range (per person AND total for {person})
                - Pros and cons
                - Booking tips
                
                **Conclude with**: Your recommended best option and why.
                
                {self.__fallback_instruction()}
                {self.__tip_section()}
            """),
            agent=agent,
            async_execution=False,
            expected_output=dedent("""
                Comparison of transportation options from origin to destination with:
                - Multiple options with duration and pricing
                - Pros/cons for each
                - Clear best-option recommendation
            """),
        )

    def Plan_Local_Transportation(self, agent, destination, travel_dates, person):
        """Local transportation planning task."""
        return Task(
            description=dedent(f"""
                **Task**: Research local transportation options
                
                How to get around {destination} during the visit.
                
                **Parameters**:
                - Destination: {destination}
                - Travel Dates: {travel_dates}
                - Travelers: {person}
                
                **Research**:
                1. Public transit (metro, buses, trams)
                2. Taxis and ride-sharing (Uber, local apps)
                3. Rental options (cars, bikes, scooters)
                4. Walking friendliness
                
                **For Each Option, Include**:
                - How it works
                - Typical costs
                - Best for what situations
                - Any apps to download
                
                {self.__fallback_instruction()}
                {self.__tip_section()}
            """),
            agent=agent,
            async_execution=False,
            expected_output=dedent("""
                Guide to local transportation with:
                - Available options and how they work
                - Pricing information
                - Recommendations for different situations
            """),
        )

    def Info_Transportation_Passes(self, agent, destination, travel_dates, person):
        """Transportation passes research task."""
        return Task(
            description=dedent(f"""
                **Task**: Research transportation passes and discount options
                
                Find money-saving passes for transportation in {destination}.
                
                **Parameters**:
                - Destination: {destination}
                - Travel Dates: {travel_dates}
                - Travelers: {person}
                
                **Look For**:
                1. Tourist/city passes (transportation + attractions)
                2. Multi-day transit passes
                3. Airport transfer deals
                4. Any discount cards for tourists
                
                **For Each Pass, Include**:
                - Name and what it covers
                - Cost
                - Duration/validity
                - Whether it's worth it for this trip
                
                {self.__fallback_instruction()}
                {self.__tip_section()}
            """),
            agent=agent,
            async_execution=False,
            expected_output=dedent("""
                List of available passes with:
                - What each covers and costs
                - Value assessment for this specific trip
            """),
        )

    def Weather_Forecasts(self, agent, destination, travel_dates):
        """Weather forecast task."""
        return Task(
            description=dedent(f"""
                **Task**: Provide weather information
                
                Get weather information for {destination} during {travel_dates}.
                
                **Parameters**:
                - Destination: {destination}
                - Travel Dates: {travel_dates}
                
                **Provide**:
                1. **General Overview**: What's the weather typically like?
                2. **Temperature Range**: Expected highs and lows
                3. **Precipitation**: Rain/snow likelihood
                4. **What to Expect**: Humidity, sun, wind
                5. **Detailed Packing List** based on weather:
                   - Clothing essentials
                   - Footwear recommendations
                   - Accessories (umbrella, sunscreen, etc.)
                
                {self.__fallback_instruction()}
                
                NOTE: If you cannot get exact forecasts, provide seasonal averages 
                and historical patterns for this time of year.
                
                {self.__tip_section()}
            """),
            agent=agent,
            async_execution=False,
            expected_output=dedent("""
                Weather report with:
                - Temperature ranges and general conditions
                - What to expect day-to-day
                - Detailed packing recommendations
            """),
        )

    def Daily_Itineraries(self, agent, destination, travel_dates, interests, person):
        """Daily itinerary creation task."""
        return Task(
            description=dedent(f"""
                **Task**: Create detailed daily itineraries
                
                Build a day-by-day plan for the trip to {destination}.
                
                **Parameters**:
                - Destination: {destination}
                - Travel Dates: {travel_dates}
                - Interests: {interests}
                - Travelers: {person}
                
                **For EACH DAY of the trip, provide**:
                
                ### Day X: [Date] - [Theme/Area]
                
                **Morning** (specify times like 8:00 AM - 12:00 PM)
                - Activity with location
                - Why this timing works
                
                **Lunch** (around 12:00 - 1:30 PM)
                - Restaurant or food recommendation
                
                **Afternoon** (1:30 PM - 6:00 PM)
                - Activities with locations
                - Transportation between spots
                
                **Dinner** (around 7:00 - 9:00 PM)
                - Restaurant recommendation
                
                **Evening** (optional)
                - Nightlife or evening activity if applicable
                
                **Day's Budget Estimate**: [Amount]
                
                **RULES**:
                1. Cover EVERY day of {travel_dates}
                2. First day should account for arrival logistics
                3. Last day should account for departure
                4. Include realistic travel times between locations
                5. Balance busy and relaxed days
                6. Align activities with interests: {interests}
                
                {self.__fallback_instruction()}
                {self.__tip_section()}
            """),
            agent=agent,
            async_execution=False,
            expected_output=dedent("""
                Complete day-by-day itinerary covering every day of the trip with:
                - Time-blocked activities for each day
                - Meal recommendations
                - Transportation notes
                - Daily budget estimates
            """),
        )

    def Budget_Plan(self, agent, destination, travel_dates, person):
        """Budget analysis task."""
        return Task(
            description=dedent(f"""
                **Task**: Create comprehensive budget breakdown
                
                Analyze and estimate all costs for the {destination} trip.
                
                **Parameters**:
                - Destination: {destination}
                - Travel Dates: {travel_dates}
                - Travelers: {person}
                
                **Calculate Costs For**:
                
                | Category | Per Person | Total ({person} travelers) |
                |----------|------------|---------------------------|
                | Transportation (to/from) | $ | $ |
                | Accommodation | $ | $ |
                | Food & Dining | $ | $ |
                | Activities & Attractions | $ | $ |
                | Local Transportation | $ | $ |
                | Miscellaneous (tips, souvenirs) | $ | $ |
                | **TOTAL** | **$** | **$** |
                
                **Also Provide**:
                1. **Budget Tier Options**:
                   - Budget-conscious total
                   - Comfortable mid-range total
                   - Splurge total
                
                2. **Cost-Saving Tips** (at least 5):
                   - Specific ways to save money at this destination
                   - Free activities
                   - Best value options
                
                **RULES**:
                - Use actual numbers, not ranges like "$100-200"
                - Calculate totals correctly
                - Use consistent currency (USD preferred)
                - Be realistic, not overly optimistic
                
                {self.__fallback_instruction()}
                {self.__tip_section()}
            """),
            agent=agent,
            async_execution=False,
            expected_output=dedent("""
                Detailed budget breakdown with:
                - Itemized costs in table format
                - Per-person and total amounts
                - Multiple budget tier options
                - At least 5 specific cost-saving tips
            """),
        )