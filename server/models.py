from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)

db = SQLAlchemy(metadata=metadata)


class Restaurant(db.Model, SerializerMixin):
    __tablename__ = "restaurants"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String)

    restaurant_pizzas = db.relationship('RestaurantPizza', back_populates='restaurant', cascade="all, delete-orphan")

    pizzas =association_proxy('restaurant_pizzas', 'pizza')
    
    serialize_rules=['-restaurant_pizza.restaurant',]

    def __repr__(self):
        return f"<Restaurant {self.name}>"



class RestaurantPizza(db.Model, SerializerMixin):
    __tablename__ = "restaurant_pizzas"

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)
    restaurant_id=db.Column(db.Integer, db.ForeignKey('restaurants.id'))
    pizza_id=db.Column(db.Integer, db.ForeignKey('pizzas.id'))
    
    restaurant = db.relationship('Restaurant', back_populates='restaurant_pizzas', cascade='all, delete')
    pizza = db.relationship('Pizza', back_populates='restaurant_pizzas', cascade='all, delete')
    
    serialize_rules=('-pizza.restaurant_pizzas', '-restaurant.restaurant_pizzas')

    @validates('price')
    def validate_price(self, key, value):
        if 1 <= value <= 30:
            return value
        else:
            raise ValueError("Must have a price between 1 and 30")
    
    def __repr__(self):
        return f"<RestaurantPizza ${self.price}>"
    
class Pizza(db.Model, SerializerMixin):
        __tablename__ = "pizzas"

        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String)
        ingredients = db.Column(db.String)

        restaurant_pizzas = db.relationship('RestaurantPizza', back_populates='pizza', cascade="all, delete-orphan")

        pizzas = association_proxy('restaurant_pizzas', 'restaurant')

        serialize_rules=['-restaurant_pizza']

        def __repr__(self):
            return f"<Pizza {self.name}, {self.ingredients}>"
