# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.users import User
from flask import flash
# model the class after the friend table from our database


class Recipe:
    def __init__(self, data):
        # place holder data
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_made_on = data['date_made_on']
        self.under_30_min = data['under_30_min']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.users_id = data['users_id']
        self.user = None
    # Now we use class methods to query our database

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes LEFT JOIN users ON recipes.users_id = users.id;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL("recipes").query_db(query)
        # Create an empty list to append our instances of friends
        User_recipes = []
        # Iterate over the db results and create instances of friends with cls.

        for item in results:
            recipe = Recipe(item)
            user = {
                'id': item['users.id'],
                'first_name': item['first_name'],
                'last_name': item['last_name'],
                'email': item['email'],
                'password': item['password'],
                'address': item['address'],
                'city': item['city'],
                'state': item['state'],
                'zip': item['zip'],
                'subscription': item['subscription'],
                'created_at': item['users.created_at'],
                'updated_at': item['users.updated_at']
            }
            recipe.user = User(user)
            User_recipes.append(recipe)

        return User_recipes

    @classmethod
    def get_recipe_by_id(cls, data):

        query = "SELECT * FROM recipes LEFT JOIN users ON recipes.users_id = users.id WHERE recipes.id = %(id)s;"

        results = connectToMySQL("recipes").query_db(query, data)
        # Create an empty list to append our instances of friends
        User_recipes = []
        # Iterate over the db results and create instances of friends with cls.

        for item in results:
            recipe = Recipe(item)
            user = {
                'id': item['users.id'],
                'first_name': item['first_name'],
                'last_name': item['last_name'],
                'email': item['email'],
                'password': item['password'],
                'address': item['address'],
                'city': item['city'],
                'state': item['state'],
                'zip': item['zip'],
                'subscription': item['subscription'],
                'created_at': item['users.created_at'],
                'updated_at': item['users.updated_at']
            }
            recipe.user = User(user)
            User_recipes.append(recipe)

        return User_recipes[0]

    @classmethod
    def save(cls, data):
        query = "INSERT INTO recipes (name , description , instructions, date_made_on, under_30_min, users_id) VALUES (%(name)s , %(description)s , %(instructions)s, %(date_made_on)s, %(under_30_min)s, %(users_id)s);"
        return connectToMySQL('recipes').query_db(query, data)

    @classmethod
    def update(cls, data):
        query = "UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, date_made_on = %(date_made_on)s, under_30_min = %(under_30_min)s WHERE id = %(id)s;"

        connectToMySQL('recipes').query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"

        connectToMySQL('recipes').query_db(query, data)

    @staticmethod
    def validate_recipe(data):
        is_valid = True

        if len(data['name']) < 3:
            flash('name must be at least 3 character!', 'name')
            is_valid = False

        if len(data['description']) < 3:
            flash('description must be at least 3 character!', 'description')
            is_valid = False

        if len(data['instructions']) < 3:
            flash(
                "instructions must be at least 3 character!", "instructions")
            is_valid = False

        if len(data['date_made_on']) < 1:
            flash('please pick a date!', 'date_made_on')
            is_valid = False

        return is_valid
