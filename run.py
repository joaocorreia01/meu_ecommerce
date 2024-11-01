import sys
sys.path.append('/mnt/c/Users/João\ Victor/engsoft_ic/')  # Ajuste conforme necessário
from loja import app


if __name__ == "__main__":
    app.run(debug=True)