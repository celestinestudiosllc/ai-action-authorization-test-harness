import yaml
from pathlib import Path

def load_matrices(path):
    matrices = []
    for file in Path(path).glob("*.yaml"):
        with open(file, "r") as f:
            matrices.append(yaml.safe_load(f))
    return matrices