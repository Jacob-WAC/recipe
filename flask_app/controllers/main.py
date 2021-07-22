from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.recipes import Recipe
from flask_app.controllers import login


@app.route('/dashboard')
def success():
    if 'user_id' not in session:
        return redirect('/')

    recipes = Recipe.get_all()

    return render_template('index.html', recipes=recipes)


@app.route('/recipe/create')
def add():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('add_data.html')


@app.route('/create_recipe', methods=['POST'])
def create_recipe():

    if not Recipe.validate_recipe(request.form):
        return redirect('/recipe/create')

    data = {
        'name': request.form['name'],
        'description': request.form['description'],
        'instructions': request.form['instructions'],
        'date_made_on': request.form['date_made_on'],
        'under_30_min': request.form['under_30_min'],
        'users_id': session['user_id']
    }
    print(data['date_made_on'])
    Recipe.save(data)

    return redirect('/dashboard')


@app.route('/view_recipe/<int:recipe_id>')
def view(recipe_id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': recipe_id
    }
    recipe = Recipe.get_recipe_by_id(data)
    return render_template('display_data.html', recipe=recipe)


@app.route('/Edit_recipe/<int:recipe_id>')
def edit_recipe(recipe_id):
    if 'user_id' not in session:
        return redirect('/')

    data = {
        'id': recipe_id
    }
    recipe = Recipe.get_recipe_by_id(data)

    return render_template('edit_data.html', recipe=recipe)


@app.route('/make_edit/<int:recipe_id>', methods=['POST'])
def edit(recipe_id):
    if not Recipe.validate_recipe(request.form):
        return redirect('/recipe/create')

    data = {
        'id': recipe_id,
        'name': request.form['name'],
        'description': request.form['description'],
        'instructions': request.form['instructions'],
        'date_made_on': request.form['date_made_on'],
        'under_30_min': request.form['under_30_min'],
        'users_id': session['user_id']
    }

    Recipe.update(data)
    return redirect('/dashboard')


@app.route('/delete/<int:recipe_id>')
def delete(recipe_id):

    data = {
        'id': recipe_id
    }

    Recipe.delete(data)
    return redirect('/dashboard')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
