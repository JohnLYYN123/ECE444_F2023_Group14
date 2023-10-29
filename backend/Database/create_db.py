from backend.backend import app, db

with app.app_context():
    # create the database and the db table
    db.create_all()

    # commit the changes
    db.session.commit()



