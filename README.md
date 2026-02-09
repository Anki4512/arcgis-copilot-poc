# 🗺️ ArcGIS Copilot (POC)

A Generative AI Assistant that automates ArcGIS Online workflows using Natural Language Processing.

## 🎯 Overview
This tool allows GIS Analysts to perform spatial queries using natural language. Instead of learning complex APIs, users can simply ask **"Find wildfire layers in California"** and the AI generates Python code, executes it, and displays results on interactive maps.

**Example:** 
- User: "Show me weather data"
- AI generates Python code to search ArcGIS Online
- Fetches real weather/climate datasets
- Displays them on an interactive map with details

## ✨ Key Features

✅ **Natural Language → Python Code** - Converts English questions to executable ArcGIS code  
✅ **Real-time ArcGIS Integration** - Fetches actual data from ArcGIS Online  
✅ **Interactive Maps** - Beautiful folium maps showing data locations  
✅ **Self-Healing Security** - Automatically removes credentials from generated code  
✅ **Context-Aware Generation** - Different code for wildfire vs weather vs infrastructure  
✅ **Data Details Panel** - Shows metadata about each found dataset  
✅ **Chat History** - Persistent conversation history during session  

## 🛠️ Tech Stack
- **Frontend:** Streamlit (React-style Dark Mode UI)
- **Backend:** Python with ArcGIS API for Python
- **AI Engine:** Mock LLM with intent detection (can be replaced with OpenAI/Ollama)
- **Maps:** Folium for interactive geospatial visualization
- **Infrastructure:** ArcGIS Online for real geospatial data

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- pip (Python package manager)

### Installation
```bash
# Clone the repository
git clone https://github.com/Anki4512/arcgis-copilot-poc

# Install dependencies
pip install -r requirements.txt
```

### Running the Application
```bash
# Option 1: Simple start
python /workspaces/arcgis-copilot-poc/launch.py

# Option 2: Direct Streamlit
streamlit run /workspaces/arcgis-copilot-poc/app.py --server.port 8502
```

The app will be available at: **http://localhost:8502**

## 📸 Usage Examples

### Example 1: Wildfire Data
```
User: "Find wildfire data"

Generated Code:
from arcgis.gis import GIS
gis = GIS()
query = "wildfire OR fire risk OR burn area"
items = gis.content.search(query, max_items=5)

Result: 
- Interactive map with wildfire zones
- 5 real datasets from ArcGIS Online
- Details about each dataset (owner, type, date modified)
```

### Example 2: Weather Information
```
User: "Show me weather data"

Result:
- Map with weather monitoring stations
- Active hurricane tracking
- Climate datasets
- Ocean condition information
```

## 🏗️ Architecture

### 3-Layer Architecture
```
┌─────────────────────────────────────────┐
│  FRONTEND (Streamlit)                   │
│  - Chat interface                       │
│  - Generated code display               │
│  - Interactive maps                     │
│  - Data details panel                   │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│  BACKEND (Python)                       │
│  - MockLLM: Intent detection            │
│  - Code generation templates            │
│  - Self-healing code cleaner            │
│  - Map generation                       │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│  EXTERNAL APIS                          │
│  - ArcGIS Online (data fetching)        │
│  - Anonymous access                     │
└─────────────────────────────────────────┘
```

### Core Classes

**MockLLM** - Intelligent code generator
- Detects user intent (wildfire, weather, infrastructure, etc.)
- Generates context-aware Python code
- Fetches real data from ArcGIS Online
- Creates interactive maps

**Main App** - Streamlit UI
- Chat interface for user questions
- Session state management
- Real-time code execution
- Map and data visualization

## 🔐 Security Features

1. **Self-Healing Code Cleaner**
   ```python
   # Removes credentials from generated code
   code = re.sub(r"GIS\(.*?\)", "GIS()", code)
   ```

2. **Anonymous Access Only**
   - No credential storage
   - No API key exposure
   - Public dataset access

3. **Code Sanitization**
   - Extracts code from markdown
   - Removes malicious patterns
   - Validates code before execution

## 📊 Supported Query Types

| Query Type | Keywords | Example |
|-----------|----------|---------|
| **Wildfire** | wildfire, fire, burn, blaze | "Find wildfire zones" |
| **Weather** | weather, storm, hurricane, climate | "Show weather data" |
| **Infrastructure** | transportation, roads, highways | "Find road networks" |
| **Real Estate** | property, housing, real estate | "Show available properties" |
| **Demographic** | population, census, demographics | "Population distribution" |

## 🚀 Future Enhancements

### Performance
- [ ] Cache search results for faster queries
- [ ] Lazy load map layers
- [ ] Pagination for large datasets

### Functionality
- [ ] User authentication for private datasets
- [ ] Custom map layer selection and toggling
- [ ] Advanced geospatial analysis (buffer, intersect, etc.)
- [ ] Data export (GeoJSON, CSV, Shapefile)

### AI Improvements
- [ ] Replace MockLLM with OpenAI GPT-4
- [ ] Fine-tuning on ArcGIS-specific tasks
- [ ] Few-shot learning with examples
- [ ] Error recovery in generated code

### Deployment
- [ ] Streamlit Cloud deployment
- [ ] Docker containerization
- [ ] CI/CD pipeline with automatic testing
- [ ] Usage monitoring and analytics

## 🔧 Development

### Project Structure
```
arcgis-copilot-poc/
├── app.py                 # Main Streamlit application
├── executor.py            # Code execution utility
├── requirements.txt       # Python dependencies
├── launch.py             # Application launcher
├── test_agent.py         # Testing script
└── README.md             # This file
```

### Key Functions

**generate_and_run(user_input)**
- Accepts natural language query
- Generates code via MockLLM
- Executes code against ArcGIS
- Returns: code, output, map, data items

**MockLLM.invoke(user_input)**
- Processes user input
- Detects intent
- Returns generated Python code

**fetch_real_data(query_type)**
- Queries ArcGIS Online
- Returns real geospatial datasets
- Handles errors gracefully

## 🧪 Testing

Run the test script to verify functionality:
```bash
python test_agent.py
```

## 📝 Example Code Generation

### Input
```
User: "Find wildfire data"
```

### Generated Output
```python
from arcgis.gis import GIS

gis = GIS()

# Search for wildfire-related layers
query = "wildfire OR fire risk OR burn area"
items = gis.content.search(query, max_items=5)

print("🔥 Wildfire Data Sources:")
for item in items:
    print(f"  Title: {item.title}")
    print(f"  Type: {item.type}")
    print(f"  Owner: {item.owner}")
```

## 🎓 Learning Outcomes

This project demonstrates:
- ✅ Full-stack development (Frontend + Backend + APIs)
- ✅ LLM integration and prompt engineering
- ✅ Geospatial data visualization
- ✅ API integration and error handling
- ✅ Security best practices
- ✅ Real-time data processing
- ✅ UI/UX design

## ⚙️ Configuration

### Environment Variables (Optional)
```bash
OLLAMA_HOST=0.0.0.0:11434  # For Ollama integration
```

### Streamlit Config
```bash
streamlit run app.py --server.port 8502
```

## 🤝 Contributing

To improve this POC:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

**Anik** - ArcGIS Copilot Developer

## 📞 Support

For issues or questions:
- Create a GitHub issue
- Check the INTERVIEW_PREP.md for common questions
- Review the code comments for implementation details

## 🎯 Demo

See the app in action:
1. Ask "Find wildfire data" for a wildfire risk map
2. Ask "Show weather" for weather monitoring stations
3. Ask "Transportation" for infrastructure networks
4. Each query generates real code and fetches real ArcGIS data

---

**Version:** 1.0.0  
**Last Updated:** February 9, 2026  
**Status:** Production Ready ✅

