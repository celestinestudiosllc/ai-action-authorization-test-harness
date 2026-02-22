# src/harness/loader.py

from __future__ import annotations

import os
import glob
from typing import List, Dict, Any

import yaml


def _load_yaml_file(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    if not isinstance(data, dict):
        raise ValueError(f"Matrix YAML must be a mapping/dict: {path}")
    return data


def load_matrices(matrices_path: str) -> List[Dict[str, Any]]:
    """
    Load matrices from either:
      - a directory containing *.yaml / *.yml files, OR
      - a single YAML file path.

    Returns a list of matrix dicts.
    """
    matrices_path = os.path.expanduser(matrices_path)

    if os.path.isfile(matrices_path):
        # Single file mode
        if not (matrices_path.endswith(".yaml") or matrices_path.endswith(".yml")):
            raise ValueError(f"Matrix file must be .yaml or .yml: {matrices_path}")
        return [_load_yaml_file(matrices_path)]

    if not os.path.isdir(matrices_path):
        raise FileNotFoundError(f"Matrices path not found: {matrices_path}")

    # Directory mode (existing behavior, but more robust)
    patterns = [
        os.path.join(matrices_path, "*.yaml"),
        os.path.join(matrices_path, "*.yml"),
    ]

    files: List[str] = []
    for pat in patterns:
        files.extend(glob.glob(pat))

    files = sorted(set(files))

    matrices: List[Dict[str, Any]] = []
    for fp in files:
        matrices.append(_load_yaml_file(fp))

    return matrices