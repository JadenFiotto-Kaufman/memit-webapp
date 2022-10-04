"""
Contains utilities for extracting token representations and indices
from string templates. Used in computing the left and right vectors for ROME.
"""

from typing import List
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from ..util import nethook

def get_repr_at_idxs(
    model: AutoModelForCausalLM,
    tok: AutoTokenizer,
    context: str,
    idxs: List[int],
    layer: int,
    module_template: str,
    track: str = "in",
) -> torch.Tensor:
    """
    Runs input through model and returns averaged representations of the tokens
    at each index in `idxs`.
    """

    assert track in {"in", "out"}
    tin, tout = (
        (track == "in"),
        (track == "out"),
    )
    module_name = module_template.format(layer)
    context_tok = tok([context], return_tensors="pt").to(
        next(model.parameters()).device
    )

    with torch.no_grad():
        with nethook.Trace(
            model,
            module_name,
            retain_input=tin,
            retain_output=tout,
        ) as tr:
            model(**context_tok)

    # cur_repr is already detached due to torch.no_grad()
    cur_repr = tr.input if track == "in" else tr.output
    cur_repr = cur_repr[0] if type(cur_repr) is tuple else cur_repr

    return torch.stack([cur_repr[0, i, :] for i in idxs], dim=1).mean(1)
