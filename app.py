"""
Streamlit application for Python Code Explainer.
"""
import streamlit as st
from code_explainer import extract_elements, generate_explanation, create_document

def main():
    """Main application function."""
    st.set_page_config(
        page_title="Python Code Explainer",
        page_icon="🤖",
        layout="wide"
    )
    
    st.title("Python Code Explainer")
    st.caption("Upload a Python file to analyze its structure and get explanations")
    
    # Sidebar for settings
    with st.sidebar:
        st.header("Settings")
        model_name = st.selectbox(
            "LLM Model",
            ["llama2", "llama3", "mistral"],
            index=0,
            help="Select the language model to use for generating explanations"
        )
    
    # File uploader
    uploaded_file = st.file_uploader("Upload Python (.py) file", type="py")
    
    if uploaded_file:
        try:
            # Read and analyze the code
            code = uploaded_file.read().decode()
            code_elements = extract_elements(code)
            
            # Display code analysis
            st.header("Code Analysis")
            for el in code_elements:
                with st.expander(f"{el['type']}: {el['name']} (Lines {el['start_line']}-{el['end_line']})"):
                    st.caption(f"Location: Lines {el['start_line']}-{el['end_line']}")
                    
                    if el['args']:
                        st.write(f"**Arguments:** `{', '.join(el['args'])}`")
                    if el['type'] != 'Class' and el['has_return']:
                        st.write("**Returns:** Yes")
                        
                    if el['docstring']:
                        st.subheader("Documentation")
                        st.text(el['docstring'])
                    
                    st.subheader("Source Code")
                    st.code(el['source'], language='python')
            
            # Generate explanation
            if st.button("Generate Explanation", type="primary"):
                with st.spinner("Analyzing code with AI..."):
                    try:
                        explanation = generate_explanation(code_elements, model=model_name)
                        st.success("AI Explanation:")
                        st.write(explanation)
                        
                        # Generate and offer download of DOCX report
                        doc_buffer = create_document(code_elements, explanation)
                        if doc_buffer:
                            st.download_button(
                                label="📥 Download Analysis Report",
                                data=doc_buffer,
                                file_name="code_analysis_report.docx",
                                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                            )
                        
                    except Exception as e:
                        st.error(f"Error generating explanation: {str(e)}")
            
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")

if __name__ == "__main__":
    main()
