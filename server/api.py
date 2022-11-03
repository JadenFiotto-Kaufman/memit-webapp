import io
import json
import os
import torch
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS

from .pompeii.hidden_state_options import HiddenStateOption
from .pompeii.Processor import Processor

app = Flask(__name__)

CORS(app)

processor = Processor("EleutherAI/gpt-j-6B", low_cpu_mem_usage=True)

memit_processor = Processor("EleutherAI/gpt-j-6B", low_cpu_mem_usage=True)

dir_path = os.path.dirname(os.path.realpath(__file__))

memit_state_dict = torch.load(os.path.join(dir_path,'memit_gptj.pth'), map_location='cpu')

memit_processor._model.load_state_dict(memit_state_dict)

memit_rewritten_facts = json.load(open(os.path.join(dir_path,'counterfact.json'), 'r'))

memit_rewritten_facts = [{
    'prompt' : case['requested_rewrite']['prompt'].split('{}'),
    'target_new' : case['requested_rewrite']['target_new']['str'],
    'target_true' : case['requested_rewrite']['target_true']['str'],
    'subject' : case['requested_rewrite']['subject'],
    }
 for case in memit_rewritten_facts]

for rewrite_fact in memit_rewritten_facts:
    rewrite_fact['search'] = ' '.join([*rewrite_fact['prompt'], rewrite_fact['target_new'], rewrite_fact['target_true'], rewrite_fact['subject']])

def decode_deltas(data):

    return torch.load(io.BytesIO(data))


@app.route('/options', methods=['GET', 'POST'])
def options():

    response = {
        'hidden_state_options': HiddenStateOption.options(),
    }

    return jsonify(response)

@app.route('/rewritefacts', methods=['GET', 'POST'])
def rewritefacts():

    return jsonify(memit_rewritten_facts)


@app.route('/logitlens', methods=['POST', 'GET'])
def logitlens():

    hidden_state_indicies, prompt, topn = request.args.getlist(
        'indicies[]'), request.args.get('prompt'), int(request.args.get('topn'))
    hidden_state_indicies = [int(index) for index in hidden_state_indicies]

    hidden_state_options = HiddenStateOption.get_options(hidden_state_indicies)

    logitlens = processor.logitlens(hidden_state_options, prompt, topn=topn)

    rewrite_logitlens = memit_processor.logitlens(
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

    rewrite_generated = memit_processor.generate(
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

    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('--port', type=int, default=8081)

    args = parser.parse_args()

    app.config.from_object('server.config.DevConfig')

    app.run(host='0.0.0.0', port=args.port, use_reloader=False)

