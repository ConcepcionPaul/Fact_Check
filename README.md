# Fact_Check (PAK CHECKER)

A small fact-checking app that can:

- Train a Naive Bayes model using a bag-of-words vocabulary
- Evaluate the model
- Classify new news from:
  - manual text (title + body)
  - a URL (scraping)
  - an image (OCR)
- Batch classify from a CSV
- Scrape multiple URLs and store results

## Requirements

- Python 3.9+

Install dependencies:

```bash
pip install -r requirements.txt
```

> Note: The OCR part uses **Tesseract** (`pytesseract`). Ensure Tesseract is installed on your system.

## Project structure (high level)

- `run_cli.py` / `run_gui.py`: entry points
- `src/cli.py`: CLI menu
- `src/gui.py`: Tkinter GUI
- `src/fake_news_detector.py`: chooses CLI vs GUI based on `--cli/--gui`
- `src/training.py`: training logic
- `src/evaluation.py`: evaluation logic
- `src/verifier.py`: verifies/classifies an input (optionally across multiple seeds)
- `src/scraper.py`: scraping helpers
- `src/ocr_reader.py`: OCR extraction

## How to run

### Option A: CLI

From the repo root:

```bash
python run_cli.py
```

You’ll see a menu with options like:

- Train model
- Evaluate model
- Classify new article (manual / URL / image)
- Batch classify from CSV
- Scrape news (multiple URLs)
- Export Bag-of-Words CSV for last seed
- Reload stopwords

### Option B: GUI

```bash
python run_gui.py
```

Tabs:

- **Detect News**: classify text / URL / image (OCR)
- **Scraping**: paste URLs and scrape into `data/true.csv` or `data/false.csv`
- **Training & Settings**: train/retrain, evaluate, export vocabulary, reload stopwords

### Option C: Single entry via arguments

```bash
python -m src.fake_news_detector --cli
python -m src.fake_news_detector --gui
```

(If your Python import path differs, use `run_cli.py` / `run_gui.py` instead.)

## Classify examples

### 1) Manual text classification (CLI)

In the CLI menu:

1. Choose `3) Classify new article`
2. Select mode `1) manual`
3. Enter title and text

The app will only mark results **CONFIDENT** when models agree across configured seeds.

### 2) URL classification (CLI)

In the CLI menu:

- Choose `3) Classify new article`
- Select mode `2) URL`

### 3) Image classification (OCR)

- Choose `3) Classify new article`
- Select mode `3) image`
- Select an image file (`.png/.jpg/.jpeg/.bmp`)

## Data files

The app uses the following CSVs:

- `data/true.csv`
- `data/false.csv`
- `data/stopwords.csv`

It also writes logs into:

- `logs/user_inputs.csv`
- `logs/scraped_log.csv`
- `logs/metrics_history.csv`
- `logs/training_log.csv`

## Notes / troubleshooting

- If OCR fails:
  - confirm Tesseract is installed
  - make sure `pytesseract` can find the Tesseract executable
- If you see missing-model/vocabulary errors:
  - run **Train model** first (CLI menu option `1` or GUI training tab)

## License

Add your license here.

