import requests
from bs4 import BeautifulSoup 
import Config.config as config
from urllib.parse import urljoin
import time
from DB.db import add_data
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import PyPDF2

mainurl = ""

# Collect the data of the web {Heading & Articles}
def webscrap(url):
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch {url}: {e}")
        return

    soup = BeautifulSoup(r.content, 'html.parser')

    paragraphs = soup.find_all(['p', 'div', 'article'])
    combined_text = ""
    for para in paragraphs:
        text = para.get_text(strip=True)
        if text and not text.isspace() and len(text) > 20:
            combined_text += text + " "
    print("url:",url)
    save_text_to_pdf(combined_text, "output.pdf") #This will save the scraped text to a pdf.
    # add_data(combined_text, url)

# Collect the links from the website
def get_links(url):
    global mainurl  # Declare mainurl as global to modify it
    mainurl = url  # Assign the global variable to the local variable
    try:
        # Ensure the URL is correctly formatted
        if not url.startswith('http://') and not url.startswith('https://'):
            url = 'https://' + url
        r = requests.get(url, timeout=10)
        print("Fetching links from: ", r.url)
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch {url}: {e}")
        return

    soup = BeautifulSoup(r.content, 'html.parser')
    for link in soup.find_all('a', href=True):
        full_link = urljoin(url, link['href'])
        if checklink(full_link):
            webscrap(full_link)
            time.sleep(1)  # Add a delay to avoid overwhelming the server
        else:
            continue

# Check we don't go from outside the domain
def checklink(url):
    if url.startswith(f'https://{mainurl}') or url.startswith(f'http://{mainurl}'):
        return True
    else:
        return False

def embedding_functions(text):
    
    pass



def save_text_to_pdf(text, filename="output.pdf"):
    """
    Saves the given text to a PDF file.

    Args:
        text (str): The text to be saved.
        filename (str): The name of the PDF file to create.
    """
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    # Set initial text position and font
    x, y = 50, height - 50
    c.setFont("Helvetica", 12)

    # Split text into lines to fit within the page width
    lines = text.splitlines()
    for line in lines:
        c.drawString(x, y, line)
        y -= 15  # Adjust line spacing

        # Start a new page if the text reaches the bottom
        if y < 50:
            c.showPage()
            y = height - 50  # Reset y position

    c.save()

# # Example usage:
# my_text = """
# This is some example text that will be saved to a PDF file.
# It can include multiple lines and even very long lines.
# You can save any text you like.
# This demonstrates how to create a simple PDF using ReportLab.
# """



# # Example usage with file read.
# def save_file_to_pdf(input_file, output_file="output.pdf"):
#     """
#     Saves the content of a text file to a PDF.

#     Args:
#         input_file (str): The path to the input text file.
#         output_file (str): The path to the output PDF file.
#     """
#     try:
#         with open(input_file, 'r', encoding='utf-8') as f:
#             text = f.read()
#         save_text_to_pdf(text, output_file)
#     except FileNotFoundError:
#         print(f"Error: Input file '{input_file}' not found.")
#     except Exception as e:
#         print(f"An error occurred: {e}")

# save_file_to_pdf("my_text_file.txt", "my_text_to_pdf.pdf") #example of saving a file to pdf.


def extract_text_from_pdf(pdf_content):
    """
    Extracts text from the provided PDF content.

    Args:
        pdf_content (str): The raw content of the PDF file.

    Returns:
        str: The extracted text, or None if an error occurs.
    """
    try:
        # Create a temporary PDF file to process the string.
        with open("temp.pdf", "wb") as f:
            f.write(pdf_content.encode('latin-1')) #write the string to the temp file.

        with open("temp.pdf", "rb") as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text() or "" #If no text, don't return none, return an empty string.

        return text.strip()  # Remove leading/trailing whitespace

    except Exception as e:
        print(f"Error extracting text: {e}")
        return None