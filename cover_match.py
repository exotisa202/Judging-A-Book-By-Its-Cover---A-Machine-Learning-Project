"""Local-image adaptation of the original histogram -> SSIM -> SIFT notebook."""
import argparse
import json
from pathlib import Path
import cv2
import numpy as np
from skimage.metrics import structural_similarity

def read_image(path):
    image = cv2.imread(str(path), cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError(f"Cannot read image: {path}")
    return cv2.resize(image, (100, 100))

def histogram(image):
    hist = cv2.calcHist([image], [0, 1, 2], None, [8, 8, 8], [0, 256] * 3)
    return cv2.normalize(hist, None)

def sift_matches(a, b):
    sift = cv2.SIFT_create()
    _, da = sift.detectAndCompute(cv2.cvtColor(a, cv2.COLOR_BGR2GRAY), None)
    _, db = sift.detectAndCompute(cv2.cvtColor(b, cv2.COLOR_BGR2GRAY), None)
    if da is None or db is None or len(db) < 2:
        return 0
    pairs = cv2.BFMatcher().knnMatch(da, db, k=2)
    return sum(len(pair) == 2 and pair[0].distance < 0.75 * pair[1].distance for pair in pairs)

def rank(query, candidates, threshold=0.9):
    qhist = histogram(query)
    result = []
    for name, image in candidates:
        correlation = float(cv2.compareHist(qhist, histogram(image), cv2.HISTCMP_CORREL))
        if correlation < threshold:
            continue
        score = float(structural_similarity(query, image, channel_axis=2, data_range=255))
        if score <= 0:
            continue
        result.append({"image": name, "histogram_correlation": correlation,
                       "ssim": score, "sift_matches": int(sift_matches(query, image))})
    return sorted(result, key=lambda row: (-row["sift_matches"], -row["ssim"], row["image"]))

def synthetic_images():
    rng = np.random.default_rng(42)
    cover = rng.integers(0, 256, (100, 100, 3), dtype=np.uint8)
    cv2.rectangle(cover, (10, 10), (90, 90), (230, 180, 50), 3)
    return cover, [("synthetic-identical", cover.copy()),
                   ("synthetic-unrelated", np.full_like(cover, 255))]

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--demo", action="store_true", help="Synthetic offline smoke demo, not a genre benchmark")
    parser.add_argument("--query", type=Path)
    parser.add_argument("--gallery", type=Path)
    parser.add_argument("--threshold", type=float, default=0.9)
    args = parser.parse_args()
    if args.demo:
        query, candidates = synthetic_images()
    elif args.query and args.gallery:
        query = read_image(args.query)
        candidates = [(p.name, read_image(p)) for p in sorted(args.gallery.iterdir())
                      if p.suffix.lower() in {".png", ".jpg", ".jpeg"} and p.resolve() != args.query.resolve()]
        if not candidates:
            parser.error("Gallery has no candidate images")
    else:
        parser.error("Use --demo or both --query and --gallery")
    print(json.dumps({"synthetic": args.demo, "matches": rank(query, candidates, args.threshold)}, indent=2))

if __name__ == "__main__":
    main()
