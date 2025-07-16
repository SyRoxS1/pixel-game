from PIL import Image

def pixelize_image(input_path, output_path, pixel_size):
    img = Image.open(input_path)


    small = img.resize(
        (img.size[0] // pixel_size, img.size[1] // pixel_size),
        resample=Image.BILINEAR
    )


    result = small.resize(img.size, Image.NEAREST)


    if output_path.lower().endswith(('.jpg', '.jpeg')) and result.mode in ('RGBA', 'LA'):
        result = result.convert('RGB')

    result.save(output_path)




# 100
# 50
# 25
# 10
# 5
# 1