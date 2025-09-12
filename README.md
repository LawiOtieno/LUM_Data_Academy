
# LUM Data Academy 🎓

A modern, comprehensive Django-based learning management system for data science education, designed specifically for the African market.

## 🌟 Overview

LUM Data Academy is a cutting-edge online learning platform that empowers individuals and organisations across Africa with future-ready data skills. Our platform offers comprehensive courses in Data Science, Business Intelligence, Machine Learning, and more, delivered through an intuitive, modern web interface.

## 🚀 Key Features

### 📚 Course Management
- **Comprehensive Course Catalog**: Organized by skill levels (Beginner, Intermediate, Advanced, Masterclass)
- **Interactive Course Modules**: Detailed syllabus with code examples and exercises
- **Multi-currency Support**: KES, USD, and NGN with real-time conversion
- **Capstone Projects**: Industry-relevant projects for practical application
- **Course Resources**: PDFs, video introductions, and downloadable materials

### 👥 Student Experience
- **Modern User Registration**: Unified registration with email verification
- **Flexible Enrollment System**: Guest enrollment and authenticated user enrollment
- **Payment Flexibility**: Multiple payment methods (M-Pesa, PayPal, Bank Transfer)
- **Installment Plans**: 1, 2, or 3 installment payment options
- **Activation Codes**: Secure course access with unique activation codes
- **Progress Tracking**: Monitor enrollment status and payment progress

### 🎯 Content Management
- **Rich Text Editor**: Latest CKEditor 5 integration for all content fields
- **Blog System**: SEO-friendly blog with rich content support
- **Event Management**: Workshops, webinars, and academy events
- **Testimonials**: Student success stories and reviews
- **Career Portal**: Job opportunities with detailed descriptions
- **Survey System**: Feedback collection and market research tools

### 📱 Modern UI/UX
- **Responsive Design**: Mobile-first approach with Tailwind CSS
- **Professional Theme**: Blue and purple gradient design scheme
- **Interactive Elements**: Smooth animations and hover effects
- **Accessibility**: Screen reader friendly with proper semantic HTML
- **Fast Loading**: Optimized assets and efficient Django templates

### 🔧 Admin Features
- **Custom Admin Dashboard**: Modern, intuitive admin interface
- **Enhanced Data Management**: Inline editing and bulk operations
- **Email System**: Automated enrollment confirmations and course access emails
- **Payment Tracking**: Comprehensive enrollment and payment management
- **Content Publishing**: Easy-to-use forms for creating courses, blogs, and events

## 🛠 Technical Stack

### Backend
- **Django 5.1**: Modern Python web framework
- **Django CKEditor 5**: Rich text editing capabilities
- **SQLite**: Default database (easily configurable for PostgreSQL/MySQL)
- **Django Admin**: Enhanced administration interface

### Frontend
- **Tailwind CSS**: Utility-first CSS framework via CDN
- **Font Awesome**: Comprehensive icon library
- **Vanilla JavaScript**: Lightweight interactive elements
- **Responsive Design**: Mobile-first approach

### Infrastructure
- **Replit Hosting**: Cloud-based development and deployment
- **Email Service**: Django email backend for notifications
- **File Storage**: Django file handling for uploads
- **Static Files**: Efficient static file serving

## 📂 Project Structure

```
lumdataacademy/
├── accounts/              # User management and authentication
├── core/                  # Main application logic
│   ├── models.py         # Database models
│   ├── views.py          # View controllers
│   ├── urls.py           # URL routing
│   ├── admin.py          # Admin configurations
│   └── templates/        # HTML templates
├── emails/               # Email service integration
├── templates/            # Global templates
├── staticfiles/          # Static assets
└── manage.py            # Django management script
```

## 🔑 Core Models

### Course System
- **CourseCategory**: Organizes courses by difficulty level
- **Course**: Main course information with pricing and content
- **CourseModule**: Individual course sections
- **CodeExample**: Programming examples with syntax highlighting
- **Exercise**: Hands-on practice assignments
- **CapstoneProject**: Comprehensive final projects

### User Management
- **Enrollment**: Course registration with payment tracking
- **PaymentInstallment**: Flexible payment plan management
- **UserProfile**: Extended user information

### Content Management
- **BlogPost**: SEO-optimized blog articles
- **Event**: Workshops and webinars
- **Testimonial**: Student success stories
- **Career**: Job opportunity listings
- **Survey**: Feedback and research collection

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Django 5.1+
- Modern web browser

### Installation
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run migrations: `python manage.py migrate`
4. Create superuser: `python manage.py createsuperuser`
5. Start development server: `python manage.py runserver 0.0.0.0:5000`

### Default Access
- **Website**: http://localhost:5000
- **Admin Panel**: http://localhost:5000/admin

## 💰 Payment Integration

### Supported Methods
- **M-Pesa**: Kenya's leading mobile payment platform
- **PayPal**: International payment processing
- **Bank Transfer**: Direct bank account transfers

### Currency Support
- **KES**: Kenyan Shillings (primary)
- **USD**: US Dollars
- **NGN**: Nigerian Naira

### Payment Features
- Flexible installment plans (1, 2, or 3 payments)
- Automatic payment tracking
- Email notifications for payment confirmations
- Secure activation code system

## 📧 Email System

### Automated Emails
- Welcome emails for new users
- Enrollment confirmation with payment instructions
- Course access emails with activation codes
- Payment reminders for installments
- Newsletter subscriptions

## 👨‍💼 Admin Features

### Dashboard Highlights
- **Statistics Overview**: User, course, and enrollment metrics
- **Quick Actions**: Fast access to common tasks
- **Recent Activity**: Real-time platform activity
- **Modern Interface**: Intuitive and user-friendly

### Content Management
- **WYSIWYG Editor**: CKEditor 5 for rich content creation
- **Media Management**: Image and file upload capabilities
- **SEO Optimization**: Meta tags and URL management
- **Publishing Workflow**: Draft and publish states

## 🔒 Security Features

### Data Protection
- **CSRF Protection**: Cross-site request forgery prevention
- **User Authentication**: Secure login and registration
- **Email Verification**: Account activation via email
- **Payment Security**: Secure payment processing
- **Privacy Compliance**: GDPR-ready privacy policies

### Legal Pages
- **Terms of Service**: Comprehensive legal terms
- **Privacy Policy**: Data protection compliance
- **Payment Policy**: Clear payment terms and conditions
- **FAQs**: Common questions and answers

## 📱 Mobile Responsiveness

### Device Support
- **Desktop**: Full-featured experience
- **Tablet**: Optimized layout and navigation
- **Mobile**: Touch-friendly interface
- **Cross-browser**: Chrome, Firefox, Safari, Edge compatibility

## 🎨 Design System

### Color Palette
- **Primary**: Blue gradient (#3B82F6 to #1E40AF)
- **Secondary**: Purple accent (#8B5CF6)
- **Neutral**: Gray scale for text and backgrounds
- **Success**: Green for positive actions
- **Warning**: Yellow for alerts
- **Error**: Red for error states

### Typography
- **Headings**: Bold, clear hierarchy
- **Body Text**: Readable and accessible
- **Code**: Monospace font for technical content

## 🌍 Localization

### Regional Focus
- **Kenya**: Primary market with KES currency
- **Nigeria**: Secondary market with NGN support
- **Pan-African**: Designed for continental expansion

### Language Support
- **British English**: Standard for Kenya
- **Technical Terminology**: Industry-standard data science terms
- **Clear Communication**: Accessible language for all skill levels

## 📈 Analytics & Reporting

### Admin Insights
- **Enrollment Statistics**: Track course popularity
- **Payment Analytics**: Monitor revenue and payment patterns
- **User Engagement**: Activity and retention metrics
- **Content Performance**: Blog and course engagement

## 🤝 Community Features

### Student Interaction
- **Testimonials**: Share success stories
- **Career Portal**: Internal job opportunities
- **Survey System**: Feedback collection
- **Contact Forms**: Direct communication channels

## 🔧 Customization

### Theming
- **CSS Variables**: Easy color scheme modification
- **Component System**: Reusable UI components
- **Template Inheritance**: Consistent layout structure

### Configuration
- **Settings Management**: Environment-specific configurations
- **Email Templates**: Customizable email designs
- **Payment Methods**: Configurable payment options

## 📚 Educational Philosophy

### Learning Approach
- **Practical Focus**: Real-world applications
- **Industry Relevance**: Current technology stacks
- **Progressive Learning**: Structured skill development
- **Community Support**: Peer learning environment

### Course Quality
- **Expert Instructors**: Industry professionals
- **Updated Content**: Current best practices
- **Hands-on Projects**: Portfolio development
- **Career Guidance**: Job placement support

## 🛡 Compliance & Standards

### Legal Compliance
- **Kenyan Law**: Local regulatory compliance
- **Data Protection**: International privacy standards
- **Educational Standards**: Quality assurance
- **Payment Regulations**: Financial compliance

## 🚀 Future Roadmap

### Planned Features
- **Mobile App**: Native iOS and Android applications
- **Advanced Analytics**: Learning progress tracking
- **AI Integration**: Personalized learning paths
- **Certification System**: Accredited course completion
- **Enterprise Features**: Corporate training packages

## 📞 Support & Contact

### Technical Support
- **Documentation**: Comprehensive guides
- **Email Support**: Technical assistance
- **Community Forum**: Peer support
- **Video Tutorials**: Visual learning aids

### Business Inquiries
- **Partnership Opportunities**: Corporate collaborations
- **Custom Training**: Tailored educational programs
- **Consulting Services**: Data science expertise
- **Bulk Enrollment**: Group discounts

---

**LUM Data Academy** - Empowering Africa with Data Skills 🌍

*Built with ❤️ for the African data science community*
