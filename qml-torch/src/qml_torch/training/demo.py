"""A bundled reproducible dataset so a PyPI install can run a complete demo."""

from __future__ import annotations

import torch

from ..validation import DataBundle


def make_demo_data(n_features: int = 2, seed: int = 7) -> DataBundle:
    """Make balanced noisy classes, independently split into 48 train / 16 test.

    Features are angles in radians. Labels and noise use a local generator, so
    making demo data does not change the caller's global random state.
    """

    generator = torch.Generator().manual_seed(seed)

    def split(per_class: int) -> tuple[torch.Tensor, torch.Tensor]:
        labels = torch.arange(2).repeat_interleave(per_class).float()
        centers = (labels * 2 - 1).unsqueeze(1).expand(-1, n_features)
        # RY encodings have useful variation away from symmetric +/- angles.
        features = 1.3 + centers * 0.65
        features = features + torch.randn(features.shape, generator=generator) * 0.3
        order = torch.randperm(len(labels), generator=generator)
        return features[order], labels[order]

    x_train, y_train = split(24)
    x_test, y_test = split(8)
    return DataBundle(x_train, y_train, x_test, y_test)
