import base64

def convert_image_to_base64(image_path):


    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

    # Choose the correct MIME type (e.g., image/png, image/jpeg, image/gif)
    mime_type = "image/png"  # Change this depending on your image type
    base64_image = f"data:{mime_type};base64,{encoded_string}"

    return base64_image