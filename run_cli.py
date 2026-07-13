import sys
import os

# Ensure `src/` is importable when running from repo root
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from src.fake_news_detector import main


if __name__ == "__main__":
    sys.argv = [sys.argv[0], "--cli"]
    main()

