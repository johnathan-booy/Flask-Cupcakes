from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)
    app.app_context().push()


class Cupcake(db.Model):
    """Cupcake Model
        id: a unique primary key that is an auto-incrementing integer
        flavor: a not-nullable text column
        size: a not-nullable text column
        rating: a not-nullable column that is a float
        image: a non-nullable text column. If an image is not given, default to https://tinyurl.com/demo-cupcake"""

    __tablename__ = 'cupcakes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    flavor = db.Column(db.Text, nullable=False)
    size = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    image = db.Column(db.Text, nullable=False,
                      default='https://tinyurl.com/demo-cupcake')

    def serialize(self):
        """Serialize a cupcake model to dictionary"""
        c = self
        return {"id": c.id, "flavor": c.flavor, "size": c.size, "rating": c.rating, "image": c.image}
