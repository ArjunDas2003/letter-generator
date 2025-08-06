from flask import Flask, render_template, request, redirect, url_for, send_file
from utils import generate_letter
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import io

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = {
            'from_name': request.form['from_name'],
            'from_designation': request.form['from_designation'],
            'to_name': request.form['to_name'],
            'to_designation': request.form['to_designation'],
            'subject': request.form['subject'],
            'purpose': request.form['purpose'],
            'date': datetime.now().strftime('%d %B, %Y')
        }

        letter = generate_letter(data)
        return render_template('letter.html', data=data, letter=letter)

    return render_template('index.html')

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit

@app.route('/download-pdf', methods=['POST'])
def download_pdf():
    letter_text = request.form['letter']

    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    margin_x = 50
    margin_y = 50
    usable_width = width - 2 * margin_x
    y = height - margin_y

    pdf.setFont("Helvetica", 12)

    # Split the input into paragraphs
    paragraphs = letter_text.strip().split('\n')

    for para in paragraphs:
        if para.strip() == "":
            y -= 20  # Add spacing between paragraphs
            continue

        # Automatically wrap long lines to fit page width
        lines = simpleSplit(para, "Helvetica", 12, usable_width)

        for line in lines:
            if y < margin_y:
                pdf.showPage()
                y = height - margin_y
                pdf.setFont("Helvetica", 12)
            pdf.drawString(margin_x, y, line)
            y -= 18  # Line spacing

        y -= 12  # Paragraph spacing

    pdf.save()
    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name="college_letter.pdf", mimetype='application/pdf')



if __name__ == '__main__':
    app.run(debug=True)
