import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
MODELS_DIR = os.path.join(BASE_DIR, 'models')
LOGS_DIR = os.path.join(BASE_DIR, 'logs')
SCRAPED_DIR = os.path.join(BASE_DIR, 'scraped')
CONFIG_DIR = os.path.join(BASE_DIR, 'config')

DEFAULT_SEEDS = [42, 99]
DEFAULT_TRAIN_TEST_SPLIT = 0.8
MIN_VOCAB_FREQ = 1
STOPWORDS_FILE = os.path.join(DATA_DIR, 'stopwords.csv')

USER_LOG = os.path.join(LOGS_DIR, 'user_inputs.csv')
SCRAPED_LOG = os.path.join(LOGS_DIR, 'scraped_log.csv')
METRICS_HISTORY = os.path.join(LOGS_DIR, 'metrics_history.csv')
TRAINING_LOG = os.path.join(LOGS_DIR, 'training_log.csv')

for d in [DATA_DIR, MODELS_DIR, LOGS_DIR, SCRAPED_DIR, CONFIG_DIR]:
    os.makedirs(d, exist_ok=True)
