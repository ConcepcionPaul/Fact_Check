import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
from src.fake_news_detector import main
if __name__ == '__main__':1
    import sys as _sys
    _sys.argv = [_sys.argv[0], '--cli']
    main()
