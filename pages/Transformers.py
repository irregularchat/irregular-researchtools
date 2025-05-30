import streamlit as st
from components.sidebar_menu import sidebar_menu
import importlib

def transformers_page():
    # Add custom CSS for wider container and better styling
    st.markdown("""
    <style>
    /* Base styles for both light and dark mode */
    .block-container {
        max-width: 95% !important;
        padding: 1rem;
    }
    
    /* Tool card styling */
    .transformer-card {
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 15px;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    /* Form elements styling */
    .stTextInput > div > div > input, 
    .stSelectbox > div > div > div,
    .stTextArea > div > div > textarea {
        border-radius: 8px;
    }
    
    /* Light mode specific styles */
    @media (prefers-color-scheme: light) {
        .transformer-card {
            background-color: white;
            color: #262730;
            border: 1px solid #e6e6e6;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        .transformer-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.15);
        }
        
        h3, h4 {
            color: #0068c9 !important;
        }
        
        .stExpander {
            border: 1px solid #e6e6e6;
            border-radius: 8px;
        }
    }
    
    /* Dark mode specific styles */
    @media (prefers-color-scheme: dark) {
        .transformer-card {
            background-color: #1e1e1e;
            color: #fafafa;
            border: 1px solid #333;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        }
        
        .transformer-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.4);
        }
        
        h3, h4 {
            color: #4da6ff !important;
        }
        
        .stExpander {
            border: 1px solid #444;
            border-radius: 8px;
        }
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.title("Data Transformation Tools")
    
    # Add the sidebar menu
    sidebar_menu()
    
    # Get the tool from query parameters
    query_params = st.query_params
    tool = query_params.get("tool", None)
    
    # Display tool selection if none specified
    if not tool:
        st.write("Select a transformation tool from the options below:")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Data Conversion")
            if st.button("CSV/JSON Converter", use_container_width=True):
                st.query_params["tool"] = "converter"
            if st.button("URL Processor", use_container_width=True):
                st.query_params["tool"] = "url_processor"
        
        with col2:
            st.subheader("Advanced Tools")
            if st.button("Advanced Query Generator", use_container_width=True):
                st.query_params["tool"] = "query_generator"
            if st.button("Image Hash Generator", use_container_width=True):
                st.query_params["tool"] = "image_hash"
        
        return
    
    # Map tool parameters to their respective modules and functions
    tool_map = {
        "converter": {"module": "utilities.conversions", "function": "converter_page"},
        "query_generator": {"module": "utilities.search_generator", "function": "query_generator_page"},
        "image_hash": {"module": "utilities.ImageSearch", "function": "image_hash_page"},
        "url_processor": {"module": "utilities.url_processing", "function": "url_processor_page"}
    }
    
    # Render the selected tool
    if tool in tool_map:
        tool_info = tool_map[tool]
        module_name = tool_info["module"]
        function_name = tool_info["function"]
        
        try:
            # Try to import the module
            module = importlib.import_module(module_name)
            
            # Check if the function exists in the module
            if hasattr(module, function_name):
                function = getattr(module, function_name)
                function()  # Call the function
            else:
                st.error(f"Function '{function_name}' not found in module '{module_name}'")
                
                # Create a placeholder UI for the tool
                st.header(tool.replace("_", " ").title())
                st.warning(f"This tool is not fully implemented yet. Please check back later.")
                
                # Show what functions are available in the module
                st.write(f"Available functions in {module_name}:")
                for name in dir(module):
                    if callable(getattr(module, name)) and not name.startswith("_"):
                        st.write(f"- {name}")
        except ImportError:
            # If the module doesn't exist, create a placeholder UI
            st.header(tool.replace("_", " ").title())
            st.error(f"Module '{module_name}' not found.")
            st.warning("This tool is not implemented yet. Please check back later.")
        except Exception as e:
            st.error(f"Error rendering tool '{tool}': {e}")
    else:
        st.error(f"Unknown tool: {tool}")
        st.write("Please select a valid tool from the options below:")
        for key in tool_map.keys():
            st.write(f"- [{key.replace('_', ' ').title()}](/Transformers?tool={key})")

def main():
    transformers_page()

if __name__ == "__main__":
    main() 