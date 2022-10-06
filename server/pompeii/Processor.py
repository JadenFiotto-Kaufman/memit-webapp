import copy
import os
import re
from pathlib import Path
from typing import Callable, List

import numpy as np
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from .nethook import TraceDict
from .rome.rome import ROMEHyperParams, apply_rome_to_model
from .rome.util import generate, nethook


class Processor:

    def __init__(self,
        model_name,
        low_cpu_mem_usage=True,
        layers=None,
        ):

        model = AutoModelForCausalLM.from_pretrained(model_name, low_cpu_mem_usage=low_cpu_mem_usage).to("cuda")
        tokenizer = AutoTokenizer.from_pretrained(model_name)

        tokenizer.pad_token = tokenizer.eos_token

        nethook.set_requires_grad(False, model)


        self._model_name = model_name
        self._model = model
        self._decoder = torch.nn.Sequential(self._model.transformer.ln_f, self._model.lm_head)
        self._tokenizer = tokenizer

        if not layers:
            layers = list(range(
            len([n for n, _ in model.named_modules()
             if re.match('^transformer.h.\d+$', n)])))

        self._layers = layers
    
    def _get_hidden_states(self, 
        hidden_state_options: List,
        prompt: str
    ):

        input = self._tokenizer(prompt, return_tensors='pt')
        input = {key: value[None].cuda() for key, value in input.items()}
        
        option_keys = self._get_keys(hidden_state_options)  

        all_keys = [y for x in option_keys.values() for y in x]  

        with TraceDict(self._model, all_keys) as trace:
            self._model(**input)['logits']

        result = {}

        for hidden_state_option in hidden_state_options:

            _result = {key: value for key, value in trace.items() if key in option_keys[hidden_state_option._index]}
            result[hidden_state_option._index] = hidden_state_option.post_process(_result)

        return result

    def _get_keys(self, 
        hidden_state_options: List
    ):
        layer_keys = {}

        for hidden_state_option in hidden_state_options:

            layer_key = hidden_state_option.layer_key

            layer_keys[hidden_state_option._index] = [f"transformer.h.{i}{'.' + layer_key if layer_key else ''}" for i in self._layers]

            if hidden_state_option.other_keys:

                layer_keys[hidden_state_option._index].extend(hidden_state_option.other_keys)

        return layer_keys

    def probabilities(self, tokens):

        return torch.nn.functional.softmax(tokens, dim=-1)

    def decode(self, hidden_states):

        return self._decoder(hidden_states)

    def tokenize(self, prompt):

        return self._tokenizer.encode(prompt)

    def detokenize(self, tokens):

        return [self._tokenizer.decode(token) for token in tokens]

    def generate(self, prompt, number_generated):

        generated = generate.generate_fast(self._model, self._tokenizer, [prompt], n_gen_per_prompt=1, top_k=1, max_out_len=number_generated)[0]

        return generated

    # def apply_rewrite(self, edited_state_dict):

        

    def rewrite(self, prompt, target, layers, token_idx):

        model_copy = copy.deepcopy(self._model.cpu()).cuda()

        nethook.set_requires_grad(True, model_copy)

        hyperparams_path = os.path.join(Path(__file__).parent.resolve(), "rome/hparams", "ROME", f"{self._model_name}.json")

        hparams = ROMEHyperParams.from_json(hyperparams_path)
        hparams.layers = layers

        request = {
            "prompt": prompt,
            "token_idx" :token_idx,
            "target": target
        }

        edited_model, orig_weights = apply_rome_to_model(
            model_copy, 
            self._tokenizer, 
            request, 
            hparams, 
            copy=False
        )

        edited_state_dict = edited_model.cpu().state_dict()

        del edited_model, model_copy

        return edited_state_dict

    def logitlens(self, 
        hidden_state_function: Callable,
        prompt: str,
        topk: int = 5):
        
        options_hidden_states = self._get_hidden_states(hidden_state_function, prompt)

        result = {}

        for key in options_hidden_states:

            hidden_states = options_hidden_states[key]

            tokens = self.decode(hidden_states)

            probabilities = self.probabilities(tokens).cpu()

            top_probs, top_tokens = probabilities.topk(k=topk, dim=-1)
            top_probs, top_tokens = top_probs[:,0].numpy(), top_tokens[:,0].numpy()

            top_words = np.array([[self.detokenize(_tokens) for _tokens in tokens] for tokens in top_tokens])

            result[key] = {'words' : top_words.tolist(), 'probabilities' : top_probs.tolist()}

        return result

   
