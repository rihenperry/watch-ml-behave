import os

# settings.py
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

# OR, the same with increased verbosity:
load_dotenv(verbose=True)

# OR, explicitly providing path to '.env'
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# set ROOT_DIR or base directory
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# set upload folder
UPLOAD_FOLDER = os.path.join(ROOT_DIR, 'neuralnet/downloads/imgdata/')
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
