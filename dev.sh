# how this script works
# https://stackoverflow.com/a/52033580/8133924

cd ~/p/manga-updater
source backend/.venv/bin/activate

(trap 'kill 0' SIGINT; PORT=7777 node ~/w/cors-anywhere/server.js & cd backend; python main.py & wait)
