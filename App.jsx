import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Input } from '@/components/ui/input.jsx'
import { ContactSection } from './components/ContactSection.jsx'
import AdminPanel from './components/AdminPanel.jsx'
import ShoppingCart from './components/ShoppingCart.jsx'
import Checkout from './components/Checkout.jsx'
import { 
  Search, 
  Home, 
  Building2, 
  ShoppingCart as ShoppingCartIcon, 
  User, 
  Menu, 
  X,
  Bed,
  Bath,
  Square,
  Car,
  Star,
  Heart,
  Settings,
  Filter,
  Grid3X3,
  List
} from 'lucide-react'
import './App.css'

function App() {
  const [isMenuOpen, setIsMenuOpen] = useState(false)
  const [viewMode, setViewMode] = useState('grid')
  const [searchQuery, setSearchQuery] = useState('')
  const [cartItems, setCartItems] = useState([])
  const [showAdminPanel, setShowAdminPanel] = useState(false)
  const [showCart, setShowCart] = useState(false)
  const [showCheckout, setShowCheckout] = useState(false)
  const [housePlans, setHousePlans] = useState([])
  const [loading, setLoading] = useState(true)

  // Load house plans from API
  useEffect(() => {
    fetchHousePlans();
  }, []);

  const fetchHousePlans = async () => {
    try {
      const response = await fetch('https://vgh0i1co5gke.manus.space/api/house-plans');
      const data = await response.json();
      if (data.success) {
        setHousePlans(data.data);
      }
    } catch (error) {
      console.error('Error fetching house plans:', error);
    } finally {
      setLoading(false);
    }
  };

  const addToCart = (plan) => {
    setCartItems(prev => {
      const existingItem = prev.find(item => item.id === plan.id);
      if (existingItem) {
        return prev.map(item =>
          item.id === plan.id
            ? { ...item, quantity: item.quantity + 1 }
            : item
        );
      } else {
        return [...prev, { ...plan, quantity: 1 }];
      }
    });
  };

  const updateCartItem = (planId, quantity) => {
    setCartItems(prev =>
      prev.map(item =>
        item.id === planId
          ? { ...item, quantity }
          : item
      )
    );
  };

  const removeFromCart = (planId) => {
    setCartItems(prev => prev.filter(item => item.id !== planId));
  };

  const handleCheckout = () => {
    setShowCart(false);
    setShowCheckout(true);
  };

  const handleOrderComplete = () => {
    setCartItems([]);
    setShowCheckout(false);
    setShowCart(false);
  };

  const toggleFavorite = (planId) => {
    console.log(`Toggled favorite for plan ${planId}`)
  }

  const filteredPlans = housePlans.filter(plan =>
    plan.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
    plan.style_category.toLowerCase().includes(searchQuery.toLowerCase())
  )

  if (showCheckout) {
    return (
      <Checkout
        cartItems={cartItems}
        onBack={() => setShowCheckout(false)}
        onOrderComplete={handleOrderComplete}
      />
    );
  }

  return (
    <div className="min-h-screen bg-background">
      {showAdminPanel ? (
        <AdminPanel />
      ) : (
        <>
          {/* Navigation */}
          <nav className="bg-white shadow-sm border-b sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            {/* Logo */}
            <div className="flex items-center space-x-2">
              <Building2 className="h-8 w-8 text-primary" />
              <span className="text-xl font-bold text-primary">Mzize Tradings</span>
            </div>

            {/* Desktop Navigation */}
            <div className="hidden md:flex items-center space-x-8">
              <a href="#" className="text-gray-700 hover:text-primary transition-colors">Home</a>
              <a href="#" className="text-gray-700 hover:text-primary transition-colors">House Plans</a>
              <a href="#" className="text-gray-700 hover:text-primary transition-colors">Categories</a>
              <a href="#" className="text-gray-700 hover:text-primary transition-colors">About</a>
              <a href="#" className="text-gray-700 hover:text-primary transition-colors">Contact</a>
            </div>

            {/* Right side icons */}
            <div className="flex items-center space-x-4">
              <Button 
                variant="ghost" 
                size="icon"
                onClick={() => setShowAdminPanel(!showAdminPanel)}
                title="Admin Panel"
              >
                <Settings className="h-5 w-5" />
              </Button>
              <Button 
                variant="ghost" 
                size="icon" 
                className="relative"
                onClick={() => setShowCart(true)}
              >
                <ShoppingCartIcon className="h-5 w-5" />
                {cartItems.length > 0 && (
                  <Badge className="absolute -top-2 -right-2 h-5 w-5 rounded-full p-0 flex items-center justify-center text-xs">
                    {cartItems.reduce((total, item) => total + item.quantity, 0)}
                  </Badge>
                )}
              </Button>
              <Button variant="ghost" size="icon">
                <User className="h-5 w-5" />
              </Button>
              <Button 
                variant="ghost" 
                size="icon" 
                className="md:hidden"
                onClick={() => setIsMenuOpen(!isMenuOpen)}
              >
                {isMenuOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
              </Button>
            </div>
          </div>

          {/* Mobile Navigation */}
          {isMenuOpen && (
            <div className="md:hidden border-t bg-white py-4">
              <div className="flex flex-col space-y-4">
                <a href="#" className="text-gray-700 hover:text-primary transition-colors">Home</a>
                <a href="#" className="text-gray-700 hover:text-primary transition-colors">House Plans</a>
                <a href="#" className="text-gray-700 hover:text-primary transition-colors">Categories</a>
                <a href="#" className="text-gray-700 hover:text-primary transition-colors">About</a>
                <a href="#" className="text-gray-700 hover:text-primary transition-colors">Contact</a>
              </div>
            </div>
          )}
        </div>
      </nav>

      {/* Hero Section */}
      <section className="bg-gradient-to-br from-blue-50 to-indigo-100 py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="text-4xl md:text-6xl font-bold text-gray-900 mb-6">
            Premium House Plans &<br />
            <span className="text-primary">Architectural Designs</span>
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
            Discover your dream home with our collection of professionally designed house plans. 
            From modern family homes to luxury villas, find the perfect design for your lifestyle.
          </p>
          
          {/* Search Bar */}
          <div className="max-w-2xl mx-auto mb-8">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-5 w-5" />
              <Input
                type="text"
                placeholder="Search house plans by style, size, or features..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-10 pr-4 py-3 text-lg"
              />
            </div>
          </div>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button size="lg" className="bg-primary hover:bg-primary/90">
              Browse All Plans
            </Button>
            <Button size="lg" variant="outline">
              Learn More
            </Button>
          </div>
        </div>
      </section>

      {/* Featured House Plans */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center mb-8">
            <div>
              <h2 className="text-3xl font-bold text-gray-900 mb-2">Featured House Plans</h2>
              <p className="text-gray-600">Discover our most popular and newest designs</p>
            </div>
            <div className="flex items-center space-x-2">
              <Button
                variant={viewMode === 'grid' ? 'default' : 'outline'}
                size="sm"
                onClick={() => setViewMode('grid')}
              >
                <Grid3X3 className="h-4 w-4" />
              </Button>
              <Button
                variant={viewMode === 'list' ? 'default' : 'outline'}
                size="sm"
                onClick={() => setViewMode('list')}
              >
                <List className="h-4 w-4" />
              </Button>
            </div>
          </div>

          {loading ? (
            <div className="text-center py-8">
              <p>Loading house plans...</p>
            </div>
          ) : (
            <div className={`grid gap-6 ${viewMode === 'grid' ? 'grid-cols-1 md:grid-cols-2 lg:grid-cols-3' : 'grid-cols-1'}`}>
              {filteredPlans.map((plan) => (
                <Card key={plan.id} className="overflow-hidden hover:shadow-lg transition-shadow">
                  <div className="relative">
                    <img
                      src={plan.featured_image_url}
                      alt={plan.title}
                      className="w-full h-48 object-cover"
                    />
                    {plan.is_featured && (
                      <Badge className="absolute top-2 left-2 bg-yellow-500">
                        Featured
                      </Badge>
                    )}
                    <Button
                      variant="ghost"
                      size="icon"
                      className="absolute top-2 right-2 bg-white/80 hover:bg-white"
                      onClick={() => toggleFavorite(plan.id)}
                    >
                      <Heart className="h-4 w-4" />
                    </Button>
                  </div>
                  
                  <CardContent className="p-6">
                    <div className="flex justify-between items-start mb-2">
                      <h3 className="text-xl font-semibold">{plan.title}</h3>
                      <Badge variant="secondary">{plan.style_category}</Badge>
                    </div>
                    
                    <p className="text-gray-600 mb-4 line-clamp-2">{plan.description}</p>
                    
                    <div className="grid grid-cols-4 gap-4 mb-4 text-sm text-gray-600">
                      <div className="flex items-center">
                        <Bed className="h-4 w-4 mr-1" />
                        <span>{plan.bedrooms} Bed</span>
                      </div>
                      <div className="flex items-center">
                        <Bath className="h-4 w-4 mr-1" />
                        <span>{plan.bathrooms} Bath</span>
                      </div>
                      <div className="flex items-center">
                        <Square className="h-4 w-4 mr-1" />
                        <span>{plan.square_footage} sq ft</span>
                      </div>
                      <div className="flex items-center">
                        <Car className="h-4 w-4 mr-1" />
                        <span>{plan.garage_spaces} Garage</span>
                      </div>
                    </div>
                    
                    <div className="flex justify-between items-center">
                      <div>
                        <span className="text-2xl font-bold text-green-600">R{plan.price.toLocaleString()}</span>
                        <div className="flex items-center mt-1">
                          <Star className="h-4 w-4 text-yellow-400 fill-current" />
                          <span className="text-sm text-gray-600 ml-1">4.8</span>
                        </div>
                      </div>
                      <div className="space-x-2">
                        <Button 
                          size="sm" 
                          className="bg-green-600 hover:bg-green-700"
                          onClick={() => addToCart(plan)}
                        >
                          Add to Cart
                        </Button>
                        <Button size="sm" variant="outline">
                          View Details
                        </Button>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          )}
        </div>
      </section>

      {/* Browse by Style */}
      <section className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">Browse by Style</h2>
            <p className="text-gray-600 max-w-2xl mx-auto">
              Explore our diverse collection of architectural styles to find the perfect design for your dream home.
            </p>
          </div>
          
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
            {[
              { name: 'Modern', count: 29, image: 'https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=300&h=200&fit=crop' },
              { name: 'Traditional', count: 27, image: 'https://images.unsplash.com/photo-1600047509807-ba8f99d2cdde?w=300&h=200&fit=crop' },
              { name: 'Contemporary', count: 36, image: 'https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=300&h=200&fit=crop' },
              { name: 'Farmhouse', count: 20, image: 'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=300&h=200&fit=crop' },
              { name: 'Minimalist', count: 43, image: 'https://images.unsplash.com/photo-1600566753190-17f0baa2a6c3?w=300&h=200&fit=crop' },
              { name: 'Urban', count: 42, image: 'https://images.unsplash.com/photo-1600607687644-c7171b42498b?w=300&h=200&fit=crop' },
              { name: 'Luxury', count: 19, image: 'https://images.unsplash.com/photo-1600607687920-4e2a09cf159d?w=300&h=200&fit=crop' },
              { name: 'Cottage', count: 37, image: 'https://images.unsplash.com/photo-1600047509358-9dc75507daeb?w=300&h=200&fit=crop' }
            ].map((style) => (
              <Card key={style.name} className="overflow-hidden hover:shadow-lg transition-shadow cursor-pointer">
                <div className="relative">
                  <img
                    src={style.image}
                    alt={style.name}
                    className="w-full h-32 object-cover"
                  />
                  <div className="absolute inset-0 bg-black bg-opacity-40 flex items-center justify-center">
                    <div className="text-center text-white">
                      <h3 className="font-semibold text-lg">{style.name}</h3>
                      <p className="text-sm opacity-90">{style.count} plans</p>
                    </div>
                  </div>
                </div>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Contact Section */}
      <ContactSection />

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div>
              <div className="flex items-center space-x-2 mb-4">
                <Building2 className="h-8 w-8" />
                <span className="text-xl font-bold">Mzize Tradings</span>
              </div>
              <p className="text-gray-400">
                Professional house plans and architectural designs for your dream home.
              </p>
            </div>
            
            <div>
              <h3 className="font-semibold mb-4">Quick Links</h3>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#" className="hover:text-white transition-colors">House Plans</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Categories</a></li>
                <li><a href="#" className="hover:text-white transition-colors">About Us</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Contact</a></li>
              </ul>
            </div>
            
            <div>
              <h3 className="font-semibold mb-4">Services</h3>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#" className="hover:text-white transition-colors">Custom Designs</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Plan Modifications</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Consultation</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Support</a></li>
              </ul>
            </div>
            
            <div>
              <h3 className="font-semibold mb-4">Contact Info</h3>
              <div className="space-y-2 text-gray-400">
                <p>👤 Banele Mditshwa</p>
                <p>📧 banelemzize@gmail.com</p>
                <p>📞 079 283 2637</p>
                <p>📍 South Africa</p>
              </div>
            </div>
          </div>
          
          <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
            <p>&copy; 2025 Mzize Tradings. All rights reserved.</p>
          </div>
        </div>
      </footer>
        </>
      )}

      {/* Shopping Cart */}
      <ShoppingCart
        isOpen={showCart}
        onClose={() => setShowCart(false)}
        cartItems={cartItems}
        updateCartItem={updateCartItem}
        removeFromCart={removeFromCart}
        onCheckout={handleCheckout}
      />
    </div>
  )
}

export default App

