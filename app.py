from flask import Flask
from flask import request
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

# Process search query

@app.route('/', methods=['GET'])
def take_input():
    input = request.args.get("input")
    input = clean_text(input)
    input = unique(input)
    # TODO
    # DB
    # Find common and render 
    return ''.join(input)

if __name__ == '__main__':
    app.run()
