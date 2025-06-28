from flask import Flask, render_template, request, redirect, url_for, make_response
from pixelize import pixelize_image
from convert_image_base64 import convert_image_to_base64
from count_nb_images_in_table import count_images
from dtb_select_game_from_rndm_nbrs import select_image
import random

app = Flask(__name__)
@app.route('/', methods=['GET','POST'],)
def index():
    attempt_count = int(request.cookies.get("attempts", 0))

    if attempt_count == 0:
        pixelization_degree = 100
    if attempt_count == 1:
        pixelization_degree = 50
    if attempt_count == 2:
        pixelization_degree = 25
    if attempt_count == 3:
        pixelization_degree = 10
    if attempt_count == 4:
        pixelization_degree = 5
    if attempt_count == 5:
        pixelization_degree = 1
    if attempt_count == 6:
        pixelization_degree = 1


    if not request.cookies.get("game"):
        random_game_id = random.randint(0, count_images())
        original_image_path = select_image(request.cookies.get("game"))
        original_image_path = "images/" + original_image_path
        print(f"Selected image path: {original_image_path}")

        pixelize_image_path = "tmp/"+str(random_game_id)+ str(attempt_count) +".jpg"
        print(f"Pixelizing image at: {pixelize_image_path} to attempt count: {attempt_count} to {original_image_path}")
        pixelize_image(original_image_path, pixelize_image_path, pixelization_degree)
        image = convert_image_to_base64(pixelize_image_path)
        response = make_response(render_template('index.html',b64_img = image))
        response.set_cookie("game", str(random_game_id), max_age=60*60*24)
        if attempt_count < 6:
            attempt_count += 1
        response.set_cookie("attempts", str(attempt_count), max_age=60*60*24) 
        return response

    original_image_path = select_image(request.cookies.get("game"))
    original_image_path = "images/" + original_image_path
    print(f"Selected image path: {original_image_path}")

    pixelize_image_path = "tmp/"+str(request.cookies.get("game"))+ str(attempt_count) +".jpg"
    pixelize_image(original_image_path, pixelize_image_path, pixelization_degree)
    image = convert_image_to_base64(pixelize_image_path)

    if request.method == "POST":
        game_title_guess = request.form.get("game")
        if attempt_count < 6:
            attempt_count += 1  # Increase attempt count
        print(f"Attempt #{attempt_count}: {game_title_guess}")
        response = make_response(render_template('index.html', b64_img = image))
        response.set_cookie("attempts", str(attempt_count), max_age=60*60*24)  # 1 day expiry
        return response
    
    if attempt_count == 6:
        return "Finished"
    
    print(f"Attempt #{attempt_count}: {request.cookies.get('game')}")
    
    return render_template('index.html',b64_img = image)




if __name__ == '__main__':
    app.run(debug=True,port=80,host='10.0.0.16')