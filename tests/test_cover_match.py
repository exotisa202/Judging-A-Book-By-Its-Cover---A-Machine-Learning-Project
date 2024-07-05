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


def test_visual_report_contains_computed_results():
    from demo_report import build_report
    report = build_report()
    assert 'synthetic-identical' in report
    assert '1.0000' in report
    assert 'data:image/png;base64,' in report
    assert 'Smoke test, not research accuracy' in report
    assert 'https://' not in report
