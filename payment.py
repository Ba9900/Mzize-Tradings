from src.models.user import db
from datetime import datetime
import json

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)  # credit_card, eft_bank
    payment_gateway = db.Column(db.String(50), nullable=False)  # payfast, ozow, stitch
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), default='ZAR')
    status = db.Column(db.String(50), default='pending')  # pending, processing, completed, failed, cancelled
    gateway_reference = db.Column(db.String(200))  # Reference from payment gateway
    gateway_response = db.Column(db.Text)  # JSON response from gateway
    transaction_id = db.Column(db.String(200))  # Transaction ID from gateway
    
    # Credit Card specific fields
    card_type = db.Column(db.String(50))  # visa, mastercard, amex
    card_last_four = db.Column(db.String(4))
    
    # EFT Bank specific fields
    bank_name = db.Column(db.String(100))  # absa, fnb, standard_bank, nedbank, capitec, etc.
    bank_reference = db.Column(db.String(200))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    order = db.relationship('Order', backref=db.backref('payments', lazy=True))
    
    def __repr__(self):
        return f'<Payment {self.id} - {self.payment_method} - {self.status}>'
    
    def get_gateway_response(self):
        """Parse gateway response JSON string"""
        if self.gateway_response:
            try:
                return json.loads(self.gateway_response)
            except json.JSONDecodeError:
                return {}
        return {}
    
    def set_gateway_response(self, response_dict):
        """Set gateway response as JSON string"""
        self.gateway_response = json.dumps(response_dict)
    
    def to_dict(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'payment_method': self.payment_method,
            'payment_gateway': self.payment_gateway,
            'amount': self.amount,
            'currency': self.currency,
            'status': self.status,
            'gateway_reference': self.gateway_reference,
            'transaction_id': self.transaction_id,
            'card_type': self.card_type,
            'card_last_four': self.card_last_four,
            'bank_name': self.bank_name,
            'bank_reference': self.bank_reference,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'gateway_response': self.get_gateway_response()
        }

class PaymentMethod(db.Model):
    """Available payment methods configuration"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # "Credit Card", "EFT Bank Transfer"
    code = db.Column(db.String(50), unique=True, nullable=False)  # "credit_card", "eft_bank"
    gateway = db.Column(db.String(50), nullable=False)  # "payfast", "ozow"
    is_active = db.Column(db.Boolean, default=True)
    display_order = db.Column(db.Integer, default=0)
    description = db.Column(db.Text)
    icon_url = db.Column(db.String(500))
    
    # South African specific configurations
    supported_cards = db.Column(db.Text)  # JSON: ["visa", "mastercard", "amex"]
    supported_banks = db.Column(db.Text)  # JSON: ["absa", "fnb", "standard_bank", "nedbank", "capitec"]
    
    def __repr__(self):
        return f'<PaymentMethod {self.name}>'
    
    def get_supported_cards(self):
        """Parse supported cards JSON string"""
        if self.supported_cards:
            try:
                return json.loads(self.supported_cards)
            except json.JSONDecodeError:
                return []
        return []
    
    def set_supported_cards(self, cards_list):
        """Set supported cards as JSON string"""
        self.supported_cards = json.dumps(cards_list)
    
    def get_supported_banks(self):
        """Parse supported banks JSON string"""
        if self.supported_banks:
            try:
                return json.loads(self.supported_banks)
            except json.JSONDecodeError:
                return []
        return []
    
    def set_supported_banks(self, banks_list):
        """Set supported banks as JSON string"""
        self.supported_banks = json.dumps(banks_list)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'gateway': self.gateway,
            'is_active': self.is_active,
            'display_order': self.display_order,
            'description': self.description,
            'icon_url': self.icon_url,
            'supported_cards': self.get_supported_cards(),
            'supported_banks': self.get_supported_banks()
        }

# South African Banks Configuration
SA_BANKS = {
    'absa': 'ABSA Bank',
    'fnb': 'First National Bank (FNB)',
    'standard_bank': 'Standard Bank',
    'nedbank': 'Nedbank',
    'capitec': 'Capitec Bank',
    'investec': 'Investec Bank',
    'discovery': 'Discovery Bank',
    'african_bank': 'African Bank',
    'bidvest': 'Bidvest Bank',
    'sasfin': 'Sasfin Bank'
}

# Credit Card Types
CARD_TYPES = {
    'visa': 'Visa',
    'mastercard': 'Mastercard',
    'amex': 'American Express'
}

