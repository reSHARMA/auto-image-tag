from flask import Flask
from flask import request
from flask import render_template
from flask import send_from_directory
from flask import url_for
from flask_uploads import UploadSet, configure_uploads, IMAGES
from werkzeug import secure_filename
import uuid
import redis
import subprocess
from flask_cors import CORS, cross_origin
from gensim.parsing.preprocessing import preprocess_string

app = Flask(__name__)

r = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)

photos = UploadSet('photos', IMAGES)
app.config['UPLOADED_PHOTOS_DEST'] = 'static/img'
configure_uploads(app, photos)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

def clean_text(input):
    return preprocess_string(input)

def unique(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]

def build_tree(low, high, node, images, seg):
    if low > high:
        pass
    elif low == high:
        seg[node] = images[low]
    else:
        mid = (low + high) / 2;
        build_tree(low, mid, 2 * node + 1, images, seg)
        build_tree(mid + 1, high, 2 * node + 2, images, seg)
        seg[node] = seg[2 * node + 1].intersection(seg[2 * node + 2])

def add_db(tag, idx):
    r.sadd(tag, idx)

def get_image(tag):
    return r.smembers(tag)

# Process search query

def yolo():
    cmd = ["darknet/darknet", "detect", "cfg/yolov3.cfg", "yolov3.weights", "static/img/" + idx + "jpeg"]
    with open('text_output.txt', 'w') as fout:
        subprocess.Popen(cmd, stdout=fout,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE)

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/upload', methods=['GET'])
def upload_home():
    return render_template('upload.html')

@app.route('/query', methods=['GET'])
def take_input():
    input = request.args.get("input")
    input = clean_text(input)
    input = unique(input)
    print(input)
    images = list()
    for tag in input:
        image_list = get_image(tag)
#       image_list = set([1])
        print(image_list)
        images.append(image_list)
    seg = [0] * (len(images) * 4)
    build_tree(0, len(images) - 1, 0, images, seg)
    output = list()
    for x in seg:
        if isinstance(x, set):
            for y in x:
                output.append(y)
    output = unique(output)
    return render_template('out.html', images=output)
#   return ''.join(input)

@app.route('/insert', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'photo' in request.files:
        code = str(int(uuid.uuid4()))
        filename = photos.save(request.files['photo'], name=code + ".jpeg")
#       tag = set(yolo(code))
        tag = set(["cat", "dog"])
        out = "Tags found are "
        for t in tag:
            add_db(t, code)
            out = out + " " + t
        return out
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)
