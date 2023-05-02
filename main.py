import io
import os
import sys
import re
import subprocess
from datetime import date

try:
    from pdfminer.converter import TextConverter
    from pdfminer.layout import LAParams
    from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
    from pdfminer.pdfpage import PDFPage
    print("pdfminer.six is already installed.")
except ImportError:
    print("Installing pdfminer.six...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pdfminer.six"])

    from pdfminer.converter import TextConverter
    from pdfminer.layout import LAParams
    from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
    from pdfminer.pdfpage import PDFPage

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

class PDFTextExtractor:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.text = ""

    def extract_text_from_pdf(self):
        with open(self.pdf_path, 'rb') as file:
            resource_manager = PDFResourceManager(caching=False)
            fake_file_handle = io.StringIO()
            converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
            page_interpreter = PDFPageInterpreter(resource_manager, converter)

            for page in PDFPage.get_pages(file, check_extractable=True):
                page_interpreter.process_page(page)

            self.text = fake_file_handle.getvalue()

            # close open handles
            converter.close()
            fake_file_handle.close()

    def split_and_save_text(self, output_folder, max_chars=7499):
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)

            # Replace any character that doesn't match the \w pattern with a space
            cleaned_text = re.sub(r'[^\w\s]', ' ', self.text)

            # Remove lines containing only a number
            cleaned_text = re.sub(r'^\d+$', '', cleaned_text, flags=re.MULTILINE)

            # Remove extra whitespaces
            cleaned_text = ' '.join(cleaned_text.split())
            num_files = len(cleaned_text) // max_chars + 1

            # Get the current date
            current_date = date.today().strftime("%Y-%m-%d")

            for i in range(num_files):
                start = i * max_chars
                end = (i + 1) * max_chars
                chunk = cleaned_text[start:end]

                # Update the output path
                output_path = os.path.join(output_folder, current_date, f"part_{i+1}.txt")

                # Create the directory if it doesn't exist
                os.makedirs(os.path.dirname(output_path), exist_ok=True)

                with open(output_path, "w", encoding='utf-8') as output_file:
                    output_file.write(chunk)


def main():
    try:
        clear_console()
        print("Please enter the path to the PDF file:")
        pdf_path = input()

        if ".pdf" not in pdf_path:
            print("Please enter a valid path to a PDF file.")
        else:
            pdf_path = pdf_path.replace("\"", "")
            if not os.path.exists(pdf_path):
                print("The file does not exist.")
            elif os.path.getsize(pdf_path) == 0:
                print("The file is empty.")
            else:
                extractor = PDFTextExtractor(pdf_path)
                
                extractor.extract_text_from_pdf()
                extractor.split_and_save_text('output_folder')
    except Exception as e:
        print(f"An Error as occured:\n{e}")


if __name__ == "__main__":
    main()
