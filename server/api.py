import io
import torch
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from .pompeii.Processor import Processor
from .pompeii.hidden_state_options import HiddenStateOption

app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = 'debug_key'

CORS(app, resources={r'/*': {'origins': '*'}})

processor = Processor('gpt2-xl', low_cpu_mem_usage=True)


def decode_deltas(data):

    return torch.load(io.BytesIO(data))


@app.route('/options', methods=['POST'])
def options():

    response = {
        'hidden_state_options': HiddenStateOption.options()
    }

    return jsonify(response)


@app.route('/logitlens', methods=['POST', 'GET'])
def logitlens():

    hidden_state_indicies, prompt, topn = request.args.getlist(
        'indicies[]'), request.args.get('prompt'), int(request.args.get('topn'))
    hidden_state_indicies = [int(index) for index in hidden_state_indicies]

    hidden_state_options = HiddenStateOption.get_options(hidden_state_indicies)

    logitlens = processor.logitlens(hidden_state_options, prompt, topn=topn)

    rewrite_logitlens = None

    if len(request.data) > 0:

        rewrite_processor = Processor('gpt2-xl', low_cpu_mem_usage=True)

        rewrite_processor.rewrite_apply(decode_deltas(request.data))

        rewrite_logitlens = rewrite_processor.logitlens(
            hidden_state_options, prompt, topn=topn)

    prompt = processor.detokenize(processor.tokenize(prompt))

    response = {
        'logitlens': logitlens,
        'rewrite_logitlens': rewrite_logitlens,
        'prompt': prompt
    }

    return jsonify(response)

@app.route('/generate', methods=['POST', 'GET'])
def generate():

    number_generated, topk, prompt = int(request.args.get('number_generated')), int(
        request.args.get('topk')), request.args.get('prompt')

    generated = processor.generate(prompt, number_generated, topk)

    rewrite_generated = None

    if len(request.data) > 0:

        rewrite_processor = Processor('gpt2-xl', low_cpu_mem_usage=True)

        rewrite_processor.rewrite_apply(decode_deltas(request.data))

        rewrite_generated = rewrite_processor.generate(
            prompt, number_generated, topk)

    response = {
        'generated': generated,
        'rewrite_generated': rewrite_generated
    }

    return jsonify(response)


@app.route('/rewrite', methods=['GET'])
def rewrite():

    layers, prompt, token_idx, target = request.args.getlist('layers[]'), request.args.get(
        'prompt'), int(request.args.get('token_idx')), request.args.get('target')
    layers = [int(layer) - 1 for layer in layers]

    deltas = processor.rewrite_deltas(prompt, target, layers, token_idx)

    to_send = io.BytesIO()
    torch.save(deltas, to_send, _use_new_zipfile_serialization=False)
    to_send.seek(0)

    return send_file(to_send, mimetype='application/octet-stream')


if __name__ == '__main__':
    app.run()
