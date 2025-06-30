from PIL import Image

def pixelize_image(input_path, output_path, pixel_size):
    img = Image.open(input_path)
    # Resize down
    small = img.resize(
        (img.size[0] // pixel_size, img.size[1] // pixel_size),
        resample=Image.BILINEAR
    )
    # Scale back up
    result = small.resize(img.size, Image.NEAREST)
    result.save(output_path)



# 100
# 50
# 25
# 10
# 5
# 1