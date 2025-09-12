
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
    
    // Add sidebar toggles
    addSidebarToggles();
    
    // Add analytics dashboard
    addAnalyticsDashboard();
    
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

function addSidebarToggles() {
    // Left sidebar toggle
    const leftToggle = document.createElement('button');
    leftToggle.className = 'sidebar-toggle left';
    leftToggle.innerHTML = '➕';
    leftToggle.title = 'Toggle Add Menu';
    
    leftToggle.addEventListener('click', function() {
        const leftSidebar = document.querySelector('#nav-sidebar');
        const content = document.querySelector('.content');
        const rightSidebar = document.querySelector('#nav-sidebar-right');
        
        if (leftSidebar && content) {
            const isExpanded = leftSidebar.classList.contains('expanded');
            
            if (isExpanded) {
                leftSidebar.classList.remove('expanded');
                this.innerHTML = '➕';
                content.classList.remove('left-expanded', 'both-expanded');
                if (rightSidebar && rightSidebar.classList.contains('expanded')) {
                    content.classList.add('right-expanded');
                }
            } else {
                leftSidebar.classList.add('expanded');
                this.innerHTML = '❌';
                content.classList.add('left-expanded');
                if (rightSidebar && rightSidebar.classList.contains('expanded')) {
                    content.classList.remove('right-expanded');
                    content.classList.add('both-expanded');
                }
            }
        }
    });
    
    // Right sidebar toggle
    const rightToggle = document.createElement('button');
    rightToggle.className = 'sidebar-toggle right';
    rightToggle.innerHTML = '👁️';
    rightToggle.title = 'Toggle View Menu';
    
    rightToggle.addEventListener('click', function() {
        const rightSidebar = document.querySelector('#nav-sidebar-right');
        const content = document.querySelector('.content');
        const leftSidebar = document.querySelector('#nav-sidebar');
        
        if (rightSidebar && content) {
            const isExpanded = rightSidebar.classList.contains('expanded');
            
            if (isExpanded) {
                rightSidebar.classList.remove('expanded');
                this.innerHTML = '👁️';
                content.classList.remove('right-expanded', 'both-expanded');
                if (leftSidebar && leftSidebar.classList.contains('expanded')) {
                    content.classList.add('left-expanded');
                }
            } else {
                rightSidebar.classList.add('expanded');
                this.innerHTML = '❌';
                content.classList.add('right-expanded');
                if (leftSidebar && leftSidebar.classList.contains('expanded')) {
                    content.classList.remove('left-expanded');
                    content.classList.add('both-expanded');
                }
            }
        }
    });
    
    document.body.appendChild(leftToggle);
    document.body.appendChild(rightToggle);
}

function addAnalyticsDashboard() {
    // Only add to the main admin index page
    if (window.location.pathname === '/admin/' || window.location.pathname.endsWith('/admin/')) {
        const content = document.querySelector('.content');
        if (content) {
            const analyticsSection = document.createElement('div');
            analyticsSection.className = 'analytics-dashboard';
            
            // Users Analytics Chart
            const usersCard = createAnalyticsCard('📊 User Analytics', 'users-chart');
            usersCard.querySelector('h3').style.setProperty('--before-content', '"📊"', 'important');
            
            // Course Enrollment Chart
            const enrollmentCard = createAnalyticsCard('📈 Course Enrollments', 'enrollment-chart');
            enrollmentCard.querySelector('h3').style.setProperty('--before-content', '"📈"', 'important');
            
            // Revenue Analytics
            const revenueCard = createAnalyticsCard('💰 Revenue Analytics', 'revenue-chart');
            revenueCard.querySelector('h3').style.setProperty('--before-content', '"💰"', 'important');
            
            // Activity Overview
            const activityCard = createAnalyticsCard('⚡ Activity Overview', 'activity-chart');
            activityCard.querySelector('h3').style.setProperty('--before-content', '"⚡"', 'important');
            
            analyticsSection.appendChild(usersCard);
            analyticsSection.appendChild(enrollmentCard);
            analyticsSection.appendChild(revenueCard);
            analyticsSection.appendChild(activityCard);
            
            // Insert before existing modules
            const firstModule = content.querySelector('.module');
            if (firstModule) {
                content.insertBefore(analyticsSection, firstModule);
            } else {
                content.appendChild(analyticsSection);
            }
            
            // Initialize charts with sample data
            initializeCharts();
        }
    }
}

function createAnalyticsCard(title, chartId) {
    const card = document.createElement('div');
    card.className = 'analytics-card';
    
    const header = document.createElement('h3');
    header.textContent = title;
    
    const chartContainer = document.createElement('div');
    chartContainer.className = 'chart-container';
    chartContainer.id = chartId;
    
    const placeholder = document.createElement('div');
    placeholder.className = 'chart-placeholder';
    placeholder.textContent = 'Loading Analytics...';
    
    chartContainer.appendChild(placeholder);
    card.appendChild(header);
    card.appendChild(chartContainer);
    
    return card;
}

function initializeCharts() {
    // Simulate chart initialization with placeholders
    setTimeout(() => {
        initializeUsersChart();
        initializeEnrollmentChart();
        initializeRevenueChart();
        initializeActivityChart();
    }, 500);
}

function initializeUsersChart() {
    const container = document.getElementById('users-chart');
    if (container) {
        container.innerHTML = createSimpleBarChart([
            {label: 'Jan', value: 45},
            {label: 'Feb', value: 52},
            {label: 'Mar', value: 67},
            {label: 'Apr', value: 73},
            {label: 'May', value: 89},
            {label: 'Jun', value: 95}
        ], 'New Users Per Month');
    }
}

function initializeEnrollmentChart() {
    const container = document.getElementById('enrollment-chart');
    if (container) {
        container.innerHTML = createPieChart([
            {label: 'Python Fundamentals', value: 35, color: '#3182ce'},
            {label: 'Data Science', value: 28, color: '#2ecc71'},
            {label: 'Machine Learning', value: 22, color: '#e74c3c'},
            {label: 'Web Development', value: 15, color: '#f39c12'}
        ], 'Course Enrollments Distribution');
    }
}

function initializeRevenueChart() {
    const container = document.getElementById('revenue-chart');
    if (container) {
        container.innerHTML = createLineChart([
            {month: 'Jan', amount: 12500},
            {month: 'Feb', amount: 15200},
            {month: 'Mar', amount: 18900},
            {month: 'Apr', amount: 22100},
            {month: 'May', amount: 25600},
            {month: 'Jun', amount: 28300}
        ], 'Monthly Revenue (KES)');
    }
}

function initializeActivityChart() {
    const container = document.getElementById('activity-chart');
    if (container) {
        container.innerHTML = createDonutChart([
            {label: 'Active Users', value: 68, color: '#2ecc71'},
            {label: 'Inactive Users', value: 32, color: '#95a5a6'}
        ], 'User Activity Status');
    }
}

function createSimpleBarChart(data, title) {
    const maxValue = Math.max(...data.map(d => d.value));
    
    return `
        <div style="padding: 20px;">
            <h4 style="text-align: center; margin-bottom: 20px; color: #495057; font-size: 14px;">${title}</h4>
            <div style="display: flex; align-items: end; justify-content: space-between; height: 200px;">
                ${data.map(item => `
                    <div style="display: flex; flex-direction: column; align-items: center; flex: 1;">
                        <div style="
                            background: linear-gradient(135deg, #3182ce 0%, #2c5282 100%);
                            width: 30px;
                            height: ${(item.value / maxValue) * 150}px;
                            margin-bottom: 10px;
                            border-radius: 4px 4px 0 0;
                            position: relative;
                        ">
                            <span style="
                                position: absolute;
                                top: -25px;
                                left: 50%;
                                transform: translateX(-50%);
                                font-size: 12px;
                                font-weight: 600;
                                color: #495057;
                            ">${item.value}</span>
                        </div>
                        <span style="font-size: 11px; color: #6c757d; font-weight: 500;">${item.label}</span>
                    </div>
                `).join('')}
            </div>
        </div>
    `;
}

function createPieChart(data, title) {
    const total = data.reduce((sum, item) => sum + item.value, 0);
    let currentAngle = 0;
    
    const slices = data.map(item => {
        const percentage = (item.value / total) * 100;
        const angle = (item.value / total) * 360;
        const slice = {
            ...item,
            percentage: percentage.toFixed(1),
            startAngle: currentAngle,
            endAngle: currentAngle + angle
        };
        currentAngle += angle;
        return slice;
    });
    
    return `
        <div style="padding: 20px;">
            <h4 style="text-align: center; margin-bottom: 20px; color: #495057; font-size: 14px;">${title}</h4>
            <div style="display: flex; align-items: center; gap: 20px;">
                <svg width="150" height="150" style="transform: rotate(-90deg);">
                    ${slices.map(slice => {
                        const x1 = 75 + 60 * Math.cos(slice.startAngle * Math.PI / 180);
                        const y1 = 75 + 60 * Math.sin(slice.startAngle * Math.PI / 180);
                        const x2 = 75 + 60 * Math.cos(slice.endAngle * Math.PI / 180);
                        const y2 = 75 + 60 * Math.sin(slice.endAngle * Math.PI / 180);
                        const largeArc = slice.endAngle - slice.startAngle > 180 ? 1 : 0;
                        
                        return `
                            <path d="M 75 75 L ${x1} ${y1} A 60 60 0 ${largeArc} 1 ${x2} ${y2} Z"
                                  fill="${slice.color}" stroke="white" stroke-width="2"/>
                        `;
                    }).join('')}
                </svg>
                <div style="flex: 1;">
                    ${slices.map(slice => `
                        <div style="display: flex; align-items: center; margin-bottom: 8px;">
                            <div style="width: 12px; height: 12px; background: ${slice.color}; border-radius: 2px; margin-right: 8px;"></div>
                            <span style="font-size: 12px; color: #495057;">${slice.label}: ${slice.percentage}%</span>
                        </div>
                    `).join('')}
                </div>
            </div>
        </div>
    `;
}

function createLineChart(data, title) {
    const maxAmount = Math.max(...data.map(d => d.amount));
    const minAmount = Math.min(...data.map(d => d.amount));
    const range = maxAmount - minAmount;
    
    return `
        <div style="padding: 20px;">
            <h4 style="text-align: center; margin-bottom: 20px; color: #495057; font-size: 14px;">${title}</h4>
            <svg width="100%" height="200" style="overflow: visible;">
                <defs>
                    <linearGradient id="lineGradient" x1="0%" y1="0%" x2="0%" y2="100%">
                        <stop offset="0%" style="stop-color:#3182ce;stop-opacity:0.3" />
                        <stop offset="100%" style="stop-color:#3182ce;stop-opacity:0" />
                    </linearGradient>
                </defs>
                ${data.map((point, index) => {
                    const x = (index / (data.length - 1)) * 250 + 25;
                    const y = 180 - ((point.amount - minAmount) / range) * 150;
                    return `
                        <circle cx="${x}" cy="${y}" r="4" fill="#3182ce"/>
                        <text x="${x}" y="${y - 10}" text-anchor="middle" font-size="10" fill="#495057">KES ${(point.amount / 1000).toFixed(0)}K</text>
                        <text x="${x}" y="195" text-anchor="middle" font-size="10" fill="#6c757d">${point.month}</text>
                    `;
                }).join('')}
                <polyline
                    fill="none"
                    stroke="#3182ce"
                    stroke-width="3"
                    points="${data.map((point, index) => {
                        const x = (index / (data.length - 1)) * 250 + 25;
                        const y = 180 - ((point.amount - minAmount) / range) * 150;
                        return `${x},${y}`;
                    }).join(' ')}"
                />
            </svg>
        </div>
    `;
}

function createDonutChart(data, title) {
    const total = data.reduce((sum, item) => sum + item.value, 0);
    let currentAngle = 0;
    
    const slices = data.map(item => {
        const percentage = (item.value / total) * 100;
        const angle = (item.value / total) * 360;
        const slice = {
            ...item,
            percentage: percentage.toFixed(1),
            startAngle: currentAngle,
            endAngle: currentAngle + angle
        };
        currentAngle += angle;
        return slice;
    });
    
    return `
        <div style="padding: 20px;">
            <h4 style="text-align: center; margin-bottom: 20px; color: #495057; font-size: 14px;">${title}</h4>
            <div style="display: flex; align-items: center; gap: 20px;">
                <svg width="150" height="150" style="transform: rotate(-90deg);">
                    ${slices.map(slice => {
                        const x1 = 75 + 60 * Math.cos(slice.startAngle * Math.PI / 180);
                        const y1 = 75 + 60 * Math.sin(slice.startAngle * Math.PI / 180);
                        const x2 = 75 + 60 * Math.cos(slice.endAngle * Math.PI / 180);
                        const y2 = 75 + 60 * Math.sin(slice.endAngle * Math.PI / 180);
                        const largeArc = slice.endAngle - slice.startAngle > 180 ? 1 : 0;
                        
                        const innerX1 = 75 + 25 * Math.cos(slice.startAngle * Math.PI / 180);
                        const innerY1 = 75 + 25 * Math.sin(slice.startAngle * Math.PI / 180);
                        const innerX2 = 75 + 25 * Math.cos(slice.endAngle * Math.PI / 180);
                        const innerY2 = 75 + 25 * Math.sin(slice.endAngle * Math.PI / 180);
                        
                        return `
                            <path d="M ${x1} ${y1} A 60 60 0 ${largeArc} 1 ${x2} ${y2} L ${innerX2} ${innerY2} A 25 25 0 ${largeArc} 0 ${innerX1} ${innerY1} Z"
                                  fill="${slice.color}" stroke="white" stroke-width="2"/>
                        `;
                    }).join('')}
                    <text x="75" y="75" text-anchor="middle" dy="0.3em" 
                          style="font-size: 20px; font-weight: bold; fill: #495057; transform: rotate(90deg); transform-origin: 75px 75px;">
                        ${data[0].value}%
                    </text>
                </svg>
                <div style="flex: 1;">
                    ${slices.map(slice => `
                        <div style="display: flex; align-items: center; margin-bottom: 8px;">
                            <div style="width: 12px; height: 12px; background: ${slice.color}; border-radius: 2px; margin-right: 8px;"></div>
                            <span style="font-size: 12px; color: #495057;">${slice.label}: ${slice.percentage}%</span>
                        </div>
                    `).join('')}
                </div>
            </div>
        </div>
    `;
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
        
        // Ctrl/Cmd + L to toggle left sidebar
        if ((e.ctrlKey || e.metaKey) && e.key === 'l') {
            e.preventDefault();
            const leftToggle = document.querySelector('.sidebar-toggle.left');
            if (leftToggle) {
                leftToggle.click();
            }
        }
        
        // Ctrl/Cmd + R to toggle right sidebar
        if ((e.ctrlKey || e.metaKey) && e.key === 'r') {
            e.preventDefault();
            const rightToggle = document.querySelector('.sidebar-toggle.right');
            if (rightToggle) {
                rightToggle.click();
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
