from flask import Blueprint, request, jsonify
from src.models.user import db, User
from src.models.order import Order, OrderItem, CartItem
from src.models.house_plan import HousePlan
from sqlalchemy import and_

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/cart', methods=['GET'])
def get_cart():
    """Get user's cart items"""
    try:
        # TODO: Get user_id from authentication
        user_id = request.args.get('user_id', 1, type=int)
        
        cart_items = CartItem.query.filter_by(user_id=user_id).all()
        
        total_amount = sum(item.plan.price * item.quantity for item in cart_items if item.plan)
        
        return jsonify({
            'success': True,
            'data': {
                'items': [item.to_dict() for item in cart_items],
                'total_amount': total_amount,
                'item_count': len(cart_items)
            }
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@cart_bp.route('/cart/add', methods=['POST'])
def add_to_cart():
    """Add item to cart"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if 'plan_id' not in data:
            return jsonify({'success': False, 'error': 'Plan ID is required'}), 400
        
        # TODO: Get user_id from authentication
        user_id = data.get('user_id', 1)
        plan_id = data['plan_id']
        quantity = data.get('quantity', 1)
        
        # Check if plan exists
        plan = HousePlan.query.filter_by(id=plan_id, is_active=True).first()
        if not plan:
            return jsonify({'success': False, 'error': 'House plan not found'}), 404
        
        # Check if item already in cart
        existing_item = CartItem.query.filter_by(user_id=user_id, plan_id=plan_id).first()
        
        if existing_item:
            # Update quantity
            existing_item.quantity += quantity
            db.session.commit()
            cart_item = existing_item
        else:
            # Create new cart item
            cart_item = CartItem(
                user_id=user_id,
                plan_id=plan_id,
                quantity=quantity
            )
            db.session.add(cart_item)
            db.session.commit()
        
        return jsonify({
            'success': True,
            'data': cart_item.to_dict(),
            'message': 'Item added to cart successfully'
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@cart_bp.route('/cart/update/<int:item_id>', methods=['PUT'])
def update_cart_item(item_id):
    """Update cart item quantity"""
    try:
        data = request.get_json()
        
        if 'quantity' not in data:
            return jsonify({'success': False, 'error': 'Quantity is required'}), 400
        
        cart_item = CartItem.query.get(item_id)
        if not cart_item:
            return jsonify({'success': False, 'error': 'Cart item not found'}), 404
        
        quantity = data['quantity']
        
        if quantity <= 0:
            # Remove item if quantity is 0 or negative
            db.session.delete(cart_item)
        else:
            cart_item.quantity = quantity
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': cart_item.to_dict() if quantity > 0 else None,
            'message': 'Cart item updated successfully'
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@cart_bp.route('/cart/remove/<int:item_id>', methods=['DELETE'])
def remove_from_cart(item_id):
    """Remove item from cart"""
    try:
        cart_item = CartItem.query.get(item_id)
        if not cart_item:
            return jsonify({'success': False, 'error': 'Cart item not found'}), 404
        
        db.session.delete(cart_item)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Item removed from cart successfully'
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@cart_bp.route('/cart/clear', methods=['DELETE'])
def clear_cart():
    """Clear all items from cart"""
    try:
        # TODO: Get user_id from authentication
        user_id = request.args.get('user_id', 1, type=int)
        
        CartItem.query.filter_by(user_id=user_id).delete()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Cart cleared successfully'
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@cart_bp.route('/orders', methods=['GET'])
def get_orders():
    """Get user's orders"""
    try:
        # TODO: Get user_id from authentication
        user_id = request.args.get('user_id', 1, type=int)
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        pagination = Order.query.filter_by(user_id=user_id)\
                               .order_by(Order.created_at.desc())\
                               .paginate(page=page, per_page=per_page, error_out=False)
        
        orders = pagination.items
        
        return jsonify({
            'success': True,
            'data': [order.to_dict() for order in orders],
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

@cart_bp.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    """Get specific order details"""
    try:
        order = Order.query.get(order_id)
        if not order:
            return jsonify({'success': False, 'error': 'Order not found'}), 404
        
        return jsonify({
            'success': True,
            'data': order.to_dict()
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@cart_bp.route('/orders', methods=['POST'])
def create_order():
    """Create order from cart"""
    try:
        data = request.get_json()
        
        # TODO: Get user_id from authentication
        user_id = data.get('user_id', 1)
        
        # Get cart items
        cart_items = CartItem.query.filter_by(user_id=user_id).all()
        
        if not cart_items:
            return jsonify({'success': False, 'error': 'Cart is empty'}), 400
        
        # Calculate total amount
        total_amount = sum(item.plan.price * item.quantity for item in cart_items if item.plan)
        
        # Create order
        order = Order(
            user_id=user_id,
            total_amount=total_amount,
            status='pending'
        )
        
        # Set billing address if provided
        if 'billing_address' in data:
            order.set_billing_address(data['billing_address'])
        
        db.session.add(order)
        db.session.flush()  # Get order ID
        
        # Create order items
        for cart_item in cart_items:
            order_item = OrderItem(
                order_id=order.id,
                plan_id=cart_item.plan_id,
                quantity=cart_item.quantity,
                unit_price=cart_item.plan.price,
                total_price=cart_item.plan.price * cart_item.quantity
            )
            db.session.add(order_item)
        
        # Clear cart
        CartItem.query.filter_by(user_id=user_id).delete()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': order.to_dict(),
            'message': 'Order created successfully'
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@cart_bp.route('/orders/<int:order_id>/status', methods=['PUT'])
def update_order_status(order_id):
    """Update order status (Admin only)"""
    try:
        data = request.get_json()
        
        if 'status' not in data:
            return jsonify({'success': False, 'error': 'Status is required'}), 400
        
        order = Order.query.get(order_id)
        if not order:
            return jsonify({'success': False, 'error': 'Order not found'}), 404
        
        valid_statuses = ['pending', 'paid', 'completed', 'cancelled']
        if data['status'] not in valid_statuses:
            return jsonify({'success': False, 'error': 'Invalid status'}), 400
        
        order.status = data['status']
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': order.to_dict(),
            'message': 'Order status updated successfully'
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@cart_bp.route('/checkout/summary', methods=['POST'])
def get_checkout_summary():
    """Get checkout summary"""
    try:
        data = request.get_json()
        
        # TODO: Get user_id from authentication
        user_id = data.get('user_id', 1)
        
        # Get cart items
        cart_items = CartItem.query.filter_by(user_id=user_id).all()
        
        if not cart_items:
            return jsonify({'success': False, 'error': 'Cart is empty'}), 400
        
        # Calculate totals
        subtotal = sum(item.plan.price * item.quantity for item in cart_items if item.plan)
        tax_rate = 0.15  # 15% VAT in South Africa
        tax_amount = subtotal * tax_rate
        total_amount = subtotal + tax_amount
        
        return jsonify({
            'success': True,
            'data': {
                'items': [item.to_dict() for item in cart_items],
                'subtotal': subtotal,
                'tax_rate': tax_rate,
                'tax_amount': tax_amount,
                'total_amount': total_amount,
                'currency': 'ZAR'
            }
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

