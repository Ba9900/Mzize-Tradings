import { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { X, Plus, Minus, ShoppingBag, CreditCard } from 'lucide-react';

const ShoppingCart = ({ isOpen, onClose, cartItems, updateCartItem, removeFromCart, onCheckout }) => {
  const [loading, setLoading] = useState(false);

  const calculateTotal = () => {
    return cartItems.reduce((total, item) => total + (item.price * item.quantity), 0);
  };

  const handleQuantityChange = (itemId, newQuantity) => {
    if (newQuantity < 1) {
      removeFromCart(itemId);
    } else {
      updateCartItem(itemId, newQuantity);
    }
  };

  const handleCheckout = () => {
    if (cartItems.length === 0) return;
    onCheckout();
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex justify-end">
      <div className="bg-white w-full max-w-md h-full overflow-y-auto">
        <div className="p-6">
          {/* Header */}
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center space-x-2">
              <ShoppingBag className="h-6 w-6" />
              <h2 className="text-xl font-semibold">Shopping Cart</h2>
            </div>
            <Button variant="ghost" size="icon" onClick={onClose}>
              <X className="h-5 w-5" />
            </Button>
          </div>

          {/* Cart Items */}
          <div className="space-y-4 mb-6">
            {cartItems.length === 0 ? (
              <div className="text-center py-8">
                <ShoppingBag className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                <p className="text-gray-500 mb-2">Your cart is empty</p>
                <p className="text-sm text-gray-400">Add some house plans to get started!</p>
              </div>
            ) : (
              cartItems.map((item) => (
                <Card key={item.id} className="p-4">
                  <div className="flex items-start space-x-4">
                    {item.featured_image_url && (
                      <img
                        src={item.featured_image_url}
                        alt={item.title}
                        className="w-16 h-16 object-cover rounded-lg"
                      />
                    )}
                    <div className="flex-1 min-w-0">
                      <h3 className="font-semibold text-sm truncate">{item.title}</h3>
                      <p className="text-xs text-gray-600 mb-2">
                        {item.bedrooms} bed • {item.bathrooms} bath • {item.square_footage} sq ft
                      </p>
                      <div className="flex items-center justify-between">
                        <span className="font-semibold text-green-600">
                          R{item.price.toLocaleString()}
                        </span>
                        <div className="flex items-center space-x-2">
                          <Button
                            variant="outline"
                            size="icon"
                            className="h-8 w-8"
                            onClick={() => handleQuantityChange(item.id, item.quantity - 1)}
                          >
                            <Minus className="h-3 w-3" />
                          </Button>
                          <span className="w-8 text-center text-sm">{item.quantity}</span>
                          <Button
                            variant="outline"
                            size="icon"
                            className="h-8 w-8"
                            onClick={() => handleQuantityChange(item.id, item.quantity + 1)}
                          >
                            <Plus className="h-3 w-3" />
                          </Button>
                        </div>
                      </div>
                    </div>
                    <Button
                      variant="ghost"
                      size="icon"
                      className="h-8 w-8 text-red-500 hover:text-red-700"
                      onClick={() => removeFromCart(item.id)}
                    >
                      <X className="h-4 w-4" />
                    </Button>
                  </div>
                </Card>
              ))
            )}
          </div>

          {/* Cart Summary */}
          {cartItems.length > 0 && (
            <div className="border-t pt-4">
              <div className="space-y-2 mb-4">
                <div className="flex justify-between text-sm">
                  <span>Subtotal ({cartItems.length} items)</span>
                  <span>R{calculateTotal().toLocaleString()}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span>Processing Fee</span>
                  <span>R0</span>
                </div>
                <div className="flex justify-between font-semibold text-lg border-t pt-2">
                  <span>Total</span>
                  <span className="text-green-600">R{calculateTotal().toLocaleString()}</span>
                </div>
              </div>

              <Button
                className="w-full bg-green-600 hover:bg-green-700"
                onClick={handleCheckout}
                disabled={loading}
              >
                <CreditCard className="h-4 w-4 mr-2" />
                {loading ? 'Processing...' : 'Proceed to Checkout'}
              </Button>

              <p className="text-xs text-gray-500 text-center mt-2">
                Secure checkout with South African payment methods
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ShoppingCart;

