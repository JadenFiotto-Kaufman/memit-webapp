import yaml
from pathlib import Path
import os

with open(os.path.join(Path(__file__).parent.parent.resolve(), 'globals.yml'), "r") as stream:
    data = yaml.safe_load(stream)

(RESULTS_DIR, DATA_DIR, STATS_DIR, HPARAMS_DIR,) = (
    Path(z)
    for z in [
        data["RESULTS_DIR"],
        data["DATA_DIR"],
        data["STATS_DIR"],
        data["HPARAMS_DIR"],
    ]
)

REMOTE_ROOT_URL = data["REMOTE_ROOT_URL"]
