from datetime import datetime
import os 

def save_md(content,filename_prefix="TravelPlan_", date_format="%Y-%m-%d", encoding="utf-8"):
    """
  Saves the provided content to a Markdown file with a timestamped filename within the "Travel Doc" folder.

  Args:
      task_output (object): The data to be saved as Markdown.
      filename_prefix (str, optional): Prefix for the filename. Defaults to "TravelPlan_".
      date_format (str, optional): Format string for the date in the filename. Defaults to "%Y-%m-%d" (YYYY-MM-DD).
      encoding (str, optional): Encoding for the file. Defaults to "utf-8".

  Returns:
      str: The filename of the saved Markdown file.
  """
     
    try:
        today_date = datetime.now().strftime(date_format)
        filename_md = f"{filename_prefix}{today_date}.md"
        travel_doc_folder = "Travel Doc"
        if not os.path.exists(travel_doc_folder):
         os.makedirs(travel_doc_folder)
        full_path = os.path.join(travel_doc_folder, filename_md)

        result = content.result if hasattr(content, 'result') else content
        if callable(result):
           result = result()
        if not isinstance(result,str):
           result = str(result) #for safety 

        with open(full_path, 'w', encoding=encoding) as file:
         file.write(result)

        print(f"Markdown file saved as: {full_path}")
        return full_path  # Return the filename for potential further processing
    
    except Exception as e:
       print("error while saving markdown : {e}")
       return None 

          
