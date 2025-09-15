/* ========================================================================
   LUM Data Academy - Material Dashboard 2 Admin JavaScript
   Enhanced interactions, animations, and functionality
   ======================================================================== */

document.addEventListener('DOMContentLoaded', function() {
    
    // ========================================================================
    // Enhanced Sidebar Toggle with Accessibility
    // ========================================================================
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebar = document.getElementById('adminSidebar');
    const content = document.getElementById('content');
    
    if (sidebarToggle && sidebar) {
        // Add ARIA attributes to sidebar elements
        sidebar.setAttribute('role', 'navigation');
        sidebar.setAttribute('aria-label', 'Main navigation');
        sidebar.setAttribute('aria-hidden', 'false');
        
        sidebarToggle.setAttribute('aria-label', 'Toggle navigation menu');
        sidebarToggle.setAttribute('aria-expanded', 'true');
        sidebarToggle.setAttribute('aria-controls', 'adminSidebar');
        
        // Make sidebar items focusable and add ARIA attributes
        const sidebarItems = sidebar.querySelectorAll('.sidebar-item');
        sidebarItems.forEach((item, index) => {
            if (!item.hasAttribute('tabindex')) {
                item.setAttribute('tabindex', '0');
            }
            item.setAttribute('role', 'menuitem');
            
            // Add keyboard navigation for sidebar items
            item.addEventListener('keydown', function(e) {
                switch (e.key) {
                    case 'Enter':
                    case ' ':
                        e.preventDefault();
                        item.click();
                        break;
                    case 'ArrowDown':
                        e.preventDefault();
                        const nextItem = sidebarItems[Math.min(index + 1, sidebarItems.length - 1)];
                        nextItem.focus();
                        break;
                    case 'ArrowUp':
                        e.preventDefault();
                        const prevItem = sidebarItems[Math.max(index - 1, 0)];
                        prevItem.focus();
                        break;
                    case 'Home':
                        e.preventDefault();
                        sidebarItems[0].focus();
                        break;
                    case 'End':
                        e.preventDefault();
                        sidebarItems[sidebarItems.length - 1].focus();
                        break;
                }
            });
        });
        
        function toggleSidebar(show = null) {
            const isOpen = sidebar.classList.contains('active');
            const shouldShow = show !== null ? show : !isOpen;
            const isMobile = window.innerWidth <= 1024;
            
            if (isMobile) {
                sidebar.classList.toggle('active', shouldShow);
                sidebar.setAttribute('aria-hidden', (!shouldShow).toString());
                sidebarToggle.setAttribute('aria-expanded', shouldShow.toString());
                
                if (shouldShow) {
                    // Create overlay
                    const overlay = document.createElement('div');
                    overlay.className = 'sidebar-overlay';
                    overlay.setAttribute('role', 'button');
                    overlay.setAttribute('aria-label', 'Close navigation menu');
                    overlay.setAttribute('tabindex', '0');
                    overlay.style.cssText = `
                        position: fixed;
                        top: 0;
                        left: 0;
                        width: 100%;
                        height: 100%;
                        background: rgba(0, 0, 0, 0.5);
                        z-index: 998;
                        opacity: 0;
                        transition: opacity 0.3s ease;
                    `;
                    document.body.appendChild(overlay);
                    
                    // Animate overlay
                    requestAnimationFrame(() => {
                        overlay.style.opacity = '1';
                    });
                    
                    // Close sidebar when overlay is clicked or activated
                    function closeOverlay() {
                        sidebar.classList.remove('active');
                        sidebar.setAttribute('aria-hidden', 'true');
                        sidebarToggle.setAttribute('aria-expanded', 'false');
                        overlay.style.opacity = '0';
                        setTimeout(() => {
                            if (overlay.parentNode) {
                                overlay.parentNode.removeChild(overlay);
                            }
                        }, 300);
                        sidebarToggle.focus(); // Return focus to toggle button
                    }
                    
                    overlay.addEventListener('click', closeOverlay);
                    overlay.addEventListener('keydown', (e) => {
                        if (e.key === 'Enter' || e.key === ' ') {
                            e.preventDefault();
                            closeOverlay();
                        }
                    });
                    
                    // Focus first sidebar item when opened
                    setTimeout(() => {
                        if (sidebarItems.length > 0) {
                            sidebarItems[0].focus();
                        }
                    }, 100);
                } else {
                    // Remove overlay
                    const overlay = document.querySelector('.sidebar-overlay');
                    if (overlay) {
                        overlay.style.opacity = '0';
                        setTimeout(() => {
                            if (overlay.parentNode) {
                                overlay.parentNode.removeChild(overlay);
                            }
                        }, 300);
                    }
                }
            } else {
                // Desktop behavior - no overlay needed
                sidebar.setAttribute('aria-hidden', 'false');
                sidebarToggle.setAttribute('aria-expanded', 'true');
            }
        }
        
        // Click handler for sidebar toggle
        sidebarToggle.addEventListener('click', function() {
            toggleSidebar();
        });
        
        // Keyboard handler for sidebar toggle
        sidebarToggle.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                toggleSidebar();
            }
        });
        
        // Handle window resize to reset sidebar state properly
        window.addEventListener('resize', function() {
            if (window.innerWidth > 1024) {
                // Reset to desktop state
                sidebar.classList.remove('active');
                sidebar.setAttribute('aria-hidden', 'false');
                sidebarToggle.setAttribute('aria-expanded', 'true');
                
                // Remove any overlay
                const overlay = document.querySelector('.sidebar-overlay');
                if (overlay && overlay.parentNode) {
                    overlay.parentNode.removeChild(overlay);
                }
            }
        });
    }
    
    // ========================================================================
    // Accessible User Dropdown
    // ========================================================================
    const userMenu = document.querySelector('.user-menu');
    const userInfo = document.querySelector('.user-info');
    const userDropdown = document.querySelector('.user-dropdown');
    
    if (userMenu && userInfo && userDropdown) {
        // Make user-info focusable
        userInfo.setAttribute('tabindex', '0');
        userInfo.setAttribute('role', 'button');
        userInfo.setAttribute('aria-expanded', 'false');
        userInfo.setAttribute('aria-haspopup', 'true');
        userInfo.setAttribute('aria-label', 'User account menu');
        
        // Set up dropdown
        userDropdown.setAttribute('role', 'menu');
        userDropdown.setAttribute('aria-hidden', 'true');
        
        // Add ARIA labels to dropdown items
        const dropdownItems = userDropdown.querySelectorAll('.dropdown-item');
        dropdownItems.forEach(item => {
            item.setAttribute('role', 'menuitem');
        });
        
        function toggleUserDropdown(show = null) {
            const isOpen = userMenu.classList.contains('active');
            const shouldShow = show !== null ? show : !isOpen;
            
            userMenu.classList.toggle('active', shouldShow);
            userInfo.setAttribute('aria-expanded', shouldShow.toString());
            userDropdown.setAttribute('aria-hidden', (!shouldShow).toString());
            
            if (shouldShow) {
                // Focus first dropdown item when opened with keyboard
                const firstItem = userDropdown.querySelector('.dropdown-item');
                if (firstItem && document.activeElement === userInfo) {
                    setTimeout(() => firstItem.focus(), 100);
                }
            }
        }
        
        // Click handler
        userInfo.addEventListener('click', (e) => {
            e.stopPropagation();
            toggleUserDropdown();
        });
        
        // Keyboard handler
        userInfo.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                toggleUserDropdown();
            } else if (e.key === 'Escape') {
                toggleUserDropdown(false);
            }
        });
        
        // Close dropdown when clicking outside
        document.addEventListener('click', (e) => {
            if (!userMenu.contains(e.target)) {
                toggleUserDropdown(false);
            }
        });
        
        // Handle escape key to close dropdown
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && userMenu.classList.contains('active')) {
                toggleUserDropdown(false);
                userInfo.focus();
            }
        });
        
        // Arrow key navigation within dropdown
        userDropdown.addEventListener('keydown', (e) => {
            const items = Array.from(userDropdown.querySelectorAll('.dropdown-item'));
            const currentIndex = items.indexOf(document.activeElement);
            
            switch (e.key) {
                case 'ArrowDown':
                    e.preventDefault();
                    const nextIndex = (currentIndex + 1) % items.length;
                    items[nextIndex].focus();
                    break;
                case 'ArrowUp':
                    e.preventDefault();
                    const prevIndex = currentIndex <= 0 ? items.length - 1 : currentIndex - 1;
                    items[prevIndex].focus();
                    break;
                case 'Tab':
                    if (e.shiftKey && currentIndex === 0) {
                        toggleUserDropdown(false);
                        userInfo.focus();
                    } else if (!e.shiftKey && currentIndex === items.length - 1) {
                        toggleUserDropdown(false);
                    }
                    break;
            }
        });
    }
    
    // ========================================================================
    // Dark Mode Toggle
    // ========================================================================
    const themeToggle = document.getElementById('themeToggle');
    const themeIcon = themeToggle?.querySelector('i');
    
    // Check for saved theme preference or default to light mode
    const currentTheme = localStorage.getItem('admin-theme') || 'light';
    document.body.classList.toggle('dark-mode', currentTheme === 'dark');
    
    if (themeIcon) {
        themeIcon.className = currentTheme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
    }
    
    if (themeToggle) {
        themeToggle.addEventListener('click', function() {
            const isDarkMode = document.body.classList.contains('dark-mode');
            
            if (isDarkMode) {
                document.body.classList.remove('dark-mode');
                localStorage.setItem('admin-theme', 'light');
                themeIcon.className = 'fas fa-moon';
            } else {
                document.body.classList.add('dark-mode');
                localStorage.setItem('admin-theme', 'dark');
                themeIcon.className = 'fas fa-sun';
            }
            
            // Add animation effect
            themeToggle.style.transform = 'scale(0.8)';
            setTimeout(() => {
                themeToggle.style.transform = 'scale(1)';
            }, 150);
        });
    }
    
    // ========================================================================
    // Active Navigation Highlighting
    // ========================================================================
    function highlightActiveNavigation() {
        const currentPath = window.location.pathname;
        const sidebarItems = document.querySelectorAll('.sidebar-item');
        
        sidebarItems.forEach(item => {
            item.classList.remove('active');
            if (currentPath.includes(item.getAttribute('href'))) {
                item.classList.add('active');
            }
        });
    }
    
    highlightActiveNavigation();
    
    // ========================================================================
    // Enhanced Table Interactions
    // ========================================================================
    function enhanceTableInteractions() {
        const tableRows = document.querySelectorAll('#result_list tbody tr');
        
        tableRows.forEach(row => {
            // Add click to edit functionality
            row.addEventListener('click', function(e) {
                // Don't trigger if clicking on a link or button
                if (e.target.tagName === 'A' || e.target.tagName === 'BUTTON' || e.target.type === 'checkbox') {
                    return;
                }
                
                const editLink = row.querySelector('a');
                if (editLink) {
                    window.location.href = editLink.href;
                }
            });
            
            // Add hover cursor
            const hasEditLink = row.querySelector('a');
            if (hasEditLink) {
                row.style.cursor = 'pointer';
            }
        });
    }
    
    enhanceTableInteractions();
    
    // ========================================================================
    // Form Enhancements
    // ========================================================================
    function enhanceFormFields() {
        const formFields = document.querySelectorAll('input[type=\"text\"], input[type=\"email\"], input[type=\"password\"], textarea, select');
        
        formFields.forEach(field => {
            // Add floating label effect
            if (field.value) {
                field.classList.add('has-value');
            }
            
            field.addEventListener('focus', function() {
                this.classList.add('focused');
            });
            
            field.addEventListener('blur', function() {
                this.classList.remove('focused');
                if (this.value) {
                    this.classList.add('has-value');
                } else {
                    this.classList.remove('has-value');
                }
            });
            
            field.addEventListener('input', function() {
                if (this.value) {
                    this.classList.add('has-value');
                } else {
                    this.classList.remove('has-value');
                }
            });
        });
    }
    
    enhanceFormFields();
    
    // ========================================================================
    // Loading States for Buttons
    // ========================================================================
    function addLoadingStates() {
        const submitButtons = document.querySelectorAll('input[type=\"submit\"], button[type=\"submit\"], .submit-row input');
        
        submitButtons.forEach(button => {
            button.addEventListener('click', function() {
                if (this.form && this.form.checkValidity()) {
                    this.disabled = true;
                    this.style.opacity = '0.7';
                    
                    const originalText = this.value || this.textContent;
                    if (this.tagName === 'INPUT') {
                        this.value = 'Saving...';
                    } else {
                        this.innerHTML = '<i class=\"fas fa-spinner fa-spin\"></i> Saving...';
                    }
                    
                    // Re-enable after 5 seconds as fallback
                    setTimeout(() => {
                        this.disabled = false;
                        this.style.opacity = '1';
                        if (this.tagName === 'INPUT') {
                            this.value = originalText;
                        } else {
                            this.textContent = originalText;
                        }
                    }, 5000);
                }
            });
        });
    }
    
    addLoadingStates();
    
    // ========================================================================
    // Enhanced Search Functionality
    // ========================================================================
    function enhanceSearch() {
        const searchInput = document.querySelector('#changelist-search input[type=\"text\"]');
        
        if (searchInput) {
            // Add search icon
            const searchContainer = searchInput.parentElement;
            searchContainer.style.position = 'relative';
            
            const searchIcon = document.createElement('i');
            searchIcon.className = 'fas fa-search';
            searchIcon.style.cssText = `
                position: absolute;
                right: 1rem;
                top: 50%;
                transform: translateY(-50%);
                color: #6b7280;
                pointer-events: none;
            `;
            searchContainer.appendChild(searchIcon);
            
            // Add search enhancement
            let searchTimeout;
            searchInput.addEventListener('input', function() {
                clearTimeout(searchTimeout);
                searchTimeout = setTimeout(() => {
                    // Add visual feedback for search
                    searchIcon.style.color = '#10b981';
                    setTimeout(() => {
                        searchIcon.style.color = '#6b7280';
                    }, 1000);
                }, 500);
            });
        }
    }
    
    enhanceSearch();
    
    // ========================================================================
    // Notification System
    // ========================================================================
    function enhanceNotifications() {
        const messages = document.querySelectorAll('.messagelist li');
        
        messages.forEach((message, index) => {
            // Add icons based on message type
            const icon = document.createElement('i');
            if (message.classList.contains('success')) {
                icon.className = 'fas fa-check-circle';
            } else if (message.classList.contains('error')) {
                icon.className = 'fas fa-exclamation-circle';
            } else if (message.classList.contains('warning')) {
                icon.className = 'fas fa-exclamation-triangle';
            } else {
                icon.className = 'fas fa-info-circle';
            }
            
            message.insertBefore(icon, message.firstChild);
            
            // Add auto-dismiss for success messages
            if (message.classList.contains('success')) {
                setTimeout(() => {
                    message.style.opacity = '0';
                    message.style.transform = 'translateX(100%)';
                    setTimeout(() => {
                        if (message.parentNode) {
                            message.parentNode.removeChild(message);
                        }
                    }, 300);
                }, 5000);
            }
            
            // Add close button
            const closeButton = document.createElement('button');
            closeButton.innerHTML = '<i class=\"fas fa-times\"></i>';
            closeButton.style.cssText = `
                background: none;
                border: none;
                color: inherit;
                cursor: pointer;
                margin-left: auto;
                padding: 0.25rem;
                border-radius: 50%;
                transition: background-color 0.15s ease;
            `;
            
            closeButton.addEventListener('click', function() {
                message.style.opacity = '0';
                message.style.transform = 'translateX(100%)';
                setTimeout(() => {
                    if (message.parentNode) {
                        message.parentNode.removeChild(message);
                    }
                }, 300);
            });
            
            message.appendChild(closeButton);
            
            // Animate in
            message.style.opacity = '0';
            message.style.transform = 'translateX(100%)';
            setTimeout(() => {
                message.style.transition = 'all 0.3s ease';
                message.style.opacity = '1';
                message.style.transform = 'translateX(0)';
            }, index * 100);
        });
    }
    
    enhanceNotifications();
    
    // ========================================================================
    // Keyboard Shortcuts
    // ========================================================================
    function addKeyboardShortcuts() {
        document.addEventListener('keydown', function(e) {
            // Ctrl/Cmd + / to toggle sidebar
            if ((e.ctrlKey || e.metaKey) && e.key === '/') {
                e.preventDefault();
                if (sidebarToggle) {
                    sidebarToggle.click();
                }
            }
            
            // Ctrl/Cmd + K to focus search
            if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
                e.preventDefault();
                const searchInput = document.querySelector('#changelist-search input[type=\"text\"]');
                if (searchInput) {
                    searchInput.focus();
                }
            }
            
            // Escape to close sidebar on mobile
            if (e.key === 'Escape' && window.innerWidth <= 1024) {
                if (sidebar && sidebar.classList.contains('active')) {
                    sidebar.classList.remove('active');
                    const overlay = document.querySelector('.sidebar-overlay');
                    if (overlay) {
                        overlay.click();
                    }
                }
            }
        });
    }
    
    addKeyboardShortcuts();
    
    // ========================================================================
    // Responsive Navigation
    // ========================================================================
    function handleResponsiveNavigation() {
        function checkScreenSize() {
            if (window.innerWidth > 1024) {
                // Desktop: always show sidebar
                sidebar?.classList.remove('active');
                const overlay = document.querySelector('.sidebar-overlay');
                if (overlay) {
                    overlay.parentNode?.removeChild(overlay);
                }
            }
        }
        
        window.addEventListener('resize', checkScreenSize);
        checkScreenSize();
    }
    
    handleResponsiveNavigation();
    
    // ========================================================================
    // Statistics Animation
    // ========================================================================
    function animateStatistics() {
        const statNumbers = document.querySelectorAll('.stat-card h3');
        
        statNumbers.forEach(stat => {
            const finalNumber = parseInt(stat.textContent);
            if (!isNaN(finalNumber)) {
                let currentNumber = 0;
                const increment = Math.ceil(finalNumber / 30);
                
                const timer = setInterval(() => {
                    currentNumber += increment;
                    if (currentNumber >= finalNumber) {
                        currentNumber = finalNumber;
                        clearInterval(timer);
                    }
                    stat.textContent = currentNumber.toLocaleString();
                }, 50);
            }
        });
    }
    
    // Run animation when stats cards are visible
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateStatistics();
                observer.disconnect();
            }
        });
    });
    
    const statsContainer = document.querySelector('.admin-stats');
    if (statsContainer) {
        observer.observe(statsContainer);
    }
    
    // ========================================================================
    // Enhanced Delete Confirmations
    // ========================================================================
    function enhanceDeleteConfirmations() {
        const deleteLinks = document.querySelectorAll('.deletelink, .button.deletelink');
        
        deleteLinks.forEach(link => {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                
                const confirmDialog = document.createElement('div');
                confirmDialog.style.cssText = `
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    background: rgba(0, 0, 0, 0.5);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    z-index: 10000;
                    opacity: 0;
                    transition: opacity 0.3s ease;
                `;
                
                confirmDialog.innerHTML = `
                    <div style="
                        background: white;
                        padding: 2rem;
                        border-radius: 1rem;
                        max-width: 400px;
                        text-align: center;
                        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
                        transform: scale(0.9);
                        transition: transform 0.3s ease;
                    ">
                        <i class="fas fa-exclamation-triangle" style="font-size: 3rem; color: #dc2626; margin-bottom: 1rem;"></i>
                        <h3 style="margin: 0 0 1rem 0; color: #333;">Confirm Delete</h3>
                        <p style="margin: 0 0 2rem 0; color: #666;">Are you sure you want to delete this item? This action cannot be undone.</p>
                        <div style="display: flex; gap: 1rem; justify-content: center;">
                            <button class="cancel-btn" style="
                                background: #6b7280;
                                color: white;
                                border: none;
                                padding: 0.75rem 1.5rem;
                                border-radius: 0.5rem;
                                cursor: pointer;
                                font-weight: 600;
                            ">Cancel</button>
                            <button class="confirm-btn" style="
                                background: #dc2626;
                                color: white;
                                border: none;
                                padding: 0.75rem 1.5rem;
                                border-radius: 0.5rem;
                                cursor: pointer;
                                font-weight: 600;
                            ">Delete</button>
                        </div>
                    </div>
                `;
                
                document.body.appendChild(confirmDialog);
                
                // Animate in
                requestAnimationFrame(() => {
                    confirmDialog.style.opacity = '1';
                    const dialog = confirmDialog.querySelector('div');
                    dialog.style.transform = 'scale(1)';
                });
                
                // Handle buttons
                const cancelBtn = confirmDialog.querySelector('.cancel-btn');
                const confirmBtn = confirmDialog.querySelector('.confirm-btn');
                
                cancelBtn.addEventListener('click', () => {
                    confirmDialog.style.opacity = '0';
                    setTimeout(() => document.body.removeChild(confirmDialog), 300);
                });
                
                confirmBtn.addEventListener('click', () => {
                    window.location.href = this.href;
                });
                
                // Close on overlay click
                confirmDialog.addEventListener('click', (e) => {
                    if (e.target === confirmDialog) {
                        cancelBtn.click();
                    }
                });
            });
        });
    }
    
    enhanceDeleteConfirmations();
    
    // ========================================================================
    // Auto-save functionality for forms
    // ========================================================================
    function enableAutoSave() {
        const forms = document.querySelectorAll('form');
        
        forms.forEach(form => {
            const inputs = form.querySelectorAll('input[type=\"text\"], textarea, select');
            
            inputs.forEach(input => {
                let autoSaveTimeout;
                
                input.addEventListener('input', function() {
                    clearTimeout(autoSaveTimeout);
                    
                    // Show auto-save indicator
                    let indicator = document.querySelector('.auto-save-indicator');
                    if (!indicator) {
                        indicator = document.createElement('div');
                        indicator.className = 'auto-save-indicator';
                        indicator.style.cssText = `
                            position: fixed;
                            bottom: 2rem;
                            right: 2rem;
                            background: #10b981;
                            color: white;
                            padding: 0.75rem 1rem;
                            border-radius: 0.5rem;
                            font-size: 0.875rem;
                            z-index: 1000;
                            transform: translateY(100px);
                            transition: transform 0.3s ease;
                        `;
                        document.body.appendChild(indicator);
                    }
                    
                    indicator.innerHTML = '<i class=\"fas fa-save\"></i> Auto-saving...';
                    indicator.style.transform = 'translateY(0)';
                    
                    autoSaveTimeout = setTimeout(() => {
                        // Save to localStorage
                        const formData = new FormData(form);
                        const data = {};
                        for (let [key, value] of formData.entries()) {
                            data[key] = value;
                        }
                        localStorage.setItem(`admin-form-${form.id || 'default'}`, JSON.stringify(data));
                        
                        indicator.innerHTML = '<i class=\"fas fa-check\"></i> Saved';
                        setTimeout(() => {
                            indicator.style.transform = 'translateY(100px)';
                        }, 2000);
                    }, 1000);
                });
            });
        });
    }
    
    enableAutoSave();
    
    // ========================================================================
    // Initialize all enhancements
    // ========================================================================
    console.log('LUM Data Academy Admin Panel - Material Dashboard 2 Loaded Successfully! 🎓');
});

// ========================================================================
// Utility Functions
// ========================================================================
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.style.cssText = `
        position: fixed;
        top: 2rem;
        right: 2rem;
        background: ${type === 'success' ? '#10b981' : type === 'error' ? '#ef4444' : '#3b82f6'};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 0.75rem;
        font-weight: 500;
        z-index: 10000;
        transform: translateX(100%);
        transition: transform 0.3s ease;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1);
    `;
    
    toast.textContent = message;
    document.body.appendChild(toast);
    
    // Animate in
    requestAnimationFrame(() => {
        toast.style.transform = 'translateX(0)';
    });
    
    // Auto remove
    setTimeout(() => {
        toast.style.transform = 'translateX(100%)';
        setTimeout(() => {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
        }, 300);
    }, 4000);
}

// Export for global use
window.showToast = showToast;