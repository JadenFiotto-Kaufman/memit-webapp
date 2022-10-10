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




@app.route('/options', methods=['POST'])
def init():


    response = {
        'hidden_state_options': HiddenStateOption.options()
    }

    return jsonify(response)


@app.route('/logitlens', methods=['GET'])
def logitlens():

    hidden_state_indicies, prompt = request.args.getlist('indicies[]'), request.args.get('prompt')
    hidden_state_indicies = [int(index) for index in hidden_state_indicies]

    hidden_state_options = HiddenStateOption.get_options(hidden_state_indicies)

    result = processor.logitlens(hidden_state_options, prompt)

    rewrite_result = None

    if processor.rewrite_processor is not None:

        rewrite_result = processor.rewrite_processor.logitlens(hidden_state_options, prompt)


    prompt = processor.detokenize(processor.tokenize(prompt))

    response = {
        'data': result,
        'rewrite_data': rewrite_result,
        'prompt': prompt
    }

    return jsonify(response)

@app.route('/generate', methods=['GET'])
def generate():

    number_generated, topk, prompt = int(request.args.get('number_generated')), int(request.args.get('topk')), request.args.get('prompt')

    original_generated = processor.generate(prompt, number_generated, topk)

    rewrite_generated = None

    if processor.rewrite_processor is not None:

        rewrite_generated = processor.rewrite_processor.generate(prompt, number_generated, topk)

    response = {
        'normal_generated': original_generated ,
        'rewrite_generated': rewrite_generated   }

    return jsonify(response)

@app.route('/rewrite', methods=['GET'])
def rewrite():

    layers, prompt, token_idx, target = request.args.getlist('layers[]'), request.args.get('prompt'), int(request.args.get('token_idx')), request.args.get('target')
    layers = [int(layer) for layer in layers]

    rewrite_model = processor.rewrite(prompt, target, layers, token_idx)

    processor.rewrite_processor = Processor('gpt2-xl', model=rewrite_model, low_cpu_mem_usage=True)

    return jsonify(success=True)


if __name__ == '__main__':
    app.run()
