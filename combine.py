from flask import Flask, render_template, request, redirect, url_for, send_file
import re   
from pdf2image import convert_from_path
import pytesseract
from PIL import Image
from docx import Document
from io import BytesIO
import os
import requests  # Import requests library
import pathlib
import textwrap
from markdown import markdown

import google.generativeai as genai

from IPython.display import display
from IPython.display import Markdown

GOOGLE_API_KEY="AIzaSyB76f7ijMcDZ5irvffpwjIUX3qB0ZYo3Q8"
genai.configure(api_key=GOOGLE_API_KEY)


for m in genai.list_models():
  if 'generateContent' in m.supported_generation_methods:
    print(m.name)



def extract_websites(text):
 
  urls = re.findall(r"(?:https?://)?(?:www\.)?[\da-z\.-]+\.[a-z]{2,6}", text, re.IGNORECASE)
  return urls

app = Flask(__name__)

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)

    if file:
        file_path = os.path.join('uploads', file.filename)
        file.save(file_path)

        text_pages = process_file(file_path)

        return render_template('index.html', text_pages=text_pages)

def process_file(file_path):
    text_pages = []

    if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
        text = process_image(file_path)
        text_pages.append(text)
    elif file_path.lower().endswith(('.pdf')):
        text_pages = process_pdf(file_path)
    else:
        text_pages.append("Unsupported file format")

    return text_pages

def process_image(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text

def process_pdf(pdf_path):
    text_pages = []
    images = convert_from_path(pdf_path)

    for i, image in enumerate(images):
        text = pytesseract.image_to_string(image)
        text_pages.append(f"Page {i + 1}:\n{text}")

    return text_pages

@app.route('/download', methods=['POST'])
def download_text():
    text_data = request.form['text_data']
    file_format = request.form['format']

    if file_format == 'text':
        # Download as Text file
        response = send_file(BytesIO(text_data.encode()), as_attachment=True, download_name='extracted_text.txt', mimetype='text/plain')
    elif file_format == 'word':
        # Download as Word file
        document = Document()
        document.add_paragraph(text_data)
        docx_output = BytesIO()
        document.save(docx_output)
        docx_output.seek(0)
        response = send_file(docx_output, as_attachment=True, download_name='extracted_text.docx', mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    else:
        response = "Unsupported format"

    return response

@app.route('/search', methods=['POST'])
def search():
    if request.method == 'POST':
        search_text = request.form['search_text']
        search_engine = request.form['search_engine']

        if search_engine == 'google':
            search_url = f"https://www.google.com/search?q={search_text}"
        elif search_engine == 'duckduckgo':
            search_url = f"https://duckduckgo.com/?q={search_text}"
        elif search_engine == 'brave':
            search_url = f"https://search.brave.com/search?q={search_text}"

        return redirect(search_url)

@app.route('/gem', methods=['POST'])
def notofy():
  for m in genai.list_models():
      if 'generateContent' in m.supported_generation_methods:
        print(m.name)
  if request.method == "POST":
        para = request.form['para']
        if not para:
            error = "Please enter some para for Gemini to process."
            return render_template("gen.html", error=error)
  model = genai.GenerativeModel('gemini-pro')
  response = model.generate_content(para)
  result = (response.text)
  result = markdown(result)

  return render_template('index.html', result=result)


@app.route('/exweb', methods=[ 'POST'])
def extract_and_show():
  if request.method == 'POST':
    text = request.form['text']
    websites = extract_websites(text)
    return render_template('index.html', websites=websites)

# if __name__ == '__main__':
#     if not os.path.exists('uploads'):
#         os.makedirs('uploads')
#     app.run(debug=True)
