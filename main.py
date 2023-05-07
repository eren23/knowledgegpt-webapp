import os 
from local_config import SECRET_KEY # or from config import SECRET_KEY
import streamlit as st 
import openai

openai.api_key = SECRET_KEY

st.title('KnowledgeGPT Document Q&A App')
st.header('A Basic User Interface For KnowledgeGPT')

save_dir = st.text_input('Enter The Directory You Want To Save The File To ( FOR NOW PLEASE REENTER EACH TIME YOU ASK A QUESTION :())')
if save_dir:
    st.session_state['save_dir'] = save_dir

if 'is_ran' not in st.session_state:
    st.session_state['is_ran'] = False

current_dir = os.getcwd()
allowed_extensions = [".ppt", ".pptx", ".pdf", ".doc", ".docx"]
files = [f for f in os.listdir(current_dir) if os.path.splitext(f)[1].lower() in allowed_extensions]

selected_file = st.selectbox("Select a file", files)
st.write("You selected a PDF file:", selected_file)

# App framework
st.title('KnowledgeGPT Document Q&A App')
prompt = st.text_input('Plug in your prompt here') 

file_type = ''


if selected_file:
    if 'save_dir' in st.session_state:  
        save_dir = st.session_state['save_dir']

    indexes_path = os.path.join('indexes', save_dir)
    
    if ".pdf" in selected_file.lower():
        
        file_type = 'pdf'
        from knowledgegpt.extractors.pdf_extractor import PDFExtractor
        pdf_extractor = PDFExtractor(index_path=indexes_path, pdf_file_path=selected_file, extraction_type="paragraph", embedding_extractor="hf", model_lang="en")
        
        
    elif any(substring in selected_file.lower() for substring in [".ppt", ".pptx"]):
        
        file_type = 'ppt'
        ppt_extractor = PowerpointExtractor(index_path=indexes_path, file_path=selected_file, extraction_type="paragraph", embedding_extractor="hf", model_lang="en")
        from knowledgegpt.extractors.powerpoint_extractor import PowerpointExtractor
        st.write("You selected a PPT file:", selected_file)
        
    elif any(substring in selected_file.lower() for substring in [".doc", ".docx"]):
        file_type = 'doc'
        doc_extractor = DocsExtractor(index_path=indexes_path, file_path=selected_file, extraction_type="paragraph", embedding_extractor="hf", model_lang="en")
        from knowledgegpt.extractors.docs_extractor import DocsExtractor

        # Do something with the selected DOC file
        
    else:
        # Invalid file type
        st.write("Invalid file type:", selected_file)
        
        
if prompt:
    st.session_state['is_ran'] = True
    if file_type == 'pdf' :
        
        answer, prompt, messages = pdf_extractor.extract(prompt, max_tokens=1500)
        st.write("Answer:", answer)
    elif file_type == 'ppt':
        answer, prompt, messages = ppt_extractor.extract(prompt, max_tokens=1500)
        st.write("Answer:", answer)
        
    elif file_type == 'doc':
        answer, prompt, messages = doc_extractor.extract(prompt, max_tokens=1500)
        st.write("Answer:", answer)
    
    else:
        st.write("Invalid file type:", selected_file)
    
if st.button('Enable File Selection'):
    st.session_state['is_ran'] = False
    