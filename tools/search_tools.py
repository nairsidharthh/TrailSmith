import json
import os
import requests
from crewai.tools import tool


class SearchTools():

    @tool("Search the internet")
    @staticmethod
    def search(query: str) -> str:
        """
        Search the internet for information about a given topic.
        Use this to find current information about destinations, prices, 
        attractions, weather, and travel details.
        
        Args:
            query: A clear, specific search query string
            
        Returns:
            Search results with titles, links, and snippets
        """
        top_result_to_return = 5  # Increased for better coverage
        url = "https://google.serper.dev/search"
        
        api_key = os.getenv('SERPER_API_KEY')
        if not api_key:
            return SearchTools._fallback_response(query, "API key not configured")
        
        payload = json.dumps({"q": query})
        headers = {
            'X-API-KEY': api_key,
            'content-type': 'application/json'
        }
        
        try:
            response = requests.request(
                "POST", 
                url, 
                headers=headers, 
                data=payload,
                timeout=15  # 15 second timeout
            )
            response.raise_for_status()
            
            data = response.json()
            
            # Check if we have organic results
            if 'organic' not in data or not data['organic']:
                return SearchTools._fallback_response(query, "No search results found")
            
            results = data['organic']
            formatted_results = []
            
            for result in results[:top_result_to_return]:
                try:
                    formatted_results.append('\n'.join([
                        f"**{result.get('title', 'Untitled')}**",
                        f"Link: {result.get('link', 'N/A')}",
                        f"Summary: {result.get('snippet', 'No description available')}",
                        "-" * 40
                    ]))
                except KeyError:
                    continue
            
            if not formatted_results:
                return SearchTools._fallback_response(query, "Could not parse search results")
                
            return '\n'.join(formatted_results)
            
        except requests.exceptions.Timeout:
            return SearchTools._fallback_response(query, "Search request timed out")
        except requests.exceptions.RequestException as e:
            return SearchTools._fallback_response(query, f"Network error: {str(e)}")
        except json.JSONDecodeError:
            return SearchTools._fallback_response(query, "Invalid response from search API")
        except Exception as e:
            return SearchTools._fallback_response(query, f"Unexpected error: {str(e)}")
    
    @staticmethod
    def _fallback_response(query: str, error_reason: str) -> str:
        """
        Provide a helpful fallback response when search fails.
        This guides the agent to use their training knowledge instead.
        """
        return f"""
SEARCH NOTE: Could not complete search for "{query}".
Reason: {error_reason}

INSTRUCTION: Since real-time search is unavailable, please use your training knowledge to provide:
1. General information about this topic based on common knowledge
2. Typical prices, options, or details for similar destinations/situations
3. Reasonable estimates with a note that they should be verified

Do NOT say "information unavailable" - provide your best knowledge-based response instead.
"""