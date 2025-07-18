# Mzize Tradings House Plans Website - Architecture Plan

## Project Overview
Building a complete e-commerce website for Mzize Tradings to sell house plans with modern interface, admin panel, shopping cart, checkout system, and South African payment integration.

## Technology Stack

### Frontend
- **Framework**: React 18 with TypeScript
- **UI Library**: Tailwind CSS + Headless UI components
- **State Management**: React Context + useReducer for cart, React Query for server state
- **Routing**: React Router v6
- **Forms**: React Hook Form with Zod validation
- **Image Handling**: React Image Gallery, lazy loading
- **Icons**: Heroicons, Lucide React
- **Animations**: Framer Motion for smooth transitions

### Backend
- **Framework**: Flask with Flask-RESTful
- **Database**: SQLite (development) / PostgreSQL (production)
- **ORM**: SQLAlchemy with Flask-SQLAlchemy
- **Authentication**: Flask-JWT-Extended
- **File Upload**: Flask-Upload with image processing
- **API Documentation**: Flask-RESTX (Swagger)
- **CORS**: Flask-CORS

### Payment Integration
- **Primary**: PayFast (most popular in SA)
- **Secondary**: Ozow (instant EFT)
- **Backup**: Stitch Money
- **Card Processing**: Visa, Mastercard, American Express

### Deployment & Infrastructure
- **Frontend**: Deployed via service_deploy_frontend
- **Backend**: Deployed via service_deploy_backend
- **File Storage**: Local filesystem with organized structure
- **SSL**: Automatic HTTPS via deployment service

## Database Schema

### Users Table
```sql
- id (Primary Key)
- email (Unique)
- password_hash
- first_name
- last_name
- phone
- is_admin (Boolean)
- is_active (Boolean)
- created_at
- updated_at
```

### House Plans Table
```sql
- id (Primary Key)
- title
- description
- price
- bedrooms
- bathrooms
- stories
- garage_spaces
- square_footage
- style_category
- featured_image_url
- gallery_images (JSON array)
- plan_files (JSON array - PDF, DWG files)
- is_featured (Boolean)
- is_active (Boolean)
- created_at
- updated_at
- created_by (Foreign Key to Users)
```

### Categories Table
```sql
- id (Primary Key)
- name
- slug
- description
- image_url
- is_active (Boolean)
```

### Plan Categories (Many-to-Many)
```sql
- plan_id (Foreign Key)
- category_id (Foreign Key)
```

### Orders Table
```sql
- id (Primary Key)
- user_id (Foreign Key)
- order_number (Unique)
- status (pending, paid, completed, cancelled)
- total_amount
- payment_method
- payment_reference
- billing_address (JSON)
- created_at
- updated_at
```

### Order Items Table
```sql
- id (Primary Key)
- order_id (Foreign Key)
- plan_id (Foreign Key)
- quantity
- unit_price
- total_price
```

### Shopping Cart Table
```sql
- id (Primary Key)
- user_id (Foreign Key)
- plan_id (Foreign Key)
- quantity
- created_at
```

## Website Structure & Pages

### Public Pages
1. **Homepage**
   - Hero section with search
   - Featured house plans
   - Categories showcase
   - Customer testimonials
   - About Mzize Tradings

2. **House Plans Catalog**
   - Grid/list view toggle
   - Advanced filtering (price, bedrooms, style, etc.)
   - Search functionality
   - Pagination
   - Sort options

3. **Plan Detail Page**
   - High-quality image gallery
   - Detailed specifications
   - Floor plan images
   - 3D renderings (if available)
   - Add to cart functionality
   - Related plans

4. **Categories Page**
   - Browse by architectural style
   - Modern, Traditional, Contemporary, etc.

5. **About Us**
   - Company information
   - Team details
   - Contact information

6. **Contact**
   - Contact form
   - Business details
   - Location map

### User Account Pages
1. **Registration/Login**
   - Email/password authentication
   - Form validation
   - Password reset functionality

2. **User Dashboard**
   - Order history
   - Downloaded plans
   - Account settings
   - Wishlist

3. **Shopping Cart**
   - Cart items management
   - Quantity updates
   - Remove items
   - Proceed to checkout

4. **Checkout**
   - Billing information
   - Payment method selection
   - Order review
   - Payment processing

### Admin Panel
1. **Dashboard**
   - Sales analytics
   - Recent orders
   - Plan performance metrics

2. **Plans Management**
   - Add new plans
   - Edit existing plans
   - Upload images and files
   - Manage categories

3. **Orders Management**
   - View all orders
   - Update order status
   - Process refunds

4. **Users Management**
   - View registered users
   - Manage admin access

## Key Features

### Modern UI/UX Design
- Responsive design (mobile-first)
- Clean, professional layout
- High-quality imagery
- Smooth animations and transitions
- Intuitive navigation
- Fast loading times

### Search & Filtering
- Text search across plan titles and descriptions
- Filter by price range
- Filter by bedrooms/bathrooms
- Filter by square footage
- Filter by architectural style
- Sort by price, popularity, newest

### Shopping Cart & Checkout
- Persistent cart (logged-in users)
- Guest checkout option
- Multiple payment methods
- Secure payment processing
- Order confirmation emails
- Digital delivery of plans

### Admin Features
- Bulk plan upload
- Image optimization
- SEO-friendly URLs
- Analytics integration
- Content management

### South African Payment Integration
- PayFast integration (primary)
- Ozow instant EFT
- Credit/debit card processing
- ZAR currency support
- Local banking integration

## Security Features
- JWT-based authentication
- Password hashing (bcrypt)
- CSRF protection
- Input validation and sanitization
- Secure file uploads
- HTTPS enforcement
- Rate limiting

## Performance Optimizations
- Image lazy loading
- Code splitting
- CDN for static assets
- Database query optimization
- Caching strategies
- Minified assets

## SEO & Marketing
- SEO-friendly URLs
- Meta tags optimization
- Structured data markup
- Social media integration
- Google Analytics
- Sitemap generation

## File Organization
```
mzize-tradings-website/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── hooks/
│   │   ├── context/
│   │   ├── utils/
│   │   └── styles/
│   └── public/
├── backend/
│   ├── app/
│   │   ├── models/
│   │   ├── routes/
│   │   ├── utils/
│   │   └── config/
│   ├── uploads/
│   │   ├── plans/
│   │   └── images/
│   └── migrations/
└── docs/
```

## Development Phases
1. Setup project structure and basic React app
2. Implement Flask backend with database models
3. Create admin panel for plan management
4. Build shopping cart and checkout flow
5. Integrate South African payment systems
6. Testing and deployment
7. Documentation and handover

This architecture provides a solid foundation for a professional, scalable house plans e-commerce website tailored for the South African market.

