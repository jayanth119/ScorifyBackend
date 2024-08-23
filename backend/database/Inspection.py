import base64
import requests
from openai import OpenAI

# OpenAI API Key
client = OpenAI(api_key="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")
api_key = "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"
ar=input("Enter the condition: ")
itemname=input("Enter the item name: ")
# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Path to your image
image_path = ["/content/test8.jpeg","/content/test10.jpeg"]

# Encode the image

# Define the headers
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}
def analy(itemname, ar, base64_image):
    # Construct the prompt with the variables
    prompt = f"""
    You are an assistant with the ability to analyze images for object detection. Your task is to identify and list only property-related objects such as furniture, fixtures, and other material items in an image. After detecting the objects, evaluate each for potential defects, such as cracks, damage, wear, or any other signs of imperfection.
    And Evaluate as one object which is Main And also decide the defect is present or not.
    Now Do the following tasks:
    1.Identify the object, is it the same or similar to '{itemname}', return yes or no as a result for this.
    2.Rate the '{itemname}' in three categories: 
      i. Good -- If the '{itemname}' is fully perfect.
      ii. Fair -- If the '{itemname}' has just notable defects but not much.
      iii. Repair -- If the '{itemname}' has wearable defects like cracks, breakage, or other forms of damage that require repair.
    Check the rating you decide with the user given i.e '{ar}' is the same or not, if yes then return yes, if not then return NO and provide a description.

    Now give the JSON of your results for the above tasks .
    '{itemname}': Yes or no
    if '{itemname}' is no:
      '{itemname}' description:
    if '{itemname}'is yes:
      no need of object name description
    '{itemname}' rating : Yes or no
    if '{itemname}'rating is no:
      '{itemname}'description:
    if '{itemname}' is yes:
      no need of '{itemname}' description
    """

    # Construct the payload
    payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }

    # Send the request to the API
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    # Check if the response contains 'choices'
    if 'choices' in response.json():
        # Extract the JSON content from the assistant's response
        json_content = response.json()['choices'][0]['message']['content']
        return json_content
    else:
        # Handle the error and return the response for debugging
        return "Error: 'choices' not found in the response. Full response:\n" + response.text

# Call the function and print the extracted JSON content
l=[]
def final_result(l,itemname):
  prompt = f"""
    You are assigned to check give the final conclusion.
    {l} contains details about item name and item rating .
    Check '{l}' and draw conclusions on: 
      i.Does all the items are same or not ,Decide yes or no.
      ii.Finalize the rating ,if all are same items and if any item rating is no then the rating would be no.
      iii.If the finalized rating is no then summarize the object rating description.
      iv.Give the final result  in the following format:
            '{itemname}':Yes or no
            if '{itemname}' is no:
              '{itemname}' description:
            '{itemname}'rating: yes or no
            if '{itemname}'rating is no:
              '{itemname}'description:
     NOte: Give only in the above format dont do in any other format.Dont include your process too.
     
    """
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

for i in image_path:
  base64_image = encode_image(i)
  l.append(analy(itemname, ar, base64_image))
print(final_result(l,itemname))

