import { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Textarea } from './ui/textarea';
import { Badge } from './ui/badge';
import { ArrowLeft, CreditCard, Building2, Shield, CheckCircle } from 'lucide-react';

const Checkout = ({ cartItems, onBack, onOrderComplete }) => {
  const [step, setStep] = useState(1); // 1: Details, 2: Payment, 3: Confirmation
  const [loading, setLoading] = useState(false);
  const [paymentMethods, setPaymentMethods] = useState([]);
  const [selectedPaymentMethod, setSelectedPaymentMethod] = useState(null);
  const [orderData, setOrderData] = useState({
    // Customer Details
    firstName: '',
    lastName: '',
    email: '',
    phone: '',
    
    // Billing Address
    address: '',
    city: '',
    province: '',
    postalCode: '',
    
    // Additional Info
    notes: ''
  });

  useEffect(() => {
    fetchPaymentMethods();
  }, []);

  const fetchPaymentMethods = async () => {
    try {
      const response = await fetch('https://vgh0i1co5gke.manus.space/api/payment-methods');
      const data = await response.json();
      if (data.success) {
        setPaymentMethods(data.data);
        if (data.data.length > 0) {
          setSelectedPaymentMethod(data.data[0]);
        }
      }
    } catch (error) {
      console.error('Error fetching payment methods:', error);
    }
  };

  const calculateTotal = () => {
    return cartItems.reduce((total, item) => total + (item.price * item.quantity), 0);
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setOrderData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleNextStep = () => {
    if (step === 1) {
      // Validate customer details
      if (!orderData.firstName || !orderData.lastName || !orderData.email || !orderData.phone) {
        alert('Please fill in all required fields');
        return;
      }
      setStep(2);
    } else if (step === 2) {
      handlePayment();
    }
  };

  const handlePayment = async () => {
    setLoading(true);
    
    try {
      // Create order
      const orderPayload = {
        customer_info: {
          first_name: orderData.firstName,
          last_name: orderData.lastName,
          email: orderData.email,
          phone: orderData.phone,
          address: orderData.address,
          city: orderData.city,
          province: orderData.province,
          postal_code: orderData.postalCode
        },
        items: cartItems.map(item => ({
          house_plan_id: item.id,
          quantity: item.quantity,
          price: item.price
        })),
        payment_method_id: selectedPaymentMethod.id,
        notes: orderData.notes,
        total_amount: calculateTotal()
      };

      const response = await fetch('https://vgh0i1co5gke.manus.space/api/orders', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(orderPayload),
      });

      const data = await response.json();
      
      if (data.success) {
        // Simulate payment processing
        setTimeout(() => {
          setStep(3);
          setLoading(false);
        }, 2000);
      } else {
        alert('Error creating order: ' + data.error);
        setLoading(false);
      }
    } catch (error) {
      console.error('Error processing payment:', error);
      alert('Error processing payment');
      setLoading(false);
    }
  };

  const handleOrderComplete = () => {
    onOrderComplete();
  };

  const renderCustomerDetails = () => (
    <div className="space-y-6">
      <div>
        <h2 className="text-xl font-semibold mb-4">Customer Information</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              First Name *
            </label>
            <Input
              name="firstName"
              value={orderData.firstName}
              onChange={handleInputChange}
              placeholder="Enter your first name"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Last Name *
            </label>
            <Input
              name="lastName"
              value={orderData.lastName}
              onChange={handleInputChange}
              placeholder="Enter your last name"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Email Address *
            </label>
            <Input
              name="email"
              type="email"
              value={orderData.email}
              onChange={handleInputChange}
              placeholder="your.email@example.com"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Phone Number *
            </label>
            <Input
              name="phone"
              value={orderData.phone}
              onChange={handleInputChange}
              placeholder="e.g., 079 123 4567"
              required
            />
          </div>
        </div>
      </div>

      <div>
        <h3 className="text-lg font-semibold mb-4">Billing Address</h3>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Street Address
            </label>
            <Input
              name="address"
              value={orderData.address}
              onChange={handleInputChange}
              placeholder="123 Main Street"
            />
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                City
              </label>
              <Input
                name="city"
                value={orderData.city}
                onChange={handleInputChange}
                placeholder="Cape Town"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Province
              </label>
              <Input
                name="province"
                value={orderData.province}
                onChange={handleInputChange}
                placeholder="Western Cape"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Postal Code
              </label>
              <Input
                name="postalCode"
                value={orderData.postalCode}
                onChange={handleInputChange}
                placeholder="8001"
              />
            </div>
          </div>
        </div>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Additional Notes (Optional)
        </label>
        <Textarea
          name="notes"
          value={orderData.notes}
          onChange={handleInputChange}
          placeholder="Any special requirements or notes about your order..."
          rows={3}
        />
      </div>
    </div>
  );

  const renderPaymentMethods = () => (
    <div className="space-y-6">
      <div>
        <h2 className="text-xl font-semibold mb-4">Payment Method</h2>
        <p className="text-gray-600 mb-4">Choose your preferred payment method</p>
        
        <div className="space-y-3">
          {paymentMethods.map((method) => (
            <Card 
              key={method.id} 
              className={`cursor-pointer transition-all ${
                selectedPaymentMethod?.id === method.id 
                  ? 'ring-2 ring-green-500 bg-green-50' 
                  : 'hover:bg-gray-50'
              }`}
              onClick={() => setSelectedPaymentMethod(method)}
            >
              <CardContent className="p-4">
                <div className="flex items-center space-x-4">
                  <div className="p-2 bg-blue-100 rounded-lg">
                    {method.code === 'credit_card' ? (
                      <CreditCard className="h-6 w-6 text-blue-600" />
                    ) : (
                      <Building2 className="h-6 w-6 text-blue-600" />
                    )}
                  </div>
                  <div className="flex-1">
                    <h3 className="font-semibold">{method.name}</h3>
                    <p className="text-sm text-gray-600">{method.description}</p>
                    <div className="flex flex-wrap gap-1 mt-2">
                      {method.supported_cards?.map((card) => (
                        <Badge key={card} variant="secondary" className="text-xs">
                          {card.toUpperCase()}
                        </Badge>
                      ))}
                      {method.supported_banks?.map((bank) => (
                        <Badge key={bank} variant="secondary" className="text-xs">
                          {bank.replace('_', ' ').toUpperCase()}
                        </Badge>
                      ))}
                    </div>
                  </div>
                  <div className="flex items-center">
                    <Shield className="h-5 w-5 text-green-500" />
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>

      <div className="bg-gray-50 p-4 rounded-lg">
        <div className="flex items-center space-x-2 mb-2">
          <Shield className="h-5 w-5 text-green-500" />
          <span className="font-semibold text-sm">Secure Payment</span>
        </div>
        <p className="text-xs text-gray-600">
          Your payment information is encrypted and secure. We use industry-standard security measures to protect your data.
        </p>
      </div>
    </div>
  );

  const renderConfirmation = () => (
    <div className="text-center space-y-6">
      <div className="flex justify-center">
        <CheckCircle className="h-16 w-16 text-green-500" />
      </div>
      <div>
        <h2 className="text-2xl font-bold text-green-600 mb-2">Order Confirmed!</h2>
        <p className="text-gray-600 mb-4">
          Thank you for your purchase. Your house plans will be sent to your email address shortly.
        </p>
        <div className="bg-green-50 p-4 rounded-lg">
          <p className="text-sm text-green-800">
            <strong>Order Total:</strong> R{calculateTotal().toLocaleString()}
          </p>
          <p className="text-sm text-green-800">
            <strong>Payment Method:</strong> {selectedPaymentMethod?.name}
          </p>
          <p className="text-sm text-green-800">
            <strong>Email:</strong> {orderData.email}
          </p>
        </div>
      </div>
      <div className="space-y-2">
        <p className="text-sm text-gray-600">
          You will receive an email confirmation with your house plans and receipt.
        </p>
        <p className="text-sm text-gray-600">
          For any questions, contact Banele at{' '}
          <a href="mailto:banelemzize@gmail.com" className="text-blue-600 hover:underline">
            banelemzize@gmail.com
          </a>
        </p>
      </div>
    </div>
  );

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="flex items-center space-x-4 mb-8">
          {step < 3 && (
            <Button variant="ghost" onClick={step === 1 ? onBack : () => setStep(step - 1)}>
              <ArrowLeft className="h-4 w-4 mr-2" />
              Back
            </Button>
          )}
          <div>
            <h1 className="text-2xl font-bold">
              {step === 1 && 'Customer Details'}
              {step === 2 && 'Payment Method'}
              {step === 3 && 'Order Complete'}
            </h1>
            <p className="text-gray-600">
              {step === 1 && 'Enter your information to complete the purchase'}
              {step === 2 && 'Choose how you\'d like to pay'}
              {step === 3 && 'Your order has been successfully processed'}
            </p>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Content */}
          <div className="lg:col-span-2">
            <Card>
              <CardContent className="p-6">
                {step === 1 && renderCustomerDetails()}
                {step === 2 && renderPaymentMethods()}
                {step === 3 && renderConfirmation()}
              </CardContent>
            </Card>
          </div>

          {/* Order Summary */}
          <div className="lg:col-span-1">
            <Card>
              <CardHeader>
                <CardTitle>Order Summary</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {cartItems.map((item) => (
                    <div key={item.id} className="flex justify-between items-start">
                      <div className="flex-1">
                        <h4 className="font-medium text-sm">{item.title}</h4>
                        <p className="text-xs text-gray-600">
                          Qty: {item.quantity} × R{item.price.toLocaleString()}
                        </p>
                      </div>
                      <span className="font-semibold text-sm">
                        R{(item.price * item.quantity).toLocaleString()}
                      </span>
                    </div>
                  ))}
                  
                  <div className="border-t pt-4">
                    <div className="flex justify-between font-semibold">
                      <span>Total</span>
                      <span className="text-green-600">R{calculateTotal().toLocaleString()}</span>
                    </div>
                  </div>
                </div>

                {step < 3 && (
                  <Button
                    className="w-full mt-6 bg-green-600 hover:bg-green-700"
                    onClick={handleNextStep}
                    disabled={loading}
                  >
                    {loading ? 'Processing...' : (step === 1 ? 'Continue to Payment' : 'Complete Order')}
                  </Button>
                )}

                {step === 3 && (
                  <Button
                    className="w-full mt-6"
                    onClick={handleOrderComplete}
                  >
                    Continue Shopping
                  </Button>
                )}
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Checkout;

