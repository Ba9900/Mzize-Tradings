from src.models.user import db
from datetime import datetime
import json
import uuid

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(50), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(50), default='pending')  # pending, paid, completed, cancelled
    total_amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(100))
    payment_reference = db.Column(db.String(200))
    billing_address = db.Column(db.Text)  # JSON string
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref=db.backref('orders', lazy=True))
    items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')
    
    def __init__(self, **kwargs):
        super(Order, self).__init__(**kwargs)
        if not self.order_number:
            self.order_number = self.generate_order_number()
    
    @staticmethod
    def generate_order_number():
        """Generate a unique order number"""
        return f"MZ{datetime.now().strftime('%Y%m%d')}{str(uuid.uuid4())[:8].upper()}"
    
    def get_billing_address(self):
        """Parse billing address JSON string"""
        if self.billing_address:
            try:
                return json.loads(self.billing_address)
            except json.JSONDecodeError:
                return {}
        return {}
    
    def set_billing_address(self, address_dict):
        """Set billing address as JSON string"""
        self.billing_address = json.dumps(address_dict)
    
    def calculate_total(self):
        """Calculate total amount from order items"""
        return sum(item.total_price for item in self.items)
    
    def __repr__(self):
        return f'<Order {self.order_number}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'order_number': self.order_number,
            'user_id': self.user_id,
            'status': self.status,
            'total_amount': self.total_amount,
            'payment_method': self.payment_method,
            'payment_reference': self.payment_reference,
            'billing_address': self.get_billing_address(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'items': [item.to_dict() for item in self.items],
            'user': self.user.to_dict() if self.user else None
        }

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    plan_id = db.Column(db.Integer, db.ForeignKey('house_plan.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    unit_price = db.Column(db.Float, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    
    # Relationships
    plan = db.relationship('HousePlan', backref=db.backref('order_items', lazy=True))
    
    def __init__(self, **kwargs):
        super(OrderItem, self).__init__(**kwargs)
        if self.unit_price and self.quantity:
            self.total_price = self.unit_price * self.quantity
    
    def __repr__(self):
        return f'<OrderItem {self.plan.title if self.plan else "Unknown"} x{self.quantity}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'plan_id': self.plan_id,
            'quantity': self.quantity,
            'unit_price': self.unit_price,
            'total_price': self.total_price,
            'plan': self.plan.to_dict() if self.plan else None
        }

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    plan_id = db.Column(db.Integer, db.ForeignKey('house_plan.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref=db.backref('cart_items', lazy=True))
    plan = db.relationship('HousePlan', backref=db.backref('cart_items', lazy=True))
    
    # Unique constraint to prevent duplicate cart items
    __table_args__ = (db.UniqueConstraint('user_id', 'plan_id', name='unique_user_plan_cart'),)
    
    def __repr__(self):
        return f'<CartItem {self.plan.title if self.plan else "Unknown"} x{self.quantity}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'plan_id': self.plan_id,
            'quantity': self.quantity,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'plan': self.plan.to_dict() if self.plan else None,
            'total_price': self.plan.price * self.quantity if self.plan else 0
        }

