from flask import Flask
from flask import request
from flask import render_template
from flask import send_from_directory
from flask import url_for
from flask_cors import CORS, cross_origin
from gensim.parsing.preprocessing import preprocess_string

app = Flask(__name__)
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

# Process search query

@app.route('/', methods=['GET'])
def take_input():
    input = request.args.get("input")
    input = clean_text(input)
    input = unique(input)
    print(input)
    images = list()
    for tag in input:
#       image_list = get_image(tag)
        image_list = set([1])
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
#    return ''.join(input)

if __name__ == '__main__':
    app.run()
