import sys
sys.path.append('/')  # Ajuste conforme necessário
from loja import app



if __name__ == "__main__":
    app.run(debug=True)