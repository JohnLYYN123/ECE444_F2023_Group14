from main import *

with app.app_context():
    # create the database and the db table
    db1.create_all()
    # commit the changes
    db1.session.commit()
