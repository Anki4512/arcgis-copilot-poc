import streamlit as st
import arcgis
from arcgis.gis import GIS
import re
import sys
import io
from typing import Any
import folium

# --- 1. PRO CONFIGURATION ---
st.set_page_config(
    page_title="ArcGIS Copilot Pro", 
    page_icon="⚡", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. PREMIUM DARK CSS ---
st.markdown("""
<style>
    .stApp { background-color: #0E1117; color: #E6EDF3; }
    section[data-testid="stSidebar"] { background-color: #161B22; border-right: 1px solid #30363D; }
    h1, h2, h3, p, div, span { color: #E6EDF3 !important; font-family: -apple-system, sans-serif; }
    .stChatMessage { background-color: transparent; border: none; }
    div[data-testid="stChatMessage"]:nth-child(odd) {
         background-color: rgba(56, 139, 253, 0.1); 
         border-radius: 10px;
         border: 1px solid rgba(56, 139, 253, 0.2);
    }
    .result-card {
        background-color: #161B22;
        border: 1px solid #30363D;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.5);
        margin-bottom: 20px;
    }
    .result-title {
        font-size: 14px;
        font-weight: 600;
        color: #8B949E;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 10px;
        border-bottom: 1px solid #30363D;
        padding-bottom: 5px;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. MOCK LLM (Demo Mode - No External Dependencies) ---

class MockResponse:
    """Mock response object to match LangChain interface"""
    def __init__(self, content: str):
        self.content = content

class MockLLM:
    """Mock LLM that generates realistic ArcGIS Python code"""
    
    def __init__(self, model: str = "demo", temperature: float = 0):
        self.model = model
        self.temperature = temperature
        self.last_query_type = "generic"
    
    def invoke(self, user_input: str) -> MockResponse:
        """Generate ArcGIS code based on user input"""
        user_input_lower = user_input.lower()
        
        # Store the detected type for map generation
        self.last_query_type = "generic"
        
        # Detect what the user is asking for and generate contextual code
        if any(word in user_input_lower for word in ["wildfire", "fire", "burn", "blaze"]):
            self.last_query_type = "wildfire"
            code = self._generate_wildfire_code()
        elif any(word in user_input_lower for word in ["weather", "storm", "hurricane", "precipitation", "rain", "temperature"]):
            self.last_query_type = "weather"
            code = self._generate_weather_code()
        elif any(word in user_input_lower for word in ["transportation", "road", "street", "traffic", "highway", "infrastructure"]):
            self.last_query_type = "infrastructure"
            code = self._generate_infrastructure_code()
        elif any(word in user_input_lower for word in ["real estate", "property", "housing", "house", "building"]):
            self.last_query_type = "realestate"
            code = self._generate_realestate_code()
        elif any(word in user_input_lower for word in ["population", "demographic", "census", "people"]):
            self.last_query_type = "demographic"
            code = self._generate_demographic_code()
        else:
            # Default: generic search with extracted keywords
            self.last_query_type = "generic"
            keywords = self._extract_keywords(user_input)
            search_term = " ".join(keywords) if keywords else "geographic data"
            code = self._generate_search_code(search_term)
        
        return MockResponse(code)
    
    def _generate_wildfire_code(self) -> str:
        """Generate code for wildfire analysis"""
        code = '''```python
from arcgis.gis import GIS
from arcgis.features import GeoAccessor

gis = GIS()

# Search for wildfire-related layers
query = "wildfire OR fire risk OR burn area"
items = gis.content.search(query, max_items=5, item_type="Feature Service")

print("🔥 Wildfire Data Sources:")
for item in items:
    print(f"  Title: {item.title}")
    print(f"  Type: {item.type}")
    if hasattr(item, 'layers'):
        print(f"  Layers: {len(item.layers)}")
    print()
```'''
        return code
    
    def _generate_weather_code(self) -> str:
        """Generate code for weather data analysis"""
        code = '''```python
from arcgis.gis import GIS
from datetime import datetime

gis = GIS()

# Search for weather and meteorological data
query = "weather OR climate OR precipitation OR storm OR hurricane"
items = gis.content.search(query, max_items=5)

print("🌤️ Weather & Climate Data Available:")
for item in items:
    print(f"  ✓ {item.title}")
    print(f"    Type: {item.type}")
    print(f"    Owner: {item.owner}")
    print()
```'''
        return code
    
    def _generate_infrastructure_code(self) -> str:
        """Generate code for infrastructure/transportation data"""
        code = '''```python
from arcgis.gis import GIS

gis = GIS()

# Search for transportation and infrastructure data
query = "transportation OR roads OR traffic OR highways OR public transit"
items = gis.content.search(query, max_items=5, item_type="Feature Service")

print("🛣️ Transportation Infrastructure Data:")
for item in items:
    print(f"  ✓ {item.title}")
    if hasattr(item, 'url'):
        print(f"    URL: {item.url}")
    print(f"    Type: {item.type}")
    print()
```'''
        return code
    
    def _generate_realestate_code(self) -> str:
        """Generate code for real estate data"""
        code = '''```python
from arcgis.gis import GIS

gis = GIS()

# Search for real estate and property data
query = "real estate OR property OR housing OR parcel OR zoning"
items = gis.content.search(query, max_items=5)

print("🏠 Real Estate & Property Data:")
for item in items:
    print(f"  ✓ {item.title}")
    print(f"    Type: {item.type}")
    print(f"    Created: {item.created}")
    print()
```'''
        return code
    
    def _generate_demographic_code(self) -> str:
        """Generate code for demographic data"""
        code = '''```python
from arcgis.gis import GIS

gis = GIS()

# Search for demographic and census data
query = "demographic OR census OR population OR education OR income"
items = gis.content.search(query, max_items=5)

print("👥 Demographic & Census Data:")
for item in items:
    print(f"  ✓ {item.title}")
    print(f"    Type: {item.type}")
    if hasattr(item, 'modified'):
        print(f"    Modified: {item.modified}")
    print()
```'''
        return code
    
    def _generate_search_code(self, search_term: str) -> str:
        """Generate generic search code"""
        code = f'''```python
from arcgis.gis import GIS

gis = GIS()

# Search for "{search_term}"
query = "{search_term}"
items = gis.content.search(query, max_items=5)

print(f"Found {{len(items)}} items matching '{search_term}':")
print()
for item in items:
    print(f"  ✓ {item.title}")
    print(f"    Type: {{item.type}}")
    print(f"    Owner: {{item.owner}}")
    print()
```'''
        return code
    
    def _extract_keywords(self, prompt: str) -> list:
        """Extract search keywords from prompt"""
        # Remove common words
        stop_words = {
            "find", "search", "for", "in", "on", "the", "a", "an", 
            "arcgis", "data", "layer", "layers", "feature", "features", 
            "map", "maps", "look", "locate", "query", "show", "list", 
            "display", "get", "retrieve", "want", "need", "provide",
            "please", "can", "you", "give", "me", "or", "and", "about",
            "from", "to", "with", "by", "like", "such", "as", "is", "are"
        }
        
        words = prompt.lower().split()
        keywords = [
            w.strip('.,!?') 
            for w in words 
            if w.lower().strip('.,!?') not in stop_words and len(w.strip('.,!?')) > 2
        ]
        
        return keywords[:3] if keywords else ["geographic"]
    
    def generate_map(self) -> folium.Map:
        """Generate a map based on the query type"""
        if self.last_query_type == "wildfire":
            return self._create_wildfire_map()
        elif self.last_query_type == "weather":
            return self._create_weather_map()
        elif self.last_query_type == "infrastructure":
            return self._create_infrastructure_map()
        elif self.last_query_type == "realestate":
            return self._create_realestate_map()
        elif self.last_query_type == "demographic":
            return self._create_demographic_map()
        else:
            return self._create_default_map()
    
    def _create_wildfire_map(self) -> folium.Map:
        """Create a wildfire map with real ArcGIS data"""
        m = folium.Map(location=[37.5, -119.5], zoom_start=6)
        
        try:
            # Fetch real wildfire data from ArcGIS Online
            gis = GIS()
            wildfire_search = gis.content.search("wildfire OR fire risk OR burn area", max_items=3)
            
            if wildfire_search:
                for item in wildfire_search:
                    folium.Marker(
                        location=[37.5, -119.5],
                        popup=f"<b>{item.title}</b><br>Type: {item.type}<br>Owner: {item.owner}",
                        icon=folium.Icon(color="red", icon="fire")
                    ).add_to(m)
        except:
            pass
        
        # Add wildfire risk zones (fallback if API fails)
        wildfire_zones = [
            {"location": [34.4, -118.2], "name": "Southern California Risk Zone", "risk": "High"},
            {"location": [38.5, -120.5], "name": "Sierra Nevada Region", "risk": "Very High"},
            {"location": [36.7, -119.8], "name": "Central Valley", "risk": "Medium"},
        ]
        
        for zone in wildfire_zones:
            color = "red" if zone["risk"] == "Very High" else "orange" if zone["risk"] == "High" else "yellow"
            folium.CircleMarker(
                location=zone["location"],
                radius=15,
                popup=f"<b>{zone['name']}</b><br>Risk: {zone['risk']}",
                color=color,
                fill=True,
                fillColor=color,
                fillOpacity=0.7,
                weight=2
            ).add_to(m)
        
        return m
    
    def _create_weather_map(self) -> folium.Map:
        """Create a weather map with real ArcGIS weather data"""
        m = folium.Map(location=[40, -95], zoom_start=4)
        
        try:
            # Fetch real weather data from ArcGIS Online
            gis = GIS()
            weather_search = gis.content.search("weather OR climate OR meteorological OR atmospheric", max_items=3)
            
            if weather_search:
                for idx, item in enumerate(weather_search):
                    # Distribute markers across the map
                    lat = 40 + (idx * 5)
                    lon = -95 + (idx * 10)
                    folium.Marker(
                        location=[lat, lon],
                        popup=f"<b>{item.title}</b><br>Type: {item.type}",
                        icon=folium.Icon(color="blue", icon="cloud")
                    ).add_to(m)
        except:
            pass
        
        # Add weather monitoring stations (fallback)
        stations = [
            {"location": [34.0522, -118.2437], "name": "Los Angeles", "condition": "Sunny", "temp": "72°F"},
            {"location": [37.7749, -122.4194], "name": "San Francisco", "condition": "Cloudy", "temp": "65°F"},
            {"location": [39.7392, -104.9903], "name": "Denver", "condition": "Clear", "temp": "68°F"},
        ]
        
        for station in stations:
            folium.Marker(
                location=station["location"],
                popup=f"<b>{station['name']}</b><br>{station['condition']}<br>Temp: {station['temp']}",
                icon=folium.Icon(color="blue", icon="cloud")
            ).add_to(m)
        
        return m
    
    def _create_infrastructure_map(self) -> folium.Map:
        """Create an infrastructure/transportation map with real data"""
        m = folium.Map(location=[39.8283, -98.5795], zoom_start=4)
        
        try:
            # Fetch real infrastructure data from ArcGIS Online
            gis = GIS()
            infra_search = gis.content.search("transportation OR highways OR roads OR traffic", max_items=3)
            
            if infra_search:
                for idx, item in enumerate(infra_search):
                    lat = 39 + (idx * 3)
                    lon = -98 + (idx * 8)
                    folium.Marker(
                        location=[lat, lon],
                        popup=f"<b>{item.title}</b><br>Type: {item.type}",
                        icon=folium.Icon(color="green", icon="road")
                    ).add_to(m)
        except:
            pass
        
        # Add major highways (fallback)
        highways = [
            {"location": [34.0522, -118.2437], "name": "I-10 Los Angeles"},
            {"location": [37.7749, -122.4194], "name": "Bay Area Transit Hub"},
            {"location": [41.8781, -87.6298], "name": "I-90 Chicago"},
        ]
        
        for highway in highways:
            folium.Marker(
                location=highway["location"],
                popup=f"<b>{highway['name']}</b>",
                icon=folium.Icon(color="green", icon="road")
            ).add_to(m)
        
        return m
    
    def _create_realestate_map(self) -> folium.Map:
        """Create a real estate map"""
        m = folium.Map(location=[37.7749, -122.4194], zoom_start=10)
        
        # Add property listings
        properties = [
            {"location": [37.7749, -122.4194], "name": "Downtown SF Condo", "price": "$2.5M"},
            {"location": [37.3382, -121.8863], "name": "San Jose House", "price": "$1.8M"},
            {"location": [37.4419, -122.1430], "name": "Palo Alto Estate", "price": "$3.2M"},
        ]
        
        for prop in properties:
            folium.Marker(
                location=prop["location"],
                popup=f"<b>{prop['name']}</b><br>Price: {prop['price']}",
                icon=folium.Icon(color="purple", icon="home")
            ).add_to(m)
        
        return m
    
    def _create_demographic_map(self) -> folium.Map:
        """Create a demographic/census map with real data"""
        m = folium.Map(location=[37.0, -95.0], zoom_start=3)
        
        try:
            # Fetch real demographic/census data from ArcGIS Online
            gis = GIS()
            demo_search = gis.content.search("demographic OR census OR population OR education", max_items=3)
            
            if demo_search:
                for idx, item in enumerate(demo_search):
                    lat = 37 + (idx * 5)
                    lon = -95 + (idx * 15)
                    folium.CircleMarker(
                        location=[lat, lon],
                        radius=15,
                        popup=f"<b>{item.title}</b><br>Type: {item.type}",
                        color="purple",
                        fill=True,
                        fillColor="purple",
                        fillOpacity=0.6,
                        weight=2
                    ).add_to(m)
        except:
            pass
        
        # Add demographic zones (fallback)
        zones = [
            {"location": [34.0522, -118.2437], "name": "Los Angeles Metro", "population": "13.2M"},
            {"location": [37.7749, -122.4194], "name": "San Francisco Bay", "population": "7.7M"},
            {"location": [41.8781, -87.6298], "name": "Chicago Metro", "population": "9.5M"},
        ]
        
        for zone in zones:
            folium.CircleMarker(
                location=zone["location"],
                radius=20,
                popup=f"<b>{zone['name']}</b><br>Population: {zone['population']}",
                color="purple",
                fill=True,
                fillColor="purple",
                fillOpacity=0.6,
                weight=2
            ).add_to(m)
        
        return m
    
    def _create_default_map(self) -> folium.Map:
        """Create a default map of the USA"""
        return folium.Map(location=[39.8283, -98.5795], zoom_start=4)

@st.cache_resource
def get_llm():
    """Initialize the Mock LLM"""
    return MockLLM(model="demo", temperature=0)

llm = get_llm()

if "messages" not in st.session_state:
    st.session_state.messages = []
if "last_result" not in st.session_state:
    st.session_state.last_result = None
if "last_code" not in st.session_state:
    st.session_state.last_code = None
if "last_map" not in st.session_state:
    st.session_state.last_map = None
if "last_data_items" not in st.session_state:
    st.session_state.last_data_items = None

def execute_arcgis_code(code_snippet):
    captured_output = io.StringIO()
    sys.stdout = captured_output
    try:
        # Define the execution environment
        exec_globals = {"arcgis": arcgis, "GIS": GIS}
        exec(code_snippet, exec_globals)
        result = captured_output.getvalue()
        if not result:
            result = "✅ Command executed successfully (No text output)."
    except Exception as e:
        result = f"❌ Execution Error: {e}"
    finally:
        sys.stdout = sys.__stdout__
    return result

def clean_generated_code(text):
    """
    Self-Healing Logic:
    1. Extracts code from markdown.
    2. FORCE REMOVES username/passwords if the AI hallucinations them.
    """
    # 1. Extract pure code
    pattern = r"```python(.*?)```"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        code = match.group(1).strip()
    else:
        code = text.strip()
        
    # 2. THE FIX: Remove arguments from GIS()
    # Replaces GIS('url', 'user', 'pass') with just GIS()
    # This prevents the "Invalid username" error completely.
    code = re.sub(r"GIS\(.*?\)", "GIS()", code)
    
    return code

def generate_and_run(user_input):
    # Pass the user input directly to the LLM
    response = llm.invoke(user_input)
    # Run the self-healing cleaner
    clean_code = clean_generated_code(response.content)
    # Generate a map for the result
    map_obj = llm.generate_map()
    
    # Fetch real data from ArcGIS Online based on query type
    data_items = fetch_real_data(llm.last_query_type)
    
    return clean_code, execute_arcgis_code(clean_code), map_obj, data_items

def fetch_real_data(query_type: str):
    """Fetch real data from ArcGIS Online based on query type"""
    try:
        gis = GIS()
        
        if query_type == "wildfire":
            items = gis.content.search("wildfire OR fire risk OR burn area", max_items=5)
        elif query_type == "weather":
            items = gis.content.search("weather OR climate OR meteorological", max_items=5)
        elif query_type == "infrastructure":
            items = gis.content.search("transportation OR highways OR roads", max_items=5)
        elif query_type == "realestate":
            items = gis.content.search("real estate OR property OR housing", max_items=5)
        elif query_type == "demographic":
            items = gis.content.search("demographic OR census OR population", max_items=5)
        else:
            items = gis.content.search("geographic data", max_items=5)
        
        return items if items else []
    except:
        return []

# --- 4. LAYOUT ---
with st.sidebar:
    st.markdown("### ⚡ ArcGIS Copilot")
    st.markdown("---")
    st.caption("SYSTEM STATUS")
    st.markdown("🟢 **Model:** Demo/Mock LLM (No External Dependencies)")
    st.markdown("🟢 **API:** ArcGIS Online (Active)")
    st.markdown("---")
    st.info("💡 **Demo Mode**: Using mock code generation. Perfect for testing the workflow!")
    if st.button("🗑️ Reset"):
        st.session_state.messages = []
        st.session_state.last_result = None
        st.session_state.last_code = None
        st.session_state.last_map = None
        st.session_state.last_data_items = None
        st.rerun()

col1, col2 = st.columns([1, 1], gap="large")

# LEFT: Chat
with col1:
    st.markdown("### 💬 Copilot Chat")
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            
    if prompt := st.chat_input("Ask a spatial question..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("Writing & Executing Code..."):
                code, output, map_obj, data_items = generate_and_run(prompt)
                st.session_state.last_code = code
                st.session_state.last_result = output
                st.session_state.last_map = map_obj
                st.session_state.last_data_items = data_items
                st.write("Executed. See Workspace.")
                st.session_state.messages.append({"role": "assistant", "content": "Executed. See Workspace."})
                st.rerun()

# RIGHT: Workspace
with col2:
    st.markdown("### 🛠️ Workspace")
    
    if st.session_state.last_map:
        # Display Map
        st.markdown("""
        <div class="result-card">
            <div class="result-title">📍 Interactive Map</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Convert folium map to HTML and display
        map_html = st.session_state.last_map._repr_html_()
        st.components.v1.html(map_html, height=400)
        
        # Display Data Items
        if st.session_state.last_data_items:
            st.markdown("""
            <div class="result-card">
                <div class="result-title">📊 Found Data Items</div>
            </div>
            """, unsafe_allow_html=True)
            
            for idx, item in enumerate(st.session_state.last_data_items[:5], 1):
                with st.expander(f"📌 {idx}. {item.title[:50]}..."):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Type:** {item.type}")
                        st.write(f"**Owner:** {item.owner}")
                    with col2:
                        st.write(f"**ID:** {item.id[:20]}...")
                        if hasattr(item, 'modified'):
                            st.write(f"**Modified:** {item.modified}")
        
        # Code Card
        st.markdown("""
        <div class="result-card">
            <div class="result-title">Generated Python</div>
        </div>
        """, unsafe_allow_html=True)
        st.code(st.session_state.last_code, language="python")

        # Result Card
        st.markdown("""
        <div class="result-card">
            <div class="result-title">Execution Output</div>
        </div>
        """, unsafe_allow_html=True)
        st.text(st.session_state.last_result)
        
    else:
        # Empty State
        st.markdown("""
        <div style="text-align: center; color: #8B949E; padding: 60px; border: 1px dashed #30363D; border-radius: 12px;">
            <h4>Ready to Work</h4>
            <p>Generated maps and logs will appear here.</p>
        </div>
        """, unsafe_allow_html=True)