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

    if not request.cookies.get("game"):
        random_game_id = random.randint(0, count_images())
        response = make_response(render_template('index.html'))
        response.set_cookie("game", str(random_game_id), max_age=60*60*24)
        return response

    original_image_path = select_image(int(request.cookies.get("game")))
    pixelize_image(original_image_path, "tmp/"+request.cookies.get("game")+ attempt_count +".jpg",attempt_count)
    image = convert_image_to_base64("tmp/"+request.cookies.get("game")+ attempt_count +".jpg")

    if request.method == "POST":
        game_title = request.form.get("game")
        attempt_count += 1  # Increase attempt count
        print(f"Attempt #{attempt_count}: {game_title}")
        response = make_response(render_template('index.html'), b64_img = image)
        response.set_cookie("attempts", str(attempt_count), max_age=60*60*24)  # 1 day expiry
        return response
    
    if attempt_count == 6:
        return "Finished"
    
    print(f"Attempt #{attempt_count}: {request.cookies.get('game')}")
    
    return render_template('index.html',b64_img = image)




if __name__ == '__main__':
    app.run(debug=True)