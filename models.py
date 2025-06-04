from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

# Association table for Recipe-Ingredient relationship with quantities
recipe_ingredients = Table(
    'recipe_ingredients',
    Base.metadata,
    Column('recipe_id', Integer, ForeignKey('recipes.id')),
    Column('ingredient_id', Integer, ForeignKey('ingredients.id')),
    Column('required_quantity', Float),
    Column('required_unit', String(20))
)

class Ingredient(Base):
    __tablename__ = 'ingredients'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    quantity = Column(Float)
    unit = Column(String(20))
    recipes = relationship("Recipe", secondary=recipe_ingredients, back_populates="ingredients")

class Recipe(Base):
    __tablename__ = 'recipes'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    cuisine_type = Column(String(50))
    preparation_time = Column(Integer)  # in minutes
    cooking_steps = Column(String(2000))  # JSON string of steps
    ingredients = relationship("Ingredient", secondary=recipe_ingredients, back_populates="recipes")
    description = Column(String(500))  # Brief description of the recipe
    difficulty_level = Column(String(20))  # Easy, Medium, Hard
    serving_size = Column(Integer)  # Number of servings

# Create database
engine = create_engine('sqlite:///cooking_assistant.db')
Base.metadata.create_all(engine) 