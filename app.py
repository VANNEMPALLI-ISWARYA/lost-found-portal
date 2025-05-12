# Import necessary libraries from Flask
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

# Initialize the Flask application
app = Flask(__name__)

# Configure the SQLite database file (will be created automatically)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database object
db = SQLAlchemy(app)

# Define a database model for lost/found items
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unique ID for each item
    item_name = db.Column(db.String(100), nullable=False)  # Name of the item
    description = db.Column(db.String(200), nullable=False)  # Description of the item
    contact = db.Column(db.String(100), nullable=False)  # Contact info of the person
    status = db.Column(db.String(10), nullable=False)  # 'lost' or 'found'

# Route: Home Page
@app.route('/')
def home():
    return render_template('index.html')

# Route: Report Page (GET to show form, POST to handle form submission)
@app.route('/report', methods=['GET', 'POST'])
def report():
    if request.method == 'POST':
        # Get form data submitted by the user
        item_name = request.form['item_name']
        description = request.form['description']
        contact = request.form['contact']
        status = request.form['status']

        # Create a new Item object with the form data
        new_item = Item(item_name=item_name, description=description, contact=contact, status=status)
        
        # Add the new item to the database and commit (save)
        db.session.add(new_item)
        db.session.commit()

        # Redirect to the view page after submission
        return redirect('/view')
    
    # If the method is GET, just show the form
    return render_template('report.html')

# Route: View all reported items
@app.route('/view')
def view():
    # Query all items from the database
    items = Item.query.all()
    
    # Pass the items to the view template
    return render_template('view_items.html', items=items)

# Run the app
if __name__ == '__main__':
    # Create the database tables if they don't already exist
    with app.app_context():
        db.create_all()
    
    # Start the Flask web server
    app.run(debug=True)
