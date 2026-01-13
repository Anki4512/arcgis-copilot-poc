from langchain_community.chat_models import ChatOllama

# 1. Setup the Local Brain
# We are using the free 'llama3' model running on your Mac
llm = ChatOllama(model="llama3", temperature=0)

# 2. Ask the Brain a Question
query = "Write a Python script using the 'arcgis' library to search for a 'Hurricanes' layer on ArcGIS Online."

print("Asking local AI... (this might take 10-20 seconds)")
response = llm.invoke(query)

# 3. Print the Result
print("--- LOCAL AI RESPONSE ---")
print(response.content)
