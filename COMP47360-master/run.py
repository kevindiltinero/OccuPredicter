from app import app
from werkzeug.serving import run_simple
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
run_simple("0.0.0.0", 5050, app,  use_debugger=True)
