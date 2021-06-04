import os
import bottle

os.chdir(os.path.dirname(os.path.abspath(__file__)))

import simple_wol
application = bottle.default_app()
