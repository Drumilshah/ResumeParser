import os
from PyPDF2 import PdfFileReader
import textract


# extract text from pdfs and docs for annotation

datasetPath = "/Users/drumilshah/Documents/ResumeParser/dataset"

trainingSetCount = 18
count = 0
trainingSetPdfs = []
for root, dirs, files in os.walk(datasetPath):
  for filename in files:
    count += 1
    trainingSetPdfs.append(filename)
    name, extension = os.path.splitext(filename)
    filePath = os.path.join(datasetPath, filename)
    text = ""
    if(extension == ".pdf"):
      pdfFileObj = open(filePath, "rb")
      pdfReader = PdfFileReader(pdfFileObj)
      pages = pdfReader.numPages
      for page in range(pages):
        pdfObj = pdfReader.getPage(page)
        text += pdfObj.extractText()
      with open(f'./extracted_text/{name}.txt', 'w') as f:
        f.write(text)
    elif(extension == ".doc" or extension == ".docx"):
      text = str(textract.process(filePath))
      with open(f'./extracted_text/{name}.txt', 'w') as f:
          f.write(text)
    if(count > trainingSetCount):
      break