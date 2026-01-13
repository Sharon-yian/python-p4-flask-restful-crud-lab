from flask import Flask, jsonify, request
from flask_migrate import Migrate
from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/plants', methods=['GET'])
def get_plants():
    plants = Plant.query.all()
    return jsonify([plant.to_dict() for plant in plants])

@app.route('/plants/<int:id>', methods=['GET'])
def get_plant(id):
    plant = Plant.query.get_or_404(id)
    return jsonify(plant.to_dict())

@app.route('/plants', methods=['POST'])
def create_plant():
    data = request.get_json()
    plant = Plant(
        name=data['name'],
        image=data['image'],
        price=data['price'],
        is_in_stock=data.get('is_in_stock', True)
    )
    db.session.add(plant)
    db.session.commit()
    return jsonify(plant.to_dict()), 201

@app.route('/plants/<int:id>', methods=['PATCH'])
def update_plant(id):
    plant = Plant.query.get_or_404(id)
    data = request.get_json()
    
    for key, value in data.items():
        if hasattr(plant, key):
            setattr(plant, key, value)
    
    db.session.commit()
    return jsonify(plant.to_dict())

@app.route('/plants/<int:id>', methods=['DELETE'])
def delete_plant(id):
    plant = Plant.query.get_or_404(id)
    db.session.delete(plant)
    db.session.commit()
    return '', 204

@app.route('/')
def home():
    return 'Plant Store API'

if __name__ == '__main__':
    app.run(port=5555, debug=True)
