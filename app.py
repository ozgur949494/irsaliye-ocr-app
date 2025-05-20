from flask import Flask, render_template, request, send_file
from PIL import Image
import pytesseract
import pandas as pd
import io
import re
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['irsaliye']
    image = Image.open(file.stream)

    raw_text = pytesseract.image_to_string(image, lang='tur')

    lines = raw_text.split('\n')
    data = []

    # Basit örnek ayrıştırma: satırda sayı varsa ürün varsayalım
    for line in lines:
        if re.search(r'\d', line):
            row = {
                "Tarih": "", "Ürün Kodu": "", "Ürün Adı": "", 
                "Miktar": "", "Birim": "", "Fiyat": "", "Tutar": ""
            }
            parts = line.split()
            if len(parts) >= 4:
                row["Ürün Kodu"] = parts[0]
                row["Ürün Adı"] = " ".join(parts[1:-3])
                row["Miktar"] = parts[-3]
                row["Fiyat"] = parts[-2]
                row["Tutar"] = parts[-1]
            data.append(row)

    df = pd.DataFrame(data)
    output = io.BytesIO()
    df.to_excel(output, index=False)
    output.seek(0)

    return send_file(output, download_name="irsaliye.xlsx", as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
