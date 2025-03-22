# app.py
from flask import Flask, render_template, request, send_file
import os
import pdfkit

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'static/downloads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure downloads folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get form data
        data = {
            'name': request.form.get('name'),
            'email': request.form.get('email'),
            'phone': request.form.get('phone'),
            'address': request.form.get('address'),
            'linkedin': request.form.get('linkedin', ''),
            'objective': request.form.get('objective'),
            'experience': request.form.get('experience'),
            'education': request.form.get('education'),
            'skills': request.form.get('skills').split('\n'),
            'certifications': request.form.get('certifications', '').split('\n'),
            'projects': request.form.get('projects', ''),
            'references': request.form.get('references', ''),
            'template': request.form.get('template'),
            'color': request.form.get('color')
        }
        return render_template('preview.html', data=data)
    return render_template('index.html')

@app.route('/download/<format>', methods=['POST'])
def download(format):
    data = request.form.to_dict()
    html_content = render_template('preview.html', data=data, download=True)
    filename = f"resume_{data['name'].replace(' ', '_')}"

    if format == 'pdf':
        pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{filename}.pdf")
        pdfkit.from_string(html_content, pdf_path)
        return send_file(pdf_path, as_attachment=True)
    
    elif format == 'txt':
        txt_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{filename}.txt")
        with open(txt_path, 'w') as f:
            f.write(f"{data['name']}\n{data['email']} | {data['phone']}\n{data['address']}\n")
            if data['linkedin']: f.write(f"LinkedIn: {data['linkedin']}\n")
            f.write("\nObjective\n")
            f.write(f"{data['objective']}\n\n")
            f.write("Work Experience\n")
            f.write(f"{data['experience']}\n\n")
            f.write("Education\n")
            f.write(f"{data['education']}\n\n")
            f.write("Skills\n")
            for skill in data['skills']: f.write(f"- {skill}\n")
            if data['certifications'][0]:
                f.write("\nCertifications\n")
                for cert in data['certifications']: f.write(f"- {cert}\n")
            if data['projects']:
                f.write("\nProjects\n")
                f.write(f"{data['projects']}\n")
            if data['references']:
                f.write("\nReferences\n")
                f.write(f"{data['references']}\n")
        return send_file(txt_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)