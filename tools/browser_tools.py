import json
import requests
from crewai import Agent, Task
from langchain.tools import tool
from unstructured.partition.html import partition_html

class BrowserTools():
    @tool("scrape website content")
    def scrape_summarize_website(website):
        """Useful to scrape and summarize a website content"""

        url = "http://localhost:3000/content"
        payload = json.dumps({"url":website})
        headers = {'cache-control': 'no-cache', 'content-type': 'application/json'}

        try: 
            response = requests.post(url,headers = headers,data = payload)
            response.raise_for_status()
            content = response.txt
        except requests.exceptions.RequestException as e:
            print("error : {e}")
            return "error while fetching"
        
        elements = partition_html(text = content)
        text_content = "\n\n".join([str(el) for el in elements])

        chunk_size = 8000
        text_chunk = [text_content[i:i+chunk_size] for i in range(0,len(text_chunk),chunk_size)]

        summaries = []
        agent = Agent(
                    role='Principal Researcher',
                    goal='Do amazing researches and summaries based on the content you are working with',
                    backstory="You're a Principal Researcher at a big company and you need to do a research about a given topic.",
                    allow_delegation=False
                )
        for chunk in text_chunk:
            task = Task(
                    agent=agent,
                    description=f'Analyze and summarize the content bellow, make sure to include the most relevant information in the summary, return only the summary nothing else.\n\nCONTENT\n----------\n{chunk}'
                   )
            summary = task.execute()
            summaries.append(summary)
 
        return "\n\n".join(summaries)
            
