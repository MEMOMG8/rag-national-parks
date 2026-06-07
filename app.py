import gradio as gr
from query import ask

def handle_query(question):
    if not question.strip():
        return "Please enter a question.", ""
    result = ask(question)
    sources = "\n".join(f"• {s}" for s in result["sources"])
    return result["answer"], sources

with gr.Blocks(title="National Parks Assistant") as demo:
    gr.Markdown("# 🏔️ National Parks Assistant")
    gr.Markdown("Ask questions about Yellowstone, Grand Canyon, Yosemite, Zion, or Great Smoky Mountains.")
    
    inp = gr.Textbox(label="Your Question", placeholder="e.g. What wildlife can I see at Yellowstone?")
    btn = gr.Button("Ask", variant="primary")
    answer = gr.Textbox(label="Answer", lines=8)
    sources = gr.Textbox(label="Retrieved From", lines=3)
    
    btn.click(handle_query, inputs=inp, outputs=[answer, sources])
    inp.submit(handle_query, inputs=inp, outputs=[answer, sources])

demo.launch()