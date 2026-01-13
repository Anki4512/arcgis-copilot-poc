from langchain_community.chat_models import ChatOllama
import re

# 1. Setup Local AI
llm = ChatOllama(model="llama3", temperature=0)

# 2. The User's Command
user_request = "Find 3 layers related to 'Wildfires' on ArcGIS Online."

# 3. The System Prompt (Instructions for the AI)
# We tell it to use 'GIS()' with no arguments for anonymous access
prompt = f"""
Write a Python script using the 'arcgis' library to:
1. Connect to ArcGIS Online anonymously (gis = GIS()).
2. {user_request}
3. Print the title of each item found.

IMPORTANT: Return ONLY the python code. No explanations. No markdown formatting.
"""

print(f"🤖 Copilot is thinking about: '{user_request}'...")
response = llm.invoke(prompt)
ai_code = response.content

# 4. Clean the Code (Remove ```python ... ``` if the AI adds it)
clean_code = re.sub(r"```python|```", "", ai_code).strip()

print("--- ⚡ EXECUTING CODE ⚡ ---")
print(clean_code)
print("--------------------------")

# 5. Run it!
try:
    exec(clean_code)
except Exception as e:
    print(f"❌ Error: {e}")
