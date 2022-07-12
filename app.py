from flask import Flask, render_template, request, send_file
from pdf2image import convert_from_path
import os
from inference import inference

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './temp'

@app.route("/")
def home():
    return render_template('home.html')


@app.route("/upload", methods = ["POST"])
def fileUpload():
    uploaded_files = request.files.getlist("file")
    print(uploaded_files)
    if(not os.path.isdir(app.config["UPLOAD_FOLDER"])):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    for file in uploaded_files:
        fileName = file.filename
        fileExt = os.path.splitext(fileName)[1]
        if(fileExt.lower() == '.pdf'):
            filePath = os.path.join(app.config["UPLOAD_FOLDER"], fileName)
            file.save(filePath)
            pages = convert_from_path(os.path.join(app.config["UPLOAD_FOLDER"], fileName))
            counter = 1
            for page in pages:
                page.save(app.config["UPLOAD_FOLDER"] + "/" +str(counter) + '.jpg', 'JPEG')
                counter += 1
            print('pdf converted')
            os.remove(filePath)
    result = inference()
    return render_template('home.html', data = result)

if __name__ == "__main__":
    app.run(debug = True)
