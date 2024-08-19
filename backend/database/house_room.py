import os
import re
from openai import OpenAI
import PyPDF2

# Initialize the OpenAI client using the API key from the environment variable
client = OpenAI(api_key="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")

# Function to read the PDF content
def extract_text_from_pdf(pdf_path):
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text

# Function to extract image links from the text
def extract_image_links(pdf_text):
    # Improved regex pattern to match complex URLs
    url_pattern = r'https?://[^\s"]+'
    links = re.findall(url_pattern, pdf_text)
    
    # Return the unique links found in the document
    return list(set(links))

# Function to analyze the document using OpenAI
def analyze_document(pdf_text):
    # Define the prompt based on the refined instructions
    prompt = f"""
    You are a highly capable assistant tasked with extracting detailed room information from an inventory report. Your objectives are:

    1. Identify and list each room by name.
    2. Extract the contents within each room such as furniture, fixtures, appliances, and other items.
    3. Add a "defects" field to each room, but only include significant defects or damages. Ignore minor issues that do not warrant attention. Defects should be based on both the text descriptions and a thorough analysis of the images related to each room. If no significant defects are found, explicitly state "No significant defects identified."
    
    Return in json format for each room with room name and item name and defects.
    The document content is as follows:
    {pdf_text}
    """

    # Non-streaming request
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )

    # Extract and return the JSON from the response
    return completion.choices[0].message.content.strip()

# Path to the PDF document
pdf_path = "/content/inventory.pdf"

# Extract text from the PDF
pdf_text = extract_text_from_pdf(pdf_path)


# Analyze the document and get the JSON output
json_output = analyze_document(pdf_text)

# Print the JSON output
print(json_output)
