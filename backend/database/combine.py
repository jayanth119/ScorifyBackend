import os
import re
import json
from openai import OpenAI
import PyPDF2
import fitz  # PyMuPDF
from PIL import Image
from io import BytesIO

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

# Function to analyze the document using OpenAI
def analyze_document(pdf_text):
    # Define the prompt based on the refined instructions
    prompt = f"""
    You are a highly capable assistant tasked with extracting detailed room information from an inventory report. Your objectives are:

    1. Identify and list each room by name.
    2. Extract the contents within each room, such as furniture, fixtures, appliances, and other items.
    3. Add a "defects" field to each room, but only include significant defects or damages. Ignore minor issues that do not warrant attention. Defects should be based on both the text descriptions and a thorough analysis of the images related to each room. If no significant defects are found, explicitly state "No significant defects identified."

    Return in JSON format for each room with room name, item name, and defects.
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

# Function to analyze the document using OpenAI for image extraction
def analyze_document_for_images(pdf_text):
    prompt = f"""
    Your task is to analyze the provided text from a property inventory report and follow these steps:

    Detect Room Name: Identify the name of the room described in the text.
    Identify Related Images: Detect all the images in the document that are related to the identified room.
    Gather Page Numbers: Collect the page numbers where these images are located.
    Repeat for Each Room: Continue this process for each room described in the document.

    Avoid Misclassification: If the images are not clearly associated with a particular room, do not include them in the results. Ensure that the output is accurate and does not include hallucinated or misconceived information.
    The text to analyze is:
        {pdf_text}
    Return in the following format:
        "Room name": "list of page numbers", "Another room name": "list of page numbers"

    Give only in the above-mentioned format and nothing else. Follow it strictly.
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

# Function to sanitize folder names
def sanitize_folder_name(name):
    return re.sub(r'[\\/*?:"<>|]', "_", name)

# Function to extract images from specific pages and save them in the corresponding room folder
def extract_images_for_rooms(pdf_path, room_page_dict):
    pdf_document = fitz.open(pdf_path)
    main_folder = "test"

    # Ensure the main directory exists
    if not os.path.exists(main_folder):
        os.makedirs(main_folder)

    for room_name, pages in room_page_dict.items():
        sanitized_room_name = sanitize_folder_name(room_name)
        room_folder = os.path.join(main_folder, sanitized_room_name)
        if not os.path.exists(room_folder):
            os.makedirs(room_folder)

        for page_num in pages:
            page = pdf_document.load_page(page_num - 1)  # Page numbers in PyMuPDF are 0-indexed
            image_list = page.get_images(full=True)

            if image_list:
                for img_index, img in enumerate(image_list):
                    xref = img[0]
                    base_image = pdf_document.extract_image(xref)
                    image_bytes = base_image["image"]
                    image_ext = base_image["ext"]

                    # Load the image data into PIL
                    image = Image.open(BytesIO(image_bytes))

                    # Create a unique filename
                    image_filename = f"{sanitized_room_name}_page_{page_num}_{img_index+1}.{image_ext}"
                    image_path = os.path.join(room_folder, image_filename)

                    # Save the image
                    image.save(image_path)
                    print(f"Saved image: {image_path}")
            else:
                print(f"No images found on page {page_num} for room {sanitized_room_name}.")

# Path to the PDF document
pdf_path = r"inventory.pdf"

# Extract text from the PDF
pdf_text = extract_text_from_pdf(pdf_path)

# Analyze the document and get the JSON output for rooms and pages
json_output = analyze_document_for_images(pdf_text)
if "```" in json_output:
    json_output = json_output.replace("```", "")
formatted_str = "{" + json_output + "}"
formatted_str = formatted_str.replace("'", "\"")


def parse_page_numbers(page_str):
    page_numbers = []
    # Ensure page_str is treated as a string
    parts = page_str.split(',') if isinstance(page_str, str) else page_str
    for part in parts:
        if isinstance(part, str) and '-' in part:  # Handle ranges like '6-9'
            start, end = map(int, part.split('-'))
            page_numbers.extend(range(start, end + 1))
        else:  # Handle single page numbers
            page_numbers.append(int(part))
    return page_numbers

# Convert the string to a dictionary and process page numbers correctly
room_page_dict = json.loads(formatted_str)
for key in room_page_dict:
    room_page_dict[key] = parse_page_numbers(room_page_dict[key])

# Print the JSON output (optional)
print(json.dumps(room_page_dict, indent=4))

# Extract images based on the JSON output
extract_images_for_rooms(pdf_path, room_page_dict)
