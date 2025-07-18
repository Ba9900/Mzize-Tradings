import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS

# Import all models to ensure they are registered
from src.models.user import db, User
from src.models.house_plan import HousePlan, Category
from src.models.order import Order, OrderItem, CartItem
from src.models.payment import Payment, PaymentMethod

# Import all routes
from src.routes.user import user_bp
from src.routes.house_plans import house_plans_bp
from src.routes.cart import cart_bp
from src.routes.payments import payments_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# Enable CORS for all routes
CORS(app, origins="*")

# Register blueprints
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(house_plans_bp, url_prefix='/api')
app.register_blueprint(cart_bp, url_prefix='/api')
app.register_blueprint(payments_bp, url_prefix='/api')

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

def init_database():
    """Initialize database with sample data"""
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Check if we need to add sample data
        if User.query.count() == 0:
            # Create admin user
            admin_user = User(
                email='banelemzize@gmail.com',
                first_name='Banele',
                last_name='Mditshwa',
                phone='0792832637',
                is_admin=True
            )
            admin_user.set_password('admin123')
            db.session.add(admin_user)
            db.session.commit()  # Commit admin user first to get ID
            
            # Create sample categories
            categories = [
                Category(name='Modern', slug='modern', description='Contemporary and sleek designs'),
                Category(name='Traditional', slug='traditional', description='Classic and timeless designs'),
                Category(name='Contemporary', slug='contemporary', description='Current and stylish designs'),
                Category(name='Farmhouse', slug='farmhouse', description='Rustic and charming designs'),
                Category(name='Minimalist', slug='minimalist', description='Simple and clean designs'),
                Category(name='Urban', slug='urban', description='City-style compact designs'),
                Category(name='Luxury', slug='luxury', description='High-end and premium designs'),
                Category(name='Cottage', slug='cottage', description='Cozy and intimate designs')
            ]
            
            for category in categories:
                db.session.add(category)
            
            # Create sample house plans
            sample_plans = [
                {
                    'title': 'Modern Family Home',
                    'description': 'Spacious modern family home with open-plan living and contemporary design.',
                    'price': 2500.0,
                    'bedrooms': 4,
                    'bathrooms': 3.0,
                    'stories': 2,
                    'garage_spaces': 2,
                    'square_footage': 2850,
                    'style_category': 'Modern',
                    'featured_image_url': 'https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=500&h=300&fit=crop',
                    'is_featured': True
                },
                {
                    'title': 'Cozy Cottage Design',
                    'description': 'Charming cottage-style home perfect for small families.',
                    'price': 1800.0,
                    'bedrooms': 3,
                    'bathrooms': 2.0,
                    'stories': 1,
                    'garage_spaces': 1,
                    'square_footage': 1650,
                    'style_category': 'Traditional',
                    'featured_image_url': 'https://images.unsplash.com/photo-1600047509807-ba8f99d2cdde?w=500&h=300&fit=crop',
                    'is_featured': True
                },
                {
                    'title': 'Luxury Villa Plan',
                    'description': 'Elegant luxury villa with premium finishes and spacious layouts.',
                    'price': 4200.0,
                    'bedrooms': 5,
                    'bathrooms': 4.0,
                    'stories': 2,
                    'garage_spaces': 3,
                    'square_footage': 4200,
                    'style_category': 'Contemporary',
                    'featured_image_url': 'https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=500&h=300&fit=crop',
                    'is_featured': True
                }
            ]
            
            for plan_data in sample_plans:
                plan = HousePlan(
                    created_by=admin_user.id,
                    **plan_data
                )
                db.session.add(plan)
            
            # Create payment methods
            payment_methods = [
                {
                    'name': 'Credit Card',
                    'code': 'credit_card',
                    'gateway': 'payfast',
                    'description': 'Pay securely with your Visa, Mastercard, or American Express',
                    'display_order': 1,
                    'supported_cards': ['visa', 'mastercard', 'amex']
                },
                {
                    'name': 'EFT Bank Transfer',
                    'code': 'eft_bank',
                    'gateway': 'ozow',
                    'description': 'Instant bank transfer from your South African bank account',
                    'display_order': 2,
                    'supported_banks': ['absa', 'fnb', 'standard_bank', 'nedbank', 'capitec']
                }
            ]
            
            for method_data in payment_methods:
                method = PaymentMethod(**method_data)
                if 'supported_cards' in method_data:
                    method.set_supported_cards(method_data['supported_cards'])
                if 'supported_banks' in method_data:
                    method.set_supported_banks(method_data['supported_banks'])
                db.session.add(method)
            
            db.session.commit()
            print("Database initialized with sample data")

# Initialize database
init_database()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
