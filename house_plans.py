from flask import Blueprint, request, jsonify
from src.models.user import db
from src.models.house_plan import HousePlan, Category
from sqlalchemy import or_, and_
import os
from werkzeug.utils import secure_filename

house_plans_bp = Blueprint('house_plans', __name__)

# Allowed file extensions for uploads
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'dwg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@house_plans_bp.route('/house-plans', methods=['GET'])
def get_house_plans():
    """Get all house plans with optional filtering"""
    try:
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 12, type=int)
        search = request.args.get('search', '')
        category = request.args.get('category', '')
        style = request.args.get('style', '')
        min_price = request.args.get('min_price', type=float)
        max_price = request.args.get('max_price', type=float)
        bedrooms = request.args.get('bedrooms', type=int)
        bathrooms = request.args.get('bathrooms', type=float)
        featured_only = request.args.get('featured', 'false').lower() == 'true'
        
        # Build query
        query = HousePlan.query.filter(HousePlan.is_active == True)
        
        # Apply filters
        if search:
            query = query.filter(or_(
                HousePlan.title.contains(search),
                HousePlan.description.contains(search),
                HousePlan.style_category.contains(search)
            ))
        
        if category:
            query = query.join(HousePlan.categories).filter(Category.slug == category)
        
        if style:
            query = query.filter(HousePlan.style_category.ilike(f'%{style}%'))
        
        if min_price is not None:
            query = query.filter(HousePlan.price >= min_price)
        
        if max_price is not None:
            query = query.filter(HousePlan.price <= max_price)
        
        if bedrooms is not None:
            query = query.filter(HousePlan.bedrooms == bedrooms)
        
        if bathrooms is not None:
            query = query.filter(HousePlan.bathrooms == bathrooms)
        
        if featured_only:
            query = query.filter(HousePlan.is_featured == True)
        
        # Order by featured first, then by created date
        query = query.order_by(HousePlan.is_featured.desc(), HousePlan.created_at.desc())
        
        # Paginate
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        plans = pagination.items
        
        return jsonify({
            'success': True,
            'data': [plan.to_dict() for plan in plans],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': pagination.total,
                'pages': pagination.pages,
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev
            }
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@house_plans_bp.route('/house-plans/<int:plan_id>', methods=['GET'])
def get_house_plan(plan_id):
    """Get a specific house plan by ID"""
    try:
        plan = HousePlan.query.filter_by(id=plan_id, is_active=True).first()
        if not plan:
            return jsonify({'success': False, 'error': 'House plan not found'}), 404
        
        return jsonify({
            'success': True,
            'data': plan.to_dict()
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@house_plans_bp.route('/house-plans', methods=['POST'])
def create_house_plan():
    """Create a new house plan (Admin only)"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['title', 'description', 'price', 'bedrooms', 'bathrooms', 'stories', 'square_footage', 'style_category']
        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'error': f'Missing required field: {field}'}), 400
        
        # Create new house plan
        plan = HousePlan(
            title=data['title'],
            description=data['description'],
            price=data['price'],
            bedrooms=data['bedrooms'],
            bathrooms=data['bathrooms'],
            stories=data['stories'],
            garage_spaces=data.get('garage_spaces', 0),
            square_footage=data['square_footage'],
            style_category=data['style_category'],
            featured_image_url=data.get('featured_image_url'),
            is_featured=data.get('is_featured', False),
            created_by=1  # TODO: Get from authenticated user
        )
        
        # Set gallery images and plan files if provided
        if 'gallery_images' in data:
            plan.set_gallery_images(data['gallery_images'])
        
        if 'plan_files' in data:
            plan.set_plan_files(data['plan_files'])
        
        db.session.add(plan)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': plan.to_dict(),
            'message': 'House plan created successfully'
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@house_plans_bp.route('/house-plans/<int:plan_id>', methods=['PUT'])
def update_house_plan(plan_id):
    """Update a house plan (Admin only)"""
    try:
        plan = HousePlan.query.get(plan_id)
        if not plan:
            return jsonify({'success': False, 'error': 'House plan not found'}), 404
        
        data = request.get_json()
        
        # Update fields
        updatable_fields = ['title', 'description', 'price', 'bedrooms', 'bathrooms', 'stories', 
                           'garage_spaces', 'square_footage', 'style_category', 'featured_image_url', 
                           'is_featured', 'is_active']
        
        for field in updatable_fields:
            if field in data:
                setattr(plan, field, data[field])
        
        # Update gallery images and plan files if provided
        if 'gallery_images' in data:
            plan.set_gallery_images(data['gallery_images'])
        
        if 'plan_files' in data:
            plan.set_plan_files(data['plan_files'])
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': plan.to_dict(),
            'message': 'House plan updated successfully'
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@house_plans_bp.route('/house-plans/<int:plan_id>', methods=['DELETE'])
def delete_house_plan(plan_id):
    """Delete a house plan (Admin only)"""
    try:
        plan = HousePlan.query.get(plan_id)
        if not plan:
            return jsonify({'success': False, 'error': 'House plan not found'}), 404
        
        # Soft delete by setting is_active to False
        plan.is_active = False
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'House plan deleted successfully'
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@house_plans_bp.route('/categories', methods=['GET'])
def get_categories():
    """Get all categories"""
    try:
        categories = Category.query.filter_by(is_active=True).order_by(Category.name).all()
        
        return jsonify({
            'success': True,
            'data': [category.to_dict() for category in categories]
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@house_plans_bp.route('/categories', methods=['POST'])
def create_category():
    """Create a new category (Admin only)"""
    try:
        data = request.get_json()
        
        if 'name' not in data:
            return jsonify({'success': False, 'error': 'Category name is required'}), 400
        
        # Generate slug from name
        slug = data['name'].lower().replace(' ', '-').replace('_', '-')
        
        category = Category(
            name=data['name'],
            slug=slug,
            description=data.get('description'),
            image_url=data.get('image_url')
        )
        
        db.session.add(category)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': category.to_dict(),
            'message': 'Category created successfully'
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@house_plans_bp.route('/featured-plans', methods=['GET'])
def get_featured_plans():
    """Get featured house plans"""
    try:
        limit = request.args.get('limit', 6, type=int)
        
        plans = HousePlan.query.filter_by(is_featured=True, is_active=True)\
                              .order_by(HousePlan.created_at.desc())\
                              .limit(limit).all()
        
        return jsonify({
            'success': True,
            'data': [plan.to_dict() for plan in plans]
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@house_plans_bp.route('/styles', methods=['GET'])
def get_styles():
    """Get all unique style categories"""
    try:
        styles = db.session.query(HousePlan.style_category)\
                          .filter(HousePlan.is_active == True)\
                          .distinct().all()
        
        style_list = [style[0] for style in styles if style[0]]
        
        return jsonify({
            'success': True,
            'data': sorted(style_list)
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

