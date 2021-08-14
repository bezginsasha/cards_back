from flask import Flask
from views.auth import auth_bp
from views.cards import cards_bp
from views.piles import piles_bp

app = Flask(__name__)
app.register_blueprint(auth_bp)
app.register_blueprint(cards_bp)
app.register_blueprint(piles_bp)
