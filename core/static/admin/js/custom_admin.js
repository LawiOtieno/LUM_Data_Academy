
// Enhanced Django Admin JavaScript for Gen-Z/Alpha/Beta Design
document.addEventListener('DOMContentLoaded', function() {
    // Initialize the enhanced admin interface
    initializeEnhancedAdmin();
    
    // Add dark theme toggle
    addThemeToggle();
    
    // Enhance navigation menus
    enhanceNavigationMenus();
    
    // Add right sidebar
    createRightSidebar();
    
    // Add mobile menu toggles
    addMobileMenuToggles();
    
    // Add loading animations
    addLoadingAnimations();
    
    // Add keyboard shortcuts
    addKeyboardShortcuts();
});

function initializeEnhancedAdmin() {
    // Add smooth scrolling
    document.documentElement.style.scrollBehavior = 'smooth';
    
    // Add enhanced animations
    const style = document.createElement('style');
    style.textContent = `
        .fade-in {
            animation: fadeIn 0.5s ease-in;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .slide-in-left {
            animation: slideInLeft 0.3s ease-out;
        }
        
        @keyframes slideInLeft {
            from { transform: translateX(-20px); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        
        .slide-in-right {
            animation: slideInRight 0.3s ease-out;
        }
        
        @keyframes slideInRight {
            from { transform: translateX(20px); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
    `;
    document.head.appendChild(style);
    
    // Apply animations to elements
    setTimeout(() => {
        const sidebar = document.querySelector('#nav-sidebar');
        if (sidebar) {
            sidebar.classList.add('slide-in-left');
        }
        
        const content = document.querySelector('.content');
        if (content) {
            content.classList.add('fade-in');
        }
    }, 100);
}

function enhanceNavigationMenus() {
    // Enhance left sidebar (Add menu)
    const leftSidebar = document.querySelector('#nav-sidebar');
    if (leftSidebar) {
        // Update menu links with better labels
        const addLinks = leftSidebar.querySelectorAll('a[href*="/add/"]');
        addLinks.forEach(link => {
            const href = link.getAttribute('href');
            let newText = link.textContent.trim();
            
            // Map model names to better labels
            const modelMappings = {
                'user': 'Add - User Account',
                'course': 'Add - Course',
                'blogpost': 'Add - Blog Post',
                'event': 'Add - Event',
                'testimonial': 'Add - Testimonial',
                'contact': 'Add - Contact Form',
                'newsletter': 'Add - Newsletter Subscriber',
                'enrollment': 'Add - Course Enrollment',
                'payment': 'Add - Payment Record',
                'userprofile': 'Add - User Profile',
                'mathcaptcha': 'Add - Math Captcha',
                'emailverificationtoken': 'Add - Email Verification Token',
                'passwordresettoken': 'Add - Password Reset Token',
                'coursemodule': 'Add - Course Module',
                'exercise': 'Add - Exercise',
                'codeexample': 'Add - Code Example',
                'capstoneproject': 'Add - Capstone Project',
                'coursecategory': 'Add - Course Category',
                'aboutpage': 'Add - About Page',
                'paymentinstallment': 'Add - Payment Installment'
            };
            
            // Check href for model name and update text
            for (const [model, label] of Object.entries(modelMappings)) {
                if (href.includes(model)) {
                    link.innerHTML = `<span class="add-icon">➕</span>${label}`;
                    break;
                }
            }
        });
        
        // Add header styling
        const header = leftSidebar.querySelector('.nav-header');
        if (!header) {
            const newHeader = document.createElement('div');
            newHeader.className = 'nav-header';
            newHeader.innerHTML = '➕ Quick Add Menu';
            leftSidebar.insertBefore(newHeader, leftSidebar.firstChild);
        }
    }
}

function createRightSidebar() {
    // Create right sidebar for View menu
    const rightSidebar = document.createElement('div');
    rightSidebar.id = 'nav-sidebar-right';
    rightSidebar.classList.add('slide-in-right');
    
    // Add header
    const header = document.createElement('div');
    header.className = 'nav-header';
    header.innerHTML = '👁️ Quick View Menu';
    rightSidebar.appendChild(header);
    
    // Create view menu items
    const viewMenus = [
        {
            category: 'User Management',
            items: [
                { name: 'View - All Users', url: '/admin/auth/user/', icon: '👥' },
                { name: 'View - User Profiles', url: '/admin/accounts/userprofile/', icon: '👤' },
                { name: 'View - User Groups', url: '/admin/auth/group/', icon: '👨‍👩‍👧‍👦' }
            ]
        },
        {
            category: 'Course Management',
            items: [
                { name: 'View - All Courses', url: '/admin/core/course/', icon: '📚' },
                { name: 'View - Course Categories', url: '/admin/core/coursecategory/', icon: '📂' },
                { name: 'View - Course Modules', url: '/admin/core/coursemodule/', icon: '📖' },
                { name: 'View - Enrollments', url: '/admin/core/enrollment/', icon: '🎯' }
            ]
        },
        {
            category: 'Content Management',
            items: [
                { name: 'View - Blog Posts', url: '/admin/core/blogpost/', icon: '📝' },
                { name: 'View - Events', url: '/admin/core/event/', icon: '📅' },
                { name: 'View - Testimonials', url: '/admin/core/testimonial/', icon: '⭐' }
            ]
        },
        {
            category: 'Communication',
            items: [
                { name: 'View - Contact Submissions', url: '/admin/core/contactsubmission/', icon: '📧' },
                { name: 'View - Newsletter Subscribers', url: '/admin/core/newsletter/', icon: '📰' }
            ]
        },
        {
            category: 'System & Security',
            items: [
                { name: 'View - Math Captchas', url: '/admin/accounts/mathcaptcha/', icon: '🔒' },
                { name: 'View - Email Tokens', url: '/admin/accounts/emailverificationtoken/', icon: '🔑' },
                { name: 'View - Reset Tokens', url: '/admin/accounts/passwordresettoken/', icon: '🔐' }
            ]
        }
    ];
    
    // Build menu structure
    viewMenus.forEach(category => {
        const module = document.createElement('div');
        module.className = 'module';
        
        const header = document.createElement('h2');
        header.textContent = category.category;
        module.appendChild(header);
        
        const table = document.createElement('table');
        const tbody = document.createElement('tbody');
        
        category.items.forEach(item => {
            const tr = document.createElement('tr');
            const td = document.createElement('td');
            const link = document.createElement('a');
            
            link.href = item.url;
            link.innerHTML = `<span class="view-icon">${item.icon}</span>${item.name}`;
            
            // Add hover effect
            link.addEventListener('mouseenter', function() {
                this.style.transform = 'translateX(-5px)';
            });
            
            link.addEventListener('mouseleave', function() {
                this.style.transform = 'translateX(0)';
            });
            
            td.appendChild(link);
            tr.appendChild(td);
            tbody.appendChild(tr);
        });
        
        table.appendChild(tbody);
        module.appendChild(table);
        rightSidebar.appendChild(module);
    });
    
    document.body.appendChild(rightSidebar);
}

function addThemeToggle() {
    const toggleButton = document.createElement('button');
    toggleButton.className = 'theme-toggle';
    toggleButton.innerHTML = '🌙';
    toggleButton.title = 'Toggle Dark Mode';
    
    toggleButton.addEventListener('click', function() {
        document.body.classList.toggle('dark-theme');
        
        // Update icon
        if (document.body.classList.contains('dark-theme')) {
            this.innerHTML = '☀️';
            localStorage.setItem('admin-theme', 'dark');
        } else {
            this.innerHTML = '🌙';
            localStorage.setItem('admin-theme', 'light');
        }
    });
    
    // Restore saved theme
    const savedTheme = localStorage.getItem('admin-theme');
    if (savedTheme === 'dark') {
        document.body.classList.add('dark-theme');
        toggleButton.innerHTML = '☀️';
    }
    
    document.body.appendChild(toggleButton);
}

function addLoadingAnimations() {
    // Add loading animation to forms
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            const submitButton = this.querySelector('input[type="submit"]');
            if (submitButton) {
                submitButton.innerHTML = '<span class="loading"></span> Processing...';
                submitButton.disabled = true;
            }
        });
    });
    
    // Add loading animation to links
    const links = document.querySelectorAll('a[href*="/admin/"]');
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            // Don't add loading for same-page anchors
            if (this.getAttribute('href').startsWith('#')) return;
            
            const loader = document.createElement('div');
            loader.style.cssText = `
                position: fixed;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                background: rgba(26, 54, 93, 0.9);
                color: white;
                padding: 20px 40px;
                border-radius: 10px;
                z-index: 10000;
                display: flex;
                align-items: center;
                gap: 10px;
                font-weight: 600;
            `;
            loader.innerHTML = '<span class="loading"></span> Loading...';
            
            document.body.appendChild(loader);
            
            // Remove loader after 3 seconds (fallback)
            setTimeout(() => {
                if (document.body.contains(loader)) {
                    document.body.removeChild(loader);
                }
            }, 3000);
        });
    });
}

function addKeyboardShortcuts() {
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + K for quick search
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            const searchInput = document.querySelector('#searchbar');
            if (searchInput) {
                searchInput.focus();
                searchInput.select();
            }
        }
        
        // Ctrl/Cmd + H for home
        if ((e.ctrlKey || e.metaKey) && e.key === 'h') {
            e.preventDefault();
            window.location.href = '/admin/';
        }
        
        // Ctrl/Cmd + L to toggle left sidebar (mobile)
        if ((e.ctrlKey || e.metaKey) && e.key === 'l') {
            e.preventDefault();
            const leftSidebar = document.querySelector('#nav-sidebar');
            if (leftSidebar) {
                leftSidebar.classList.toggle('mobile-show');
            }
        }
        
        // Ctrl/Cmd + R to toggle right sidebar (mobile)
        if ((e.ctrlKey || e.metaKey) && e.key === 'r') {
            e.preventDefault();
            const rightSidebar = document.querySelector('#nav-sidebar-right');
            if (rightSidebar) {
                rightSidebar.classList.toggle('mobile-show');
            }
        }
    });
}

function addMobileMenuToggles() {
    // Only add mobile toggles on small screens
    if (window.innerWidth <= 768) {
        // Left menu toggle
        const leftToggle = document.createElement('button');
        leftToggle.className = 'mobile-menu-toggle left';
        leftToggle.innerHTML = '➕';
        leftToggle.title = 'Toggle Add Menu';
        
        leftToggle.addEventListener('click', function() {
            const leftSidebar = document.querySelector('#nav-sidebar');
            if (leftSidebar) {
                leftSidebar.classList.toggle('mobile-show');
            }
        });
        
        // Right menu toggle
        const rightToggle = document.createElement('button');
        rightToggle.className = 'mobile-menu-toggle right';
        rightToggle.innerHTML = '👁️';
        rightToggle.title = 'Toggle View Menu';
        
        rightToggle.addEventListener('click', function() {
            const rightSidebar = document.querySelector('#nav-sidebar-right');
            if (rightSidebar) {
                rightSidebar.classList.toggle('mobile-show');
            }
        });
        
        document.body.appendChild(leftToggle);
        document.body.appendChild(rightToggle);
    }
}

// Update initialization to include mobile toggles
window.addEventListener('resize', function() {
    // Remove existing toggles
    const existingToggles = document.querySelectorAll('.mobile-menu-toggle');
    existingToggles.forEach(toggle => toggle.remove());
    
    // Re-add if needed
    addMobileMenuToggles();
});

// Add notification system
function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 90px;
        right: 20px;
        background: ${type === 'success' ? 'linear-gradient(135deg, #2ecc71 0%, #27ae60 100%)' : 'linear-gradient(135deg, #e74c3c 0%, #c0392b 100%)'};
        color: white;
        padding: 15px 25px;
        border-radius: 10px;
        z-index: 10001;
        font-weight: 600;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
        transform: translateX(100%);
        transition: transform 0.3s ease;
    `;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    // Slide in
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    // Slide out and remove
    setTimeout(() => {
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => {
            if (document.body.contains(notification)) {
                document.body.removeChild(notification);
            }
        }, 300);
    }, 3000);
}

// Enhanced table interactions
document.addEventListener('DOMContentLoaded', function() {
    const tables = document.querySelectorAll('table.results');
    tables.forEach(table => {
        const rows = table.querySelectorAll('tbody tr');
        rows.forEach(row => {
            row.addEventListener('mouseenter', function() {
                this.style.transform = 'scale(1.01)';
                this.style.zIndex = '10';
            });
            
            row.addEventListener('mouseleave', function() {
                this.style.transform = 'scale(1)';
                this.style.zIndex = '1';
            });
        });
    });
});
