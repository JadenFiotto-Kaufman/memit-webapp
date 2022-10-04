from dataclasses import dataclass
from typing import Callable, List, Tuple

import torch


def post_stack(trace):
    return torch.stack([trace[layer_name].output[0] for layer_name in trace.keys()])


@dataclass
class HiddenStateOption:

    name: str
    color: Tuple[int, int, int]
    layer_key: str = ''
    other_keys: List[str] = None
    post_process: Callable = post_stack

    __instances__ = []

    @classmethod
    def options(cls):
        return [instance.dict() for instance in HiddenStateOption.__instances__]

    @classmethod
    def get_option(cls, index):
        return HiddenStateOption.__instances__[index]

    @classmethod
    def get_options(cls, indicies):
        return [HiddenStateOption.get_option(index) for index in indicies]

    def __post_init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self._index = len(HiddenStateOption.__instances__)
        HiddenStateOption.__instances__.append(self)

    def dict(self):

        return {
            'name': self.name,
            'color': self.color,
            'index': self._index
        }


def post_layer_delta(trace):

    hidden_states = torch.stack([trace[layer_name].output[0]
                                for layer_name in trace.keys() if layer_name != 'transformer.drop'])
    first_hidden_state = trace['transformer.drop'].output[None]
    hidden_states = torch.cat([first_hidden_state, hidden_states])
    delta_hidden_states = hidden_states[1:] - hidden_states[:-1]

    return delta_hidden_states

def post_mlp(trace):

    return post_stack(trace)[:, None, :, :]


HiddenStateOption('Layer', (0, 0, 255))
HiddenStateOption('Layer Delta', (255, 0, 255), other_keys=[
                  'transformer.drop'], post_process=post_layer_delta)
HiddenStateOption('MLP', (0, 255, 0), layer_key='mlp', post_process=post_mlp)
HiddenStateOption('ATTN', (255, 0, 0), layer_key='attn')
