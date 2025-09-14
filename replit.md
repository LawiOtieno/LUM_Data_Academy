# LUM Data Academy Website

## Overview

This is a Django-based website for LUM Data Academy, an educational institution focused on equipping Africa with future-ready data skills. The platform serves as the primary digital presence for the academy, featuring course information, admissions processes, and institutional details. The website is designed to showcase various data science and analytics programs ranging from beginner to advanced levels, including Python, Power BI, R, AI tools, and cloud technologies.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Web Framework Architecture
The application is built using Django 5.2, following the Model-View-Template (MVT) pattern. This choice provides a robust, scalable foundation with built-in admin interface, ORM, and security features that are essential for an educational platform handling student registrations and course management.

### Static File Management
WhiteNoise middleware is integrated for efficient static file serving, eliminating the need for separate web servers in production. This simplifies deployment while maintaining performance for CSS, JavaScript, and media files like course PDFs and academy logos.

### Configuration Management
Environment-based configuration is implemented using Django's settings system with environment variable overrides for:
- Secret key management (DJANGO_SECRET_KEY)
- Debug mode control (DJANGO_DEBUG) 
- Host allowlist configuration (ALLOWED_HOSTS)

This approach ensures security best practices while maintaining flexibility across development, staging, and production environments.

### Security Architecture
The application includes Django's built-in security middleware stack:
- CSRF protection for form submissions (critical for registration and application forms)
- Session management for user authentication
- Security middleware for common web vulnerabilities protection

### URL Routing Structure
Django's URL dispatcher is configured to handle routing, with the admin interface already set up for content management. The architecture anticipates additional URL patterns for:
- Course catalog pages
- Registration and admissions workflows
- Public content pages (About, Homepage)

### Deployment Architecture
The WSGI/ASGI configuration supports both synchronous and asynchronous deployment scenarios, making it compatible with various hosting platforms and scaling requirements.

## Recent Changes

### September 14, 2025 - Replit Environment Setup
- Installed Python dependencies using uv package manager
- Fixed DEBUG configuration for development environment (DEBUG=True by default)
- Configured Gunicorn for production deployment with proper build steps
- Applied Django migrations and verified server startup
- Configured autoscale deployment with collectstatic build step

## External Dependencies

### Core Framework
- **Django 5.2**: Main web framework providing ORM, admin interface, security features, and template system
- **WhiteNoise**: Static file serving middleware for simplified deployment without separate web servers
- **Gunicorn**: Production WSGI server for deployment

### Infrastructure Requirements
- **Python Runtime**: Python 3.11 installed via Replit modules
- **Database**: SQLite for development (Django default), with architecture ready for PostgreSQL/MySQL in production
- **Email Services**: Configuration ready for SMTP integration for the specified email addresses (noreply@lumdataacademy.org, info@lumdataacademy.org, careers@lumdataacademy.org)

### Domain and Hosting
- **Domain**: lumdataacademy.org (as specified in requirements)
- **SSL/TLS**: Production deployment will require certificate management for secure communications
- **Static Asset Storage**: Local filesystem via WhiteNoise, with potential for cloud storage integration (AWS S3, Google Cloud Storage) for course materials and PDFs

### Future Integration Points
The architecture is prepared for:
- Payment gateway integration for course fees and payment plans
- Email marketing services for student communications
- File storage services for downloadable course PDFs
- Analytics platforms for tracking enrollment and engagement metrics