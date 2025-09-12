
// Custom Django Admin JavaScript - Modern Interactive Features

document.addEventListener('DOMContentLoaded', function() {
    // Add mobile menu toggle
    addMobileMenuToggle();
    
    // Add theme toggle
    addThemeToggle();
    
    // Add search functionality
    enhanceSearch();
    
    // Add smooth scrolling
    addSmoothScrolling();
    
    // Add loading states
    addLoadingStates();
    
    // Add tooltips
    addTooltips();
    
    // Add keyboard shortcuts
    addKeyboardShortcuts();
});

function addMobileMenuToggle() {
    const header = document.getElementById('header');
    const sidebar = document.getElementById('nav-sidebar');
    
    if (!header || !sidebar) return;
    
    // Create mobile menu toggle button
    const toggleBtn = document.createElement('button');
    toggleBtn.innerHTML = '☰';
    toggleBtn.className = 'mobile-menu-toggle';
    toggleBtn.style.cssText = `
        display: none;
        background: none;
        border: none;
        color: white;
        font-size: 24px;
        cursor: pointer;
        padding: 10px;
        border-radius: 5px;
        transition: all 0.3s ease;
    `;
    
    // Add toggle functionality
    toggleBtn.addEventListener('click', function() {
        sidebar.classList.toggle('show');
        document.body.style.overflow = sidebar.classList.contains('show') ? 'hidden' : '';
    });
    
    header.insertBefore(toggleBtn, header.firstChild);
    
    // Show on mobile
    const mediaQuery = window.matchMedia('(max-width: 768px)');
    function handleMobile(e) {
        toggleBtn.style.display = e.matches ? 'block' : 'none';
        if (!e.matches) {
            sidebar.classList.remove('show');
            document.body.style.overflow = '';
        }
    }
    mediaQuery.addListener(handleMobile);
    handleMobile(mediaQuery);
}

function addThemeToggle() {
    const toggleBtn = document.createElement('button');
    toggleBtn.innerHTML = '🌙';
    toggleBtn.className = 'theme-toggle';
    toggleBtn.title = 'Toggle Dark Mode';
    
    toggleBtn.addEventListener('click', function() {
        document.body.classList.toggle('dark-theme');
        toggleBtn.innerHTML = document.body.classList.contains('dark-theme') ? '☀️' : '🌙';
        
        // Save preference
        localStorage.setItem('admin-theme', document.body.classList.contains('dark-theme') ? 'dark' : 'light');
    });
    
    // Load saved theme
    const savedTheme = localStorage.getItem('admin-theme');
    if (savedTheme === 'dark') {
        document.body.classList.add('dark-theme');
        toggleBtn.innerHTML = '☀️';
    }
    
    document.body.appendChild(toggleBtn);
}

function enhanceSearch() {
    const searchInput = document.getElementById('searchbar');
    if (!searchInput) return;
    
    // Add search icon
    const searchContainer = document.createElement('div');
    searchContainer.style.cssText = `
        position: relative;
        display: inline-block;
        width: 100%;
        max-width: 400px;
    `;
    
    const searchIcon = document.createElement('span');
    searchIcon.innerHTML = '🔍';
    searchIcon.style.cssText = `
        position: absolute;
        right: 15px;
        top: 50%;
        transform: translateY(-50%);
        font-size: 16px;
        pointer-events: none;
    `;
    
    searchInput.parentNode.insertBefore(searchContainer, searchInput);
    searchContainer.appendChild(searchInput);
    searchContainer.appendChild(searchIcon);
    
    // Add real-time search feedback
    searchInput.addEventListener('input', function() {
        if (this.value.length > 0) {
            searchIcon.innerHTML = '❌';
            searchIcon.style.cursor = 'pointer';
            searchIcon.style.pointerEvents = 'auto';
            searchIcon.onclick = () => {
                searchInput.value = '';
                searchIcon.innerHTML = '🔍';
                searchIcon.style.pointerEvents = 'none';
            };
        } else {
            searchIcon.innerHTML = '🔍';
            searchIcon.style.pointerEvents = 'none';
        }
    });
}

function addSmoothScrolling() {
    const links = document.querySelectorAll('a[href^="#"]');
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

function addLoadingStates() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            const submitBtn = form.querySelector('input[type="submit"], button[type="submit"]');
            if (submitBtn) {
                const originalText = submitBtn.value || submitBtn.textContent;
                submitBtn.innerHTML = '<span class="loading"></span> Processing...';
                submitBtn.disabled = true;
                
                // Re-enable after 5 seconds as fallback
                setTimeout(() => {
                    submitBtn.innerHTML = originalText;
                    submitBtn.disabled = false;
                }, 5000);
            }
        });
    });
}

function addTooltips() {
    const elements = document.querySelectorAll('[title]');
    elements.forEach(element => {
        element.addEventListener('mouseenter', function() {
            const tooltip = document.createElement('div');
            tooltip.textContent = this.title;
            tooltip.className = 'custom-tooltip';
            tooltip.style.cssText = `
                position: absolute;
                background: #2c3e50;
                color: white;
                padding: 8px 12px;
                border-radius: 6px;
                font-size: 14px;
                z-index: 1002;
                pointer-events: none;
                opacity: 0;
                transition: opacity 0.3s ease;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
            `;
            
            document.body.appendChild(tooltip);
            
            const rect = this.getBoundingClientRect();
            tooltip.style.left = rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2) + 'px';
            tooltip.style.top = rect.top - tooltip.offsetHeight - 10 + 'px';
            
            setTimeout(() => tooltip.style.opacity = '1', 100);
            
            this.addEventListener('mouseleave', function() {
                tooltip.style.opacity = '0';
                setTimeout(() => {
                    if (tooltip.parentNode) {
                        tooltip.parentNode.removeChild(tooltip);
                    }
                }, 300);
            }, { once: true });
            
            // Remove title to prevent default tooltip
            this.setAttribute('data-title', this.title);
            this.removeAttribute('title');
        });
        
        element.addEventListener('mouseleave', function() {
            if (this.getAttribute('data-title')) {
                this.title = this.getAttribute('data-title');
                this.removeAttribute('data-title');
            }
        });
    });
}

function addKeyboardShortcuts() {
    document.addEventListener('keydown', function(e) {
        // Alt + N for Add New
        if (e.altKey && e.key === 'n') {
            e.preventDefault();
            const addLink = document.querySelector('.addlink');
            if (addLink) addLink.click();
        }
        
        // Alt + S for Save
        if (e.altKey && e.key === 's') {
            e.preventDefault();
            const saveBtn = document.querySelector('input[name="_save"], button[name="_save"]');
            if (saveBtn) saveBtn.click();
        }
        
        // Alt + H for Home
        if (e.altKey && e.key === 'h') {
            e.preventDefault();
            window.location.href = '/admin/';
        }
        
        // Escape to close mobile menu
        if (e.key === 'Escape') {
            const sidebar = document.getElementById('nav-sidebar');
            if (sidebar && sidebar.classList.contains('show')) {
                sidebar.classList.remove('show');
                document.body.style.overflow = '';
            }
        }
    });
}

// Add notification system
function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 90px;
        right: 30px;
        background: ${type === 'success' ? '#2ecc71' : type === 'error' ? '#e74c3c' : '#f39c12'};
        color: white;
        padding: 15px 20px;
        border-radius: 10px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
        z-index: 1003;
        font-weight: 500;
        transform: translateX(100%);
        transition: transform 0.3s ease;
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    setTimeout(() => {
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }, 4000);
}

// Expose for external use
window.adminUtils = {
    showNotification
};
