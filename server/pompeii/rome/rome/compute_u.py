import logging
import os
from pathlib import Path
from typing import Dict, List

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from ..util.globals import *
from . import repr_tools
from .layer_stats import layer_stats
from .rome_hparams import ROMEHyperParams

# Cache variables
inv_mom2_cache = {}


def get_inv_cov(
    model: AutoModelForCausalLM,
    tok: AutoTokenizer,
    layer_name: str,
    mom2_dataset: str,
    mom2_n_samples: str,
    mom2_dtype: str,
) -> torch.Tensor:
    """
    Retrieves covariance statistics, then computes the algebraic inverse.
    Caches result for future use.
    """

    global inv_mom2_cache

    model_name = model.config._name_or_path.replace("/", "_")
    key = (model_name, layer_name)

    if key not in inv_mom2_cache:
        logging.info(
            f"Retrieving inverse covariance statistics for {model_name} @ {layer_name}. "
            f"The result will be cached to avoid repetitive computation."
        )
        stat = layer_stats(
            model,
            tok,
            layer_name,
            STATS_DIR,
            mom2_dataset,
            to_collect=["mom2"],
            sample_size=mom2_n_samples,
            precision=mom2_dtype,
            progress=None
        )
        inv_mom2_cache[key] = torch.inverse(
            stat.mom2.moment().to("cuda")
        ).float()  # Cast back to float32

    return inv_mom2_cache[key]


def compute_u(
    model: AutoModelForCausalLM,
    tok: AutoTokenizer,
    request: Dict,
    hparams: ROMEHyperParams,
    layer: int,
    context_templates: List[str],
) -> torch.Tensor:
    """
    Computes the right vector used in constructing the rank-1 update matrix.
    """

    logging.info("Computing left vector (u)...")

    # Compute projection token
    word_repr_args = dict(
        model=model,
        tok=tok,
        layer=layer,
        module_template=hparams.rewrite_module_tmp,
        track="in",
    )
 
    cur_repr = torch.stack(
        [  # TODO batch this to improve performance
            repr_tools.get_repr_at_idxs(
                context=templ.format(request["prompt"]),
                idxs=[request['token_idx_inverse']],
                **word_repr_args
            )
            for templ in context_templates
        ],
        dim=0,
    ).mean(0)

    # Apply inverse second moment adjustment
    u = cur_repr
    if hparams.mom2_adjustment:
        u = get_inv_cov(
            model,
            tok,
            hparams.rewrite_module_tmp.format(layer),
            hparams.mom2_dataset,
            hparams.mom2_n_samples,
            hparams.mom2_dtype,
        ) @ u.unsqueeze(1)
        u = u.squeeze()

    return u / u.norm()
