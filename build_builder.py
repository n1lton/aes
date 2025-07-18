import os

#  --noconsole
os.system("py -m PyInstaller -F -w -c -n=AESbuilder --noconsole --add-data main.py;. --add-data logo.png;. --hiddenimport PyInstaller --paths venv/Lib/site-packages --add-data logo.ico;. --add-data consola.ttf;. --add-data style.css;. --onefile --icon logo.ico builder2.py")
