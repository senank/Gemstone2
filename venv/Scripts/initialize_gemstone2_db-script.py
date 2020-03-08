#!c:\users\user\senan\gemstone2\venv\scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'gemstone2','console_scripts','initialize_gemstone2_db'
__requires__ = 'gemstone2'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('gemstone2', 'console_scripts', 'initialize_gemstone2_db')()
    )
