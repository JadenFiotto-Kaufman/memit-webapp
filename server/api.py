import io
from uuid import uuid1
import torch
from flask import Flask, jsonify, session, request, Response, send_file
from flask_cors import CORS
from .pompeii.Processor import Processor
from .pompeii.hidden_state_options import HiddenStateOption

app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = 'debug_key'

CORS(app, resources={r'/*': {'origins': '*'}})

processor = Processor('gpt2-xl', low_cpu_mem_usage=True)


def initialization_required(func):
    def wrapper():

        if not session.get('uuid'):
            return Response(
                'Uninitialized',
                401
            )

        return func()
    return wrapper


@app.route('/init', methods=['POST'])
def init():

    session['uuid'] = uuid1()

    response = {
        'hidden_state_options': HiddenStateOption.options()
    }

    return jsonify(response)


@initialization_required
@app.route('/logitlens', methods=['GET'])
def logitlens():

    hidden_state_indicies, prompt = request.args.getlist('indicies[]'), request.args.get('prompt')
    hidden_state_indicies = [int(index) for index in hidden_state_indicies]

    hidden_state_options = HiddenStateOption.get_options(hidden_state_indicies)

    result = processor.logitlens(hidden_state_options, prompt)

    prompt = processor.detokenize(processor.tokenize(prompt))

    response = {
        'data': result,
        'prompt': prompt
    }

    return jsonify(response)

@initialization_required
@app.route('/generate', methods=['GET'])
def generate():

    number_generated, prompt = int(request.args.get('number_generated')), request.args.get('prompt')

    normal_generated = processor.generate(prompt, number_generated)

    response = {
        'normal_generated': normal_generated    }

    return jsonify(response)

@initialization_required
@app.route('/rewrite', methods=['GET'])
def rewrite():

    layers, prompt, token_idx, target = request.args.getlist('layers[]'), request.args.get('prompt'), int(request.args.get('token_idx')), request.args.get('target')
    layers = [int(layer) for layer in layers]

    edited_state_dict = processor.rewrite(prompt, target, layers, token_idx)

    file = io.BytesIO()
    torch.save(edited_state_dict, file, _use_new_zipfile_serialization=False)
    file.seek(0)

    return send_file(file, mimetype='application/octet-stream')


if __name__ == '__main__':
    app.run()
