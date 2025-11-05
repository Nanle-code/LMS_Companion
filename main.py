import os
from dotenv import load_dotenv
from openai import OpenAI
from typing import Optional, Iterable
import gradio as gr
import json
import shutil

load_dotenv(override=True)
# openai_api_key = os.getenv("OPENAI_API_KEY")

app_details = {
    "app_name": "FLASHMIND",
    "app_version": "0.1.1",
    "app_description": "An AI-powered educational tool to help students learn complex subjects through multimedia content.",
    "app_author": "Kiel",
}

media_dic = {
    "title": "Understanding the Ovaries: Functions and Importance",
    "video": "https://www.youtube.com/embed/NHECopO6L3g?si=tGshdLoXMUn71xTQ",
    "video_download": "ana.mp4",
    "pdf": "ana.pdf"
}



openai_api_key = os.getenv('OPENAI_API_KEY')
if openai_api_key:
    print(f"OpenAI API Key exists and begins {openai_api_key[:8]}")
else:
    print("OpenAI API Key not set")
    
MODEL = "gpt-4.1-mini"
openai = OpenAI()

summarize_system_prompt = """You are an academic summarizer. 
Read the teacher’s transcribed text carefully and produce a clear, concise, 
and well-structured summary. Focus on the main ideas, learning objectives, 
and key explanations. Remove filler words, repetitions, and irrelevant dialogue.
The summary should sound educational, easy to understand, 
and suitable for student notes, if you dont know the 
answer please say so."""

user_explain_system_prompt = """You are a helpful educational assistant, 
that explains any concept clearly and simply based on the user’s specific 
challenge, confusion, or question. Always ensure the explanation is easy to 
understand, uses examples, and connects directly to the user’s difficulty.
Identify what part of the concept the user finds difficult or confusing,
Explain it step-by-step using clear, everyday language, providing external resource link that open in another web tab if clicked 
Give practical examples, analogies, or comparisons to make it relatable"""

list_points_system_prompt = """You are an expert at converting text into
a list of key points. Read the provided text carefully and extract the main
ideas, concepts, or steps. Present these in a clear, concise list format.
Ensure each point is distinct and captures the essence of the original text.
Avoid unnecessary details or filler information. The list should be easy to
read and understand, suitable for quick reference or study purposes.
Respond only with the list of key points.
"""

question_answer_system_prompt = """ Create a question and answer pair based on the provided text.
The question should test understanding of a key concept from the text.
The answer should be clear, concise, and directly address the question.
let your response be in the following JSON format:
{
"links": [
        {"question": "what is this about?", "answer": "answer to the question"},
        {"question": "another question", "answer": "an answer"}
    ]
}


"""

flash_card_point_system_prompt = """ """

def summarize_transcript(transcript):
    messages = [
        {"role": "system", "content": summarize_system_prompt},
        {"role": "user", "content": transcript}
    ]
    
    response = openai.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.2,
        max_tokens=500,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    
    summary = response.choices[0].message.content
    return summary

def question_answer_pair(text):
    messages = [
        {"role": "system", "content": question_answer_system_prompt},
        {"role": "user", "content": text}
    ]
    
    response = openai.chat.completions.create(
        model=MODEL,
        messages=messages,
        
        response_format={"type": "json_object"}
    )
    
    result = response.choices[0].message.content
    links = json.loads(result) 
    return links     

def user_explain_concept(concept, user_question):
    messages = [
        {"role": "system", "content": user_explain_system_prompt},
        {"role": "user", "content": f"Concept: {concept}\nUser Question: {user_question}"}
    ]
    
    response = openai.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.3,
        max_tokens=500,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    
    explanation = response.choices[0].message.content
    return explanation


def list_key_points(text):
    messages = [
        {"role": "system", "content": list_points_system_prompt},
        {"role": "user", "content": text}
    ]
    
    response = openai.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.2,
        # max_tokens=300,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    
    return response.choices[0].message.content

def web_search(query):
    response = openai.responses.create(
    model="gpt-5",
    tools=[{"type": "web_search"}],
    input="What was a positive news story from today?")

    return response.output_text



def _try_import(name: str):
    try:
        return __import__(name)
    except Exception as e:
        raise ImportError(f"Missing dependency '{name}': {e}")

PyPDF2 = _try_import("PyPDF2")

def transcribe_pdf_to_text(
    pdf_path: str,
    ocr: bool = False,
    pages: Optional[Iterable[int]] = None,
    dpi: int = 300,
    write_to: Optional[str] = None,
) -> str:
    """
    Extract text from a PDF file. Uses direct PDF text extraction first.
    If ocr=True or no text found, falls back to OCR (pytesseract + pdf2image).

    Args:
      pdf_path: path to the PDF file
      ocr: force OCR fallback or allow OCR when no text found
      pages: iterable of 0-based page indices to process (default: all)
      dpi: resolution for OCR page images
      write_to: optional path to write the resulting text

    Returns:
      The extracted text as a single string.
    """
    if not os.path.isfile(pdf_path):
        raise FileNotFoundError(pdf_path)

    reader = PyPDF2.PdfReader(pdf_path)
    if getattr(reader, "is_encrypted", False):
        try:
            reader.decrypt("")  # try empty password
        except Exception:
            raise RuntimeError("PDF is encrypted and cannot be decrypted automatically.")

    # Normalize pages selection
    total = len(reader.pages)
    if pages is None:
        page_indices = range(total)
    else:
        page_indices = [p for p in pages if 0 <= p < total]

    # 1) Try direct text extraction
    text_parts = []
    for i in page_indices:
        try:
            page = reader.pages[i]
            txt = page.extract_text() or ""
        except Exception:
            txt = ""
        text_parts.append(txt)

    full_text = "\n\n".join(part for part in text_parts if part and part.strip())

    # 2) If no text found and OCR allowed, do OCR
    if (not full_text.strip()) and ocr:
        pdf2image = _try_import("pdf2image")
        pytesseract = _try_import("pytesseract")
        from PIL import Image  # pillow

        # convert selected pages to images
        # pdf2image.convert_from_path accepts first_page/last_page (1-based)
        # We'll convert the minimal page range if pages is continuous, otherwise convert all and index.
        images = pdf2image.convert_from_path(pdf_path, dpi=dpi)
        ocr_texts = []
        for i in page_indices:
            img = images[i]
            ocr_texts.append(pytesseract.image_to_string(img))
        full_text = "\n\n".join(ocr_texts)

    if write_to:
        with open(write_to, "w", encoding="utf-8") as f:
            f.write(full_text)

    return full_text

pdf_text = transcribe_pdf_to_text(media_dic.get("pdf",""))


def save_pdf(file):
    if file is None:
        return "No file uploaded."
    # Define root directory (current working directory)
    root_dir = os.getcwd()
    save_path = os.path.join(root_dir, file.name)
    
    # Save uploaded file
    shutil.copy(file.name, save_path)
    return f"✅ File saved successfully to: {save_path}"


def upload_pdf(file):
    if file is None:
        return "No file uploaded", None
    
    # Save file to root directory
    save_path = os.path.join(os.getcwd(), file.name)
    file.save(save_path)
    
    # Return confirmation and embed the PDF in an iframe
    pdf_view = f'<iframe src="file/{file.name}" width="100%" height="600px"></iframe>'
    return f"✅ PDF '{file.name}' uploaded successfully!", pdf_view


flashcards = [
    {"question": "What is the capital of France?", "answer": "Paris"},
    
]

# HTML template with CSS animation
def get_flashcard_html(index=0):
    card = flashcards[index % len(flashcards)]
    html = f"""
    <style>
    .flashcard-container {{
        perspective: 1000px;
        width: 400px;
        height: 300px;
        margin: auto;
        cursor: pointer;
    }}
    .flashcard {{
        position: relative;
        width: 100%;
        height: 100%;
        text-align: center;
        transition: transform 0.8s;
        transform-style: preserve-3d;
    }}
    .flashcard.is-flipped {{
        transform: rotateY(180deg);
    }}
    .flashcard-face {{
        position: absolute;
        width: 100%;
        height: 100%;
        backface-visibility: hidden;
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 1.3em;
        border-radius: 12px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        background: #000ff;
    }}
    .flashcard-front {{
        background-color: #585D59FF;
    }}
    .flashcard-back {{
        background-color: #4caf50;
        color: white;
        transform: rotateY(180deg);
    }}
    </style>

    <div class="flashcard-container" onclick="this.querySelector('.flashcard').classList.toggle('is-flipped')">
      <div class="flashcard">
        <div class="flashcard-face flashcard-front">{card['question']}</div>
        <div class="flashcard-face flashcard-back">{card['answer']}</div>
      </div>
    </div>
    """
    return html

def next_card(current_index):
    current_index = (current_index + 1) % len(flashcards)
    return get_flashcard_html(current_index), current_index



def web_search():
   progress = gr.Progress(track_tqdm=True)
   response = client.responses.create(
        model="gpt-5",
        tools=[{"type": "web_search"}],
        input=f"Give me video links on the topic {media_dic.get('title','')} while using {pdf_text} as a guide , group these into a study sequence that mirrors theoutline , return as a markdown list"
    )

   return response.output_text



flashcards = question_answer_pair(pdf_text).get("links", [])
# Define function that returns a tuple (3 outputs)
def process_input(user_text):
    
    return (
        user_explain_concept(pdf_text, user_text),
        list_key_points(pdf_text),
        
    )
    
def view_pdf (pdf_url):
     return pdf_url
 
def render_local_pdf():
    if not os.path.exists(media_dic.get("pdf", "")):
        return f"<p style='color:red;'>⚠️ File not found: {media_dic.get('pdf', '')}</p>"

    # Create iframe to display PDF
    return f"<iframe src='file/{media_dic.get('pdf', '')}' width='100%' height='600px'></iframe>"

# Build layout
with gr.Blocks() as demo:
    gr.Markdown(f"## {app_details.get('app_name','Welcome to the Learning App')}")

    # --- Row 1 ---
    with gr.Row():
        with gr.Column():
            gr.Markdown("### 📘 Topic: AI Learning ")
            # show_button = gr.Button("Show PDF")
            pdf_display = gr.HTML()
#             upp = gr.Interface(fn=save_pdf, inputs=gr.File(label="Upload your PDF", file_types=[".pdf"]), outputs="text", title="PDF Uploader", description="Upload a PDF file to save it in the root directory."
# )
#             upp.launch(share=False)
            # show_button.click(render_local_pdf, outputs=pdf_display)
            
            # pdf_input = gr.File(label="Upload your PDF", file_types=[".pdf"])
            # upload_button = gr.Button("Upload & View")
            gr.Label(f"Enter your concerns about this topic")
            status = gr.Markdown()
        
            # pdf_display = gr.HTML(label="PDF Viewer")
            
            # upload_button.click(upload_pdf, inputs=pdf_input, outputs=[status, pdf_display])

            
            
        with gr.Column():
            gr.Label("Deep  Explanation")
            out1 = gr.Markdown(label="A Quick Explanation")

    # --- Row 2 ---
    with gr.Row():
        with gr.Column():
            # Embed a YouTube video using iframe
            gr.HTML(f"""
                <iframe width="500" height="300" 
                src="{media_dic.get('video','')}"
                title="Gradio Tutorial" 
                frameborder="0" allowfullscreen></iframe>
            """)
        with gr.Column():
            gr.Label("Key Points")
            out2 = gr.Markdown(label="Key Points")

    # --- Row 3 ---
    with gr.Row():
        with gr.Column():
            text_input = gr.TextArea(label="Enter your text here")
            submit_btn = gr.Button("Submit")
        with gr.Column():
           
            
            gr.Markdown("### 🧠 Educative Flashcards")
            html_card = gr.HTML(get_flashcard_html(0))
            index_state = gr.State(0)
            next_btn = gr.Button("Next ➡️")
                
            next_btn.click(fn=next_card, inputs=index_state, outputs=[html_card, index_state])
            
    with gr.Row():
         with gr.Column():
              gr.Label(f"Get more web resources for this course {media_dic.get('title','')}")
              btn = gr.Button("Click for More Resources")
         with gr.Column():  
             output = gr.Markdown("")  
                
    btn.click(fn=web_search, outputs=output) 

    # --- Link function ---
    submit_btn.click(fn=process_input, inputs=text_input, outputs=[out1, out2] )

# Launch app
demo.launch(share=True)

