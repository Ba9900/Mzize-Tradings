from flask import Blueprint, request, jsonify, redirect, url_for
from src.models.user import db
from src.models.order import Order, OrderItem
from src.models.payment import Payment, PaymentMethod, SA_BANKS, CARD_TYPES
from src.models.house_plan import HousePlan
import hashlib
import urllib.parse
import requests
from datetime import datetime

payments_bp = Blueprint('payments', __name__)

# PayFast Configuration (Sandbox)
PAYFAST_CONFIG = {
    'merchant_id': '10000100',  # Sandbox merchant ID
    'merchant_key': '46f0cd694581a',  # Sandbox merchant key
    'passphrase': 'jt7NOE43FZPn',  # Sandbox passphrase
    'sandbox': True,
    'url': 'https://sandbox.payfast.co.za/eng/process'
}

# Ozow Configuration (Test)
OZOW_CONFIG = {
    'site_code': 'TEST-TEST',  # Test site code
    'private_key': 'test-private-key',
    'api_url': 'https://api.ozow.com',
    'sandbox': True
}

@payments_bp.route('/payment-methods', methods=['GET'])
def get_payment_methods():
    """Get available payment methods for South Africa"""
    try:
        methods = PaymentMethod.query.filter_by(is_active=True)\
                                   .order_by(PaymentMethod.display_order).all()
        
        return jsonify({
            'success': True,
            'data': [method.to_dict() for method in methods]
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@payments_bp.route('/banks', methods=['GET'])
def get_south_african_banks():
    """Get list of South African banks for EFT payments"""
    try:
        banks = [{'code': code, 'name': name} for code, name in SA_BANKS.items()]
        
        return jsonify({
            'success': True,
            'data': banks
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@payments_bp.route('/card-types', methods=['GET'])
def get_card_types():
    """Get supported credit card types"""
    try:
        cards = [{'code': code, 'name': name} for code, name in CARD_TYPES.items()]
        
        return jsonify({
            'success': True,
            'data': cards
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@payments_bp.route('/process-payment', methods=['POST'])
def process_payment():
    """Process payment based on selected method"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['order_id', 'payment_method', 'amount']
        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'error': f'Missing required field: {field}'}), 400
        
        # Get order
        order = Order.query.get(data['order_id'])
        if not order:
            return jsonify({'success': False, 'error': 'Order not found'}), 404
        
        payment_method = data['payment_method']
        amount = data['amount']
        
        # Create payment record
        payment = Payment(
            order_id=order.id,
            payment_method=payment_method,
            amount=amount,
            currency='ZAR',
            status='pending'
        )
        
        if payment_method == 'credit_card':
            return process_credit_card_payment(payment, data)
        elif payment_method == 'eft_bank':
            return process_eft_payment(payment, data)
        else:
            return jsonify({'success': False, 'error': 'Invalid payment method'}), 400
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

def process_credit_card_payment(payment, data):
    """Process credit card payment via PayFast"""
    try:
        payment.payment_gateway = 'payfast'
        
        # PayFast payment data
        payfast_data = {
            'merchant_id': PAYFAST_CONFIG['merchant_id'],
            'merchant_key': PAYFAST_CONFIG['merchant_key'],
            'return_url': f"{request.host_url}api/payments/payfast/return",
            'cancel_url': f"{request.host_url}api/payments/payfast/cancel",
            'notify_url': f"{request.host_url}api/payments/payfast/notify",
            'name_first': data.get('first_name', ''),
            'name_last': data.get('last_name', ''),
            'email_address': data.get('email', ''),
            'cell_number': data.get('phone', ''),
            'm_payment_id': str(payment.order_id),
            'amount': f"{payment.amount:.2f}",
            'item_name': f"House Plans - Order #{payment.order.order_number}",
            'item_description': 'House plan purchase from Mzize Tradings',
            'custom_str1': str(payment.order_id),
            'custom_str2': payment.payment_method
        }
        
        # Generate signature
        signature = generate_payfast_signature(payfast_data)
        payfast_data['signature'] = signature
        
        # Save payment
        payment.gateway_reference = f"PF_{payment.order_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        db.session.add(payment)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'payment_url': PAYFAST_CONFIG['url'],
            'payment_data': payfast_data,
            'payment_id': payment.id
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

def process_eft_payment(payment, data):
    """Process EFT bank payment via Ozow"""
    try:
        payment.payment_gateway = 'ozow'
        payment.bank_name = data.get('bank_code', '')
        
        # Ozow payment data
        ozow_data = {
            'SiteCode': OZOW_CONFIG['site_code'],
            'CountryCode': 'ZA',
            'CurrencyCode': 'ZAR',
            'Amount': payment.amount,
            'TransactionReference': f"MZ_{payment.order_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            'BankReference': f"Mzize Tradings Order #{payment.order.order_number}",
            'Customer': data.get('email', ''),
            'SuccessUrl': f"{request.host_url}api/payments/ozow/success",
            'CancelUrl': f"{request.host_url}api/payments/ozow/cancel",
            'ErrorUrl': f"{request.host_url}api/payments/ozow/error",
            'NotifyUrl': f"{request.host_url}api/payments/ozow/notify",
            'IsTest': OZOW_CONFIG['sandbox']
        }
        
        # Generate hash for Ozow
        hash_string = f"{ozow_data['SiteCode']}{ozow_data['CountryCode']}{ozow_data['CurrencyCode']}" \
                     f"{ozow_data['Amount']}{ozow_data['TransactionReference']}{ozow_data['BankReference']}" \
                     f"{OZOW_CONFIG['private_key']}"
        
        ozow_data['HashCheck'] = hashlib.sha512(hash_string.encode()).hexdigest()
        
        # Save payment
        payment.gateway_reference = ozow_data['TransactionReference']
        payment.bank_reference = ozow_data['BankReference']
        db.session.add(payment)
        db.session.commit()
        
        # Build Ozow URL
        ozow_url = f"https://pay.ozow.com/?{urllib.parse.urlencode(ozow_data)}"
        
        return jsonify({
            'success': True,
            'payment_url': ozow_url,
            'payment_data': ozow_data,
            'payment_id': payment.id
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

def generate_payfast_signature(data):
    """Generate PayFast signature"""
    # Create parameter string
    param_string = ""
    for key in sorted(data.keys()):
        if key != 'signature':
            param_string += f"{key}={urllib.parse.quote_plus(str(data[key]))}&"
    
    # Remove last ampersand
    param_string = param_string.rstrip('&')
    
    # Add passphrase if provided
    if PAYFAST_CONFIG.get('passphrase'):
        param_string += f"&passphrase={urllib.parse.quote_plus(PAYFAST_CONFIG['passphrase'])}"
    
    # Generate MD5 hash
    return hashlib.md5(param_string.encode()).hexdigest()

@payments_bp.route('/payfast/return', methods=['GET', 'POST'])
def payfast_return():
    """PayFast return URL handler"""
    try:
        # Handle successful payment return
        return redirect(f"{request.host_url}payment-success")
    except Exception as e:
        return redirect(f"{request.host_url}payment-error")

@payments_bp.route('/payfast/cancel', methods=['GET', 'POST'])
def payfast_cancel():
    """PayFast cancel URL handler"""
    try:
        # Handle cancelled payment
        return redirect(f"{request.host_url}payment-cancelled")
    except Exception as e:
        return redirect(f"{request.host_url}payment-error")

@payments_bp.route('/payfast/notify', methods=['POST'])
def payfast_notify():
    """PayFast IPN (Instant Payment Notification) handler"""
    try:
        data = request.form.to_dict()
        
        # Verify signature
        if not verify_payfast_signature(data):
            return "Invalid signature", 400
        
        # Update payment status
        payment_id = data.get('custom_str1')
        if payment_id:
            order = Order.query.get(payment_id)
            if order:
                payment = Payment.query.filter_by(order_id=order.id).first()
                if payment:
                    payment.status = 'completed' if data.get('payment_status') == 'COMPLETE' else 'failed'
                    payment.transaction_id = data.get('pf_payment_id')
                    payment.set_gateway_response(data)
                    
                    # Update order status
                    if payment.status == 'completed':
                        order.status = 'paid'
                    
                    db.session.commit()
        
        return "OK", 200
    
    except Exception as e:
        return str(e), 500

def verify_payfast_signature(data):
    """Verify PayFast signature"""
    try:
        received_signature = data.pop('signature', '')
        generated_signature = generate_payfast_signature(data)
        return received_signature == generated_signature
    except:
        return False

@payments_bp.route('/ozow/success', methods=['GET', 'POST'])
def ozow_success():
    """Ozow success URL handler"""
    try:
        return redirect(f"{request.host_url}payment-success")
    except Exception as e:
        return redirect(f"{request.host_url}payment-error")

@payments_bp.route('/ozow/cancel', methods=['GET', 'POST'])
def ozow_cancel():
    """Ozow cancel URL handler"""
    try:
        return redirect(f"{request.host_url}payment-cancelled")
    except Exception as e:
        return redirect(f"{request.host_url}payment-error")

@payments_bp.route('/ozow/error', methods=['GET', 'POST'])
def ozow_error():
    """Ozow error URL handler"""
    try:
        return redirect(f"{request.host_url}payment-error")
    except Exception as e:
        return redirect(f"{request.host_url}payment-error")

@payments_bp.route('/ozow/notify', methods=['POST'])
def ozow_notify():
    """Ozow notification handler"""
    try:
        data = request.form.to_dict()
        
        # Update payment status based on Ozow response
        transaction_ref = data.get('TransactionReference')
        if transaction_ref:
            payment = Payment.query.filter_by(gateway_reference=transaction_ref).first()
            if payment:
                payment.status = 'completed' if data.get('Status') == 'Complete' else 'failed'
                payment.transaction_id = data.get('TransactionId')
                payment.set_gateway_response(data)
                
                # Update order status
                if payment.status == 'completed':
                    payment.order.status = 'paid'
                
                db.session.commit()
        
        return "OK", 200
    
    except Exception as e:
        return str(e), 500

@payments_bp.route('/payment-status/<int:payment_id>', methods=['GET'])
def get_payment_status(payment_id):
    """Get payment status"""
    try:
        payment = Payment.query.get(payment_id)
        if not payment:
            return jsonify({'success': False, 'error': 'Payment not found'}), 404
        
        return jsonify({
            'success': True,
            'data': payment.to_dict()
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

