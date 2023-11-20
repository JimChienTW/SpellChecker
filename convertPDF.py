import PyPDF2

def extract_text_from_pdf(pdf_path):
    text = ''
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
    return text

def save_text_to_txt(text, output_path):
    with open(output_path, 'w', encoding='utf-8') as txt_file:
        txt_file.write(text)

# Example usage
pdf_path = 'reference.pdf'
output_txt_path = 'output.txt'

text = extract_text_from_pdf(pdf_path)
save_text_to_txt(text, output_txt_path)
print(f"Text has been saved to {output_txt_path}")