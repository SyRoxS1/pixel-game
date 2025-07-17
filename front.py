from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify
from pixelize import pixelize_image
from convert_image_base64 import convert_image_to_base64
from count_nb_images_in_table import count_images
from dtb_select_game_img_path_from_rndm_nbrs import select_image
from dtb_select_game_name_from_rndm_nbrs import select_name
from dtb_search_game_name import search_name
import random

app = Flask(__name__)
@app.route('/', methods=['GET','POST'],)
def index():
    won = request.cookies.get("won", False)

    attempt_count = int(request.cookies.get("attempts", 0))

    if attempt_count == 0:
        pixelization_degree = 100
    if attempt_count == 1:
        pixelization_degree = 70
    if attempt_count == 2:
        pixelization_degree = 50
    if attempt_count == 3:
        pixelization_degree = 30
    if attempt_count == 4:
        pixelization_degree = 20
    if attempt_count == 5:
        pixelization_degree = 10

    # Value shouldnt be used, but just in case
    if attempt_count == 6:
        pixelization_degree = 1

    # If no game cookie is set, start a new game
    if not request.cookies.get("game"):
        random_game_id = random.randint(0, count_images())
        original_image_path = select_image(random_game_id)
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

    if attempt_count > 0 and request.method == "GET":

        attempt_count -= 1

        if attempt_count == 0:
            pixelization_degree = 100
        if attempt_count == 1:
            pixelization_degree = 70
        if attempt_count == 2:
            pixelization_degree = 50
        if attempt_count == 3:
            pixelization_degree = 30
        if attempt_count == 4:
            pixelization_degree = 20
        if attempt_count == 5:
            pixelization_degree = 10

        attempt_count += 1
        guess1 = request.cookies.get("guess1", "")
        guess2 = request.cookies.get("guess2", "")
        guess3 = request.cookies.get("guess3", "")
        guess4 = request.cookies.get("guess4", "")
        guess5 = request.cookies.get("guess5", "")
        guess6 = request.cookies.get("guess6", "")

        original_image_path = select_image(request.cookies.get("game"))
        original_image_path = "images/" + original_image_path
        print(f"Selected image path: {original_image_path}")

        pixelize_image_path = "tmp/"+str(request.cookies.get("game"))+ str(attempt_count) +".jpg"
        pixelize_image(original_image_path, pixelize_image_path, pixelization_degree)
        image = convert_image_to_base64(pixelize_image_path)

        response = make_response(render_template('index.html', b64_img = image, guess1=guess1, guess2=guess2, guess3=guess3, guess4=guess4, guess5=guess5, guess6=guess6))
        response.set_cookie("guess"+str(attempt_count), max_age=60*60*24)
        return response

    original_image_path = select_image(request.cookies.get("game"))
    original_image_path = "images/" + original_image_path
    print(f"Selected image path: {original_image_path}")

    pixelize_image_path = "tmp/"+str(request.cookies.get("game"))+ str(attempt_count) +".jpg"
    pixelize_image(original_image_path, pixelize_image_path, pixelization_degree)
    image = convert_image_to_base64(pixelize_image_path)

    if request.method == "POST":

        game_title_guess = request.form.get("game")
        if select_name(request.cookies.get("game")) != game_title_guess:
            game_title_guess += "❌"

        guess1 = request.cookies.get("guess1", "")
        guess2 = request.cookies.get("guess2", "")
        guess3 = request.cookies.get("guess3", "")
        guess4 = request.cookies.get("guess4", "")
        guess5 = request.cookies.get("guess5", "")
        guess6 = request.cookies.get("guess6", "")

        if attempt_count == 1:
            guess1 = game_title_guess
        elif attempt_count == 2:
            guess2 = game_title_guess
        elif attempt_count == 3:
            guess3 = game_title_guess
        elif attempt_count == 4:
            guess4 = game_title_guess
        elif attempt_count == 5:
            guess5 = game_title_guess
        elif attempt_count == 6:
            guess6 = game_title_guess


        if select_name(request.cookies.get("game")) == game_title_guess:
            print(f"Correct guess: {game_title_guess}")
            game_title_guess += "✅" 
            pixelization_degree = 1
            original_image_path = select_image(request.cookies.get("game"))
            original_image_path = "images/" + original_image_path
            print(f"Selected image path: {original_image_path}")

            pixelize_image_path = "tmp/"+str(request.cookies.get("game"))+ str(attempt_count) +".jpg"
            pixelize_image(original_image_path, pixelize_image_path, pixelization_degree)
            image = convert_image_to_base64(pixelize_image_path)
            response = make_response(render_template('won.html',b64_img = image, guess1=guess1, guess2=guess2, guess3=guess3, guess4=guess4, guess5=guess5, guess6=guess6,winning_guess=game_title_guess))
            response.set_cookie("won", str(1), max_age=60*60*24)
            return response
        
        elif attempt_count == 6:
            pixelization_degree = 1
            original_image_path = select_image(request.cookies.get("game"))
            original_image_path = "images/" + original_image_path
            print(f"Selected image path: {original_image_path}")
        
            pixelize_image_path = "tmp/"+str(request.cookies.get("game"))+ str(attempt_count) +".jpg"
            pixelize_image(original_image_path, pixelize_image_path, pixelization_degree)
            image = convert_image_to_base64(pixelize_image_path)
            response = make_response(render_template('lost.html',b64_img = image, guess1=guess1, guess2=guess2, guess3=guess3, guess4=guess4, guess5=guess5, guess6=guess6,winning_guess=select_name(request.cookies.get("game"))))
            response.set_cookie("won", str(0), max_age=60*60*24)
            return response


        
        
        print(f"Guesses: {guess1}, {guess2}, {guess3}, {guess4}, {guess5}, {guess6}")
        response = make_response(render_template('index.html', b64_img = image, guess1=guess1, guess2=guess2, guess3=guess3, guess4=guess4, guess5=guess5, guess6=guess6))
        response.set_cookie("guess"+str(attempt_count), game_title_guess, max_age=60*60*24)

        if attempt_count < 6:
            attempt_count += 1  # Increase attempt count
        print(f"Attempt #{attempt_count}: {game_title_guess}")
        
        response.set_cookie("attempts", str(attempt_count), max_age=60*60*24)  # 1 day expiry
        return response
    
    if attempt_count == 6:
        return redirect("/reset")
    
    print(f"Attempt #{attempt_count}: {request.cookies.get('game')}")
    
    return render_template('index.html',b64_img = image)


@app.route("/search")
def search():
    query = request.args.get("q", "")
    if not query:
        return jsonify([])

    results = search_name(query)
    return jsonify(results)

@app.route("/reset",methods=['GET','POST'],)
def reset():
    resp = make_response(redirect('/'))  # or render_template(...) if you prefer
    for cookie in request.cookies:
        resp.set_cookie(cookie, '', expires=0)
    return resp



if __name__ == '__main__':
    app.run(debug=True,port=80,host='10.0.0.16')