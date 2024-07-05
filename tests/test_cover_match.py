import numpy as np
import pytest
from cover_match import rank, read_image, sift_matches, synthetic_images

def test_identical_ranks_first():
    query, candidates = synthetic_images()
    result = rank(query, candidates)
    assert result[0]["image"] == "synthetic-identical"
    assert result[0]["ssim"] == pytest.approx(1)
    assert result[0]["sift_matches"] > 0

def test_featureless_images():
    blank = np.zeros((100, 100, 3), dtype=np.uint8)
    assert sift_matches(blank, blank) == 0

def test_unreadable_image(tmp_path):
    with pytest.raises(ValueError, match="Cannot read image"):
        read_image(tmp_path / "missing.png")

def test_empty_gallery():
    query, _ = synthetic_images()
    assert rank(query, []) == []
