import gradio as gr
from pypdf import PdfReader
from transformers import pipeline
import chromadb
import os

# --- SETUP: Load Model on Startup ---
print("⏳ Loading AI Brain...")
generator = pipeline(
    "text2text-generation",
    model="MBZUAI/LaMini-T5-738M", 
    max_length=512
)
print("✅ Model Loaded!")

# --- PROCESSING FUNCTIONS ---
def process_file(file_obj):
    if file_obj is None:
        return "⚠️ Please upload a file first!", None
    
    try:
        reader = PdfReader(file_obj.name)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
            
        clean_text = text.replace('\n', ' ').replace('  ', ' ')
        words = clean_text.split(' ')
        chunk_size = 60
        overlap = 10
        
        documents = []
        for i in range(0, len(words), chunk_size - overlap):
            chunk = " ".join(words[i : i + chunk_size])
            if len(chunk) > 20:
                documents.append(chunk)
                
        chroma_client = chromadb.Client()
        collection_name = "doc_" + str(hash(file_obj.name))
        collection = chroma_client.create_collection(name=collection_name)
        
        ids = [str(i) for i in range(len(documents))]
        collection.add(documents=documents, ids=ids)
        
        return f"✅ Ready! Loaded {len(documents)} chunks.", collection
        
    except Exception as e:
        return f"❌ Error: {str(e)}", None

def chat_logic(message, history, collection_state):
    if collection_state is None:
        return "⚠️ Please upload a PDF first!"
        
    results = collection_state.query(query_texts=[message], n_results=2)
    
    if not results['documents'][0]:
        return "I couldn't find an answer in the document."

    context = " ".join(results['documents'][0])
    
    prompt = f"Answer the question based strictly on the context below.\nContext: {context}\nQuestion: {message}\nAnswer:"
    
    response = generator(prompt, max_length=200, do_sample=False)[0]['generated_text']
    return response

# --- BUILD UI ---
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 📄 Chat with Your Data (RAG)")
    db_state = gr.State(None)
    with gr.Row():
        with gr.Column(scale=1):
            file_input = gr.File(label="Upload PDF", file_types=[".pdf"])
            upload_btn = gr.Button("Process PDF", variant="primary")
            status_box = gr.Textbox(label="Status", interactive=False)
            upload_btn.click(fn=process_file, inputs=file_input, outputs=[status_box, db_state])
        with gr.Column(scale=2):
            chatbot = gr.ChatInterface(fn=chat_logic, additional_inputs=[db_state], title="AI Assistant")

demo.launch()
