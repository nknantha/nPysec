"""
A helper to create tables on database.
"""
if __name__ == "__main__":
    from . import create_app
    from .models import db
    
    db.create_all(app=create_app())
