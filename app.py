import streamlit as st
from langchain_community.chat_models import ChatOllama
import arcgis
from arcgis.gis import GIS
import re
import sys
import io

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

# --- 3. LOGIC (The Brain) ---
@st.cache_resource
def get_llm():
    return ChatOllama(model="llama3", temperature=0)

llm = get_llm()

if "messages" not in st.session_state:
    st.session_state.messages = []
if "last_result" not in st.session_state:
    st.session_state.last_result = None
if "last_code" not in st.session_state:
    st.session_state.last_code = None

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
    prompt = f"""
    You are a Python GIS Developer.
    
    USER REQUEST: "{user_input}"
    
    RULES:
    1. Write a script to accomplish the task using 'arcgis'.
    2. Connection: Use 'gis = GIS()' ONLY. Do NOT add username/password.
    3. Searching: Use 'gis.content.search(query, max_items=5)'.
    4. Printing: Print the 'title' and 'id' of results.
    5. OUTPUT: Return ONLY the code inside ```python ``` blocks.
    """
    
    response = llm.invoke(prompt)
    # Run the self-healing cleaner
    clean_code = clean_generated_code(response.content)
    return clean_code, execute_arcgis_code(clean_code)

# --- 4. LAYOUT ---
with st.sidebar:
    st.markdown("### ⚡ ArcGIS Copilot")
    st.markdown("---")
    st.caption("SYSTEM STATUS")
    st.markdown("🟢 **Model:** Llama 3 (Local)")
    st.markdown("🟢 **API:** ArcGIS Online (Active)")
    st.markdown("---")
    if st.button("🗑️ Reset"):
        st.session_state.messages = []
        st.session_state.last_result = None
        st.session_state.last_code = None
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
                code, output = generate_and_run(prompt)
                st.session_state.last_code = code
                st.session_state.last_result = output
                st.write("Executed. See Workspace.")
                st.session_state.messages.append({"role": "assistant", "content": "Executed. See Workspace."})
                st.rerun()

# RIGHT: Workspace
with col2:
    st.markdown("### 🛠️ Workspace")
    
    if st.session_state.last_code:
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