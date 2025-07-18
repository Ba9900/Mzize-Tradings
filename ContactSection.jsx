import { useState } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Textarea } from '@/components/ui/textarea.jsx'
import { Label } from '@/components/ui/label.jsx'
import { 
  Mail, 
  Phone, 
  MapPin, 
  User, 
  Clock,
  MessageSquare,
  Send
} from 'lucide-react'

export function ContactSection() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    subject: '',
    message: ''
  })

  const handleInputChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    // In a real app, this would send the form data to the backend
    console.log('Contact form submitted:', formData)
    alert('Thank you for your message! We will get back to you soon.')
    setFormData({
      name: '',
      email: '',
      phone: '',
      subject: '',
      message: ''
    })
  }

  return (
    <section className="py-16 bg-gray-50" id="contact">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold text-gray-900 mb-4">Get In Touch</h2>
          <p className="text-gray-600 max-w-2xl mx-auto">
            Ready to start building your dream home? Contact us today to discuss your house plan needs 
            or get answers to any questions you may have.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
          {/* Contact Information */}
          <div className="space-y-8">
            <div>
              <h3 className="text-2xl font-semibold text-gray-900 mb-6">Contact Information</h3>
              
              <div className="space-y-6">
                <Card>
                  <CardContent className="p-6">
                    <div className="flex items-start space-x-4">
                      <div className="bg-primary/10 p-3 rounded-lg">
                        <User className="h-6 w-6 text-primary" />
                      </div>
                      <div>
                        <h4 className="font-semibold text-gray-900">Business Owner</h4>
                        <p className="text-gray-600">Banele Mditshwa</p>
                        <p className="text-sm text-gray-500 mt-1">Founder & Lead Designer</p>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                <Card>
                  <CardContent className="p-6">
                    <div className="flex items-start space-x-4">
                      <div className="bg-primary/10 p-3 rounded-lg">
                        <Mail className="h-6 w-6 text-primary" />
                      </div>
                      <div>
                        <h4 className="font-semibold text-gray-900">Email Address</h4>
                        <a 
                          href="mailto:banelemzize@gmail.com" 
                          className="text-primary hover:underline"
                        >
                          banelemzize@gmail.com
                        </a>
                        <p className="text-sm text-gray-500 mt-1">We respond within 24 hours</p>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                <Card>
                  <CardContent className="p-6">
                    <div className="flex items-start space-x-4">
                      <div className="bg-primary/10 p-3 rounded-lg">
                        <Phone className="h-6 w-6 text-primary" />
                      </div>
                      <div>
                        <h4 className="font-semibold text-gray-900">Phone Number</h4>
                        <a 
                          href="tel:0792832637" 
                          className="text-primary hover:underline"
                        >
                          079 283 2637
                        </a>
                        <p className="text-sm text-gray-500 mt-1">Available Mon-Fri, 8AM-6PM</p>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                <Card>
                  <CardContent className="p-6">
                    <div className="flex items-start space-x-4">
                      <div className="bg-primary/10 p-3 rounded-lg">
                        <MapPin className="h-6 w-6 text-primary" />
                      </div>
                      <div>
                        <h4 className="font-semibold text-gray-900">Location</h4>
                        <p className="text-gray-600">South Africa</p>
                        <p className="text-sm text-gray-500 mt-1">Serving clients nationwide</p>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </div>
            </div>

            {/* Business Hours */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Clock className="h-5 w-5 text-primary" />
                  <span>Business Hours</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <span className="text-gray-600">Monday - Friday</span>
                    <span className="font-medium">8:00 AM - 6:00 PM</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Saturday</span>
                    <span className="font-medium">9:00 AM - 4:00 PM</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Sunday</span>
                    <span className="font-medium">Closed</span>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Contact Form */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <MessageSquare className="h-5 w-5 text-primary" />
                <span>Send us a Message</span>
              </CardTitle>
              <CardDescription>
                Fill out the form below and we'll get back to you as soon as possible.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleSubmit} className="space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="name">Full Name *</Label>
                    <Input
                      id="name"
                      name="name"
                      type="text"
                      placeholder="Your full name"
                      value={formData.name}
                      onChange={handleInputChange}
                      required
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="email">Email Address *</Label>
                    <Input
                      id="email"
                      name="email"
                      type="email"
                      placeholder="your.email@example.com"
                      value={formData.email}
                      onChange={handleInputChange}
                      required
                    />
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="phone">Phone Number</Label>
                    <Input
                      id="phone"
                      name="phone"
                      type="tel"
                      placeholder="Your phone number"
                      value={formData.phone}
                      onChange={handleInputChange}
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="subject">Subject *</Label>
                    <Input
                      id="subject"
                      name="subject"
                      type="text"
                      placeholder="What is this regarding?"
                      value={formData.subject}
                      onChange={handleInputChange}
                      required
                    />
                  </div>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="message">Message *</Label>
                  <Textarea
                    id="message"
                    name="message"
                    placeholder="Tell us about your project, questions, or how we can help you..."
                    rows={6}
                    value={formData.message}
                    onChange={handleInputChange}
                    required
                  />
                </div>

                <Button type="submit" className="w-full" size="lg">
                  <Send className="h-4 w-4 mr-2" />
                  Send Message
                </Button>
              </form>
            </CardContent>
          </Card>
        </div>

        {/* Additional Information */}
        <div className="mt-16 text-center">
          <Card className="bg-primary/5 border-primary/20">
            <CardContent className="p-8">
              <h3 className="text-xl font-semibold text-gray-900 mb-4">
                Why Choose Mzize Tradings?
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-sm">
                <div>
                  <h4 className="font-medium text-gray-900 mb-2">Professional Designs</h4>
                  <p className="text-gray-600">
                    All our house plans are professionally designed and meet South African building standards.
                  </p>
                </div>
                <div>
                  <h4 className="font-medium text-gray-900 mb-2">Custom Modifications</h4>
                  <p className="text-gray-600">
                    We can modify any plan to suit your specific needs and preferences.
                  </p>
                </div>
                <div>
                  <h4 className="font-medium text-gray-900 mb-2">Expert Support</h4>
                  <p className="text-gray-600">
                    Get expert guidance throughout your building journey from planning to completion.
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </section>
  )
}

