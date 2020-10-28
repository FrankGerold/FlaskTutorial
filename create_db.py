from project.app import db


# Create DB and table
db.create_all()


# Commit changes
db.session.commit()
