import gradio as gr

# Sample flashcards 
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
        width: 300px;
        height: 200px;
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

with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### 🧠 Animated Flashcards")
            html_card = gr.HTML(get_flashcard_html(0))
            index_state = gr.State(0)
            next_btn = gr.Button("Next ➡️")
        

    next_btn.click(fn=next_card, inputs=index_state, outputs=[html_card, index_state])

demo.launch()



import gradio as gr

# Sample flashcards
flashcards = [
    {"question": "What is the capital of France?", "answer": "Paris"},
    {"question": "Who developed Python?", "answer": "Guido van Rossum"},
    {"question": "What is 5 + 7?", "answer": "12"},
    {"question": "What year did AI boom begin?", "answer": "Around 2012"},
]

# HTML template with CSS animation
def get_flashcard_html(index=0):
    card = flashcards[index % len(flashcards)]
    html = f"""
    <style>
    .flashcard-container {{
        perspective: 1000px;
        width: 300px;
        height: 200px;
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

with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### 🧠 Animated Flashcards")
            html_card = gr.HTML(get_flashcard_html(0))
            index_state = gr.State(0)
            next_btn = gr.Button("Next ➡️")
        

    next_btn.click(fn=next_card, inputs=index_state, outputs=[html_card, index_state])

demo.launch()

