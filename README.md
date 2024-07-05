# Judging a Book by Its Cover

An academic computer-vision project exploring book-cover similarity and genre inference. The original notebook uses a three-stage retrieval pipeline: RGB histograms, structural similarity (SSIM), and SIFT feature matching. Original code, proposal, report and related paper are preserved.

## Run an offline demonstration

Use Python 3.12, from the repository root:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt
python cover_match.py --demo
python -m pytest -q
```

This runs a deterministic **synthetic smoke demo**, not a trained classifier or an accuracy benchmark. An identical patterned image should be ranked first with SSIM 1.0. No book images or external service is downloaded.

For images you have permission to use:

```bash
python cover_match.py --query /path/query.jpg --gallery /path/gallery
```

The gallery accepts JPG/JPEG/PNG files. The query itself is excluded when it is the same file. Output is JSON containing histogram correlation, SSIM and SIFT match counts. Empty matches are possible with the default histogram threshold of 0.9; use `--threshold 0.5` to explore less selective retrieval. These scores are similarity measures, not probabilities or genre confidence.

## How the runnable adaptation differs

`cover_match.py` extracts the original notebook's approach into a local-image CLI. It normalizes images to 100×100, handles RGB SSIM explicitly, handles missing SIFT descriptors and incomplete match pairs, and uses exact brute-force matching rather than the notebook's FLANN configuration. It does not reproduce the full notebook experiment or infer genre from synthetic examples.

## Original research material

- `Codes/judgingABookCode.ipynb`: original exploratory workflow, retained unchanged
- `Codes/shortbook.csv`: headerless book metadata with image URLs, title, author, class and genre
- `Judging_A_Book_By_It_s_Cover.pdf`: project report
- `proposal/`: original project proposal
- `Related paper/`: reference material

The notebook requires further packages (`pandas`, `matplotlib`, `scikit-learn`, `requests`, `Pillow`, `imutils`, Jupyter) and live external image URLs. Do not blindly run all cells: URLs may fail, some cells assume at least 39 predictions or 500 descriptor matches, and loading pickle files is unsafe unless they are trusted. Read the CSV with `header=None` to avoid discarding its first book. Cached notebook outputs are historical, not revalidated results.

## Limitations and honest presentation

The notebook's single-example “Accuracy is 100%” output is not dataset-level accuracy. Cover similarity need not predict genre; colour/layout bias and duplicate covers can distort evaluation. A proper genre benchmark needs an independently held-out, deduplicated labeled dataset and aggregate metrics. The runnable CLI verifies retrieval mechanics only. The full external-image notebook experiment has not been rerun.

For an interview: explain the three stages, run the synthetic smoke demo, then try a small authorized local gallery and discuss failure cases. Cite the existing report and authors rather than claiming this cleanup as new research. Dataset/image redistribution rights and a repository license have not been established here; no license is added by this maintenance work.

## Container recipe

```bash
docker build -t portfolio-demo .
docker run --rm --network none portfolio-demo
```

This recipe runs the offline demo and component tests as an unprivileged user. Docker was unavailable in the maintenance environment, so this container recipe is provided but not claimed as executed. The commands were verified in a dedicated Python virtual environment instead.
