"""Entry point used by Replit's Run button.

Runs any pending database migrations before starting the dev server,
since (unlike a plain script project) this app ships with a database
that needs to be created/updated on first boot.
"""
import os

from flask_migrate import upgrade

from blog import app

if __name__ == "__main__":
    with app.app_context():
        upgrade()

    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
