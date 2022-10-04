from uuid import uuid1

from flask import Flask, jsonify, session, request, Response
from flask_cors import CORS
from .pompeii.logitlens import LogitLens
from .pompeii.hidden_state_options import HiddenStateOption

app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = 'debug_key'

CORS(app, resources={r'/*': {'origins': '*'}})

logit_lens = LogitLens('gpt2-xl', low_cpu_mem_usage=True)


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

    result = logit_lens(hidden_state_options, prompt)

    prompt = logit_lens.detokenize(logit_lens.tokenize(prompt))

    response = {
        'data': result,
        'prompt': prompt
    }

    return jsonify(response)


if __name__ == '__main__':
    app.run()
