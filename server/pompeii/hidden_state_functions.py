import re

import torch





def get_hidden_state_layers(model, tokenizer, prefix, layers=None):

    tr = get_hidden_states(model, tokenizer, prefix, layers=layers)

    hidden_states = torch.stack([tr[layer_name].output[0] for layer_name in tr.keys()])

    return hidden_states

def get_hidden_state_mlp(model, tokenizer, prefix, layers=None):

    tr = get_hidden_states(model, tokenizer, prefix, layers=layers, layer_key='mlp')

    hidden_states = torch.stack([tr[layer_name].output[0] for layer_name in tr.keys()])

    return hidden_states[:, None, :, :]

def get_hidden_state_attn(model, tokenizer, prefix, layers=None):

    tr = get_hidden_states(model, tokenizer, prefix, layers=layers, layer_key='attn')

    hidden_states = torch.stack([tr[layer_name].output[0] for layer_name in tr.keys()])

    return hidden_states

def get_hidden_state_layer_deltas(model, tokenizer, prefix, layers=None):

    tr = get_hidden_states(model, tokenizer, prefix, layers=layers, other_keys=['transformer.drop'])

    hidden_states = torch.stack([tr[layer_name].output[0] for layer_name in tr.keys() if layer_name != 'transformer.drop'])
    first_hidden_state = tr['transformer.drop'].output[None]
    hidden_states = torch.cat([first_hidden_state, hidden_states])
    delta_hidden_states = hidden_states[1:] - hidden_states[:-1]

    return delta_hidden_states
