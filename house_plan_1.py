from src.models.user import db
from datetime import datetime
import json

# Association table for many-to-many relationship between plans and categories
plan_categories = db.Table('plan_categories',
    db.Column('plan_id', db.Integer, db.ForeignKey('house_plan.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('category.id'), primary_key=True)
)

class HousePlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    bedrooms = db.Column(db.Integer, nullable=False)
    bathrooms = db.Column(db.Float, nullable=False)
    stories = db.Column(db.Integer, nullable=False)
    garage_spaces = db.Column(db.Integer, default=0)
    square_footage = db.Column(db.Integer, nullable=False)
    style_category = db.Column(db.String(100), nullable=False)
    featured_image_url = db.Column(db.String(500))
    gallery_images = db.Column(db.Text)  # JSON string of image URLs
    plan_files = db.Column(db.Text)  # JSON string of file URLs (PDF, DWG)
    is_featured = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Relationships
    categories = db.relationship('Category', secondary=plan_categories, lazy='subquery',
                               backref=db.backref('plans', lazy=True))
    creator = db.relationship('User', backref=db.backref('created_plans', lazy=True))
    
    def __repr__(self):
        return f'<HousePlan {self.title}>'
    
    def get_gallery_images(self):
        """Parse gallery images JSON string"""
        if self.gallery_images:
            try:
                return json.loads(self.gallery_images)
            except json.JSONDecodeError:
                return []
        return []
    
    def set_gallery_images(self, images_list):
        """Set gallery images as JSON string"""
        self.gallery_images = json.dumps(images_list)
    
    def get_plan_files(self):
        """Parse plan files JSON string"""
        if self.plan_files:
            try:
                return json.loads(self.plan_files)
            except json.JSONDecodeError:
                return []
        return []
    
    def set_plan_files(self, files_list):
        """Set plan files as JSON string"""
        self.plan_files = json.dumps(files_list)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'bedrooms': self.bedrooms,
            'bathrooms': self.bathrooms,
            'stories': self.stories,
            'garage_spaces': self.garage_spaces,
            'square_footage': self.square_footage,
            'style_category': self.style_category,
            'featured_image_url': self.featured_image_url,
            'gallery_images': self.get_gallery_images(),
            'plan_files': self.get_plan_files(),
            'is_featured': self.is_featured,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'categories': [cat.to_dict() for cat in self.categories],
            'creator': self.creator.to_dict() if self.creator else None
        }

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(500))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Category {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'description': self.description,
            'image_url': self.image_url,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'plan_count': len(self.plans) if hasattr(self, 'plans') else 0
        }

