#!/usr/bin/python3
import os
from api import create_app, db

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        if app.config['USE_DATABASE'] and os.environ.get('DATABASE_TYPE') == 'sqlite':
            db.create_all()
    app.run(debug=True)