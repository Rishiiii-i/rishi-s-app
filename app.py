from flask import Flask, render_template, request, session
from pdf_utils import extract_text_from_pdf
from llm_utils import ask_llm

app = Flask(__name__)  # Create the Flask app FIRST
app.secret_key = "AIzaSyDVA_R-xfyL5IkWVgasqJXJEeb_EBjm8MI"  # Set your secret key (do NOT use an API key here!)

pdf_text = ""  # Store extracted text globally for demo purposes

@app.route('/', methods=['GET', 'POST'])
def index():
    global pdf_text
    answer = ""
    pdf_uploaded = False

    # Initialize Q&A history in session if not present
    if 'history' not in session:
        session['history'] = []

    if request.method == 'POST':
        if 'pdf' in request.files and request.files['pdf'].filename != '':
            pdf_file = request.files['pdf']
            pdf_text = extract_text_from_pdf(pdf_file)
            pdf_uploaded = True
        elif 'question' in request.form:
            question = request.form['question']
            if pdf_text:
                answer = ask_llm(question, pdf_text[:3000])  # Limit context for LLM
                # Save Q&A to history
                session['history'].append({"question": question, "answer": answer})
                session.modified = True
            else:
                answer = "Please upload a PDF first."

    return render_template(
        'index.html',
        answer=answer,
        pdf_uploaded=pdf_uploaded,
        history=session.get('history', [])
    )

if __name__ == '__main__':
    app.run(debug=True)
