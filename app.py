from flask import Flask, request, jsonify
from flask import render_template, send_file, make_response
from PIL import Image, ImageDraw, ImageFont, ImageOps
import io
from io import StringIO


app = Flask(__name__)

# Function to paste text on the image
def paste_text_on_image(image_path, text, text2):
    # Opening the primary image (used in background)
    img = Image.new("RGBA", (4000, 4000), (255, 255, 255))

    img1 = Image.open(image_path).convert("RGBA")
    img1 = ImageOps.contain(img1, (3588,2648))

    # Opening the secondary image (overlay image)
    img2 = Image.open("mfo_1.png")
    
    # Pasting img2 image on top of img1 
    # starting at coordinates (0, 0)
    x = (img2.width - img1.width) // 2
    y = (img2.height - img1.height - 600) // 2

    img.paste(img1, (x,y), mask = img1)
    img.paste(img2, (0,0), mask = img2)
    
    
    # Call draw Method to add 2D graphics in an image
    I1 = ImageDraw.Draw(img)
    
    # Custom font style and font size
    myFont = ImageFont.truetype('rugsnatcher.otf', 256)
    
    # Add Text to an image
    I1.text((2442, 350), text, font=myFont, fill =(92, 182, 217), anchor="mm")
    I1.text((2690, 3298), text2, font=myFont, fill =(255, 233, 189),  anchor="mm")
    #draw.text((width/2, height/2), "my text", font=my_font, anchor="mm")

    edited_image = io.BytesIO()
    img.save(edited_image, 'PNG')
    return edited_image.getvalue()


@app.route('/', methods=['GET'])
def index():
    return render_template('main.html')

@app.route('/paste_text_on_image', methods=['POST'])
def paste_text_on_image_route():
    # Get the image and text from the request
    image_file = request.files['image']
    text = request.form['text']
    text2 = request.form['text2']

    # Check if both image and text are provided
    if not image_file or not text:
        return jsonify({'error': 'Image and text are required.'}), 400

    # Process the image and text
    edited_image_data = paste_text_on_image(image_file, text, text2)

    response = make_response(edited_image_data)
    response.headers.set('Content-Type', 'image/png')
    
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0')
