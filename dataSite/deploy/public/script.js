// Global Variables
let demoModal, contactModal;

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeModals();
    initializeAnimations();
    initializeSmoothScrolling();
    initializeNavbarEffects();
    initializeCounters();
    
    // Add loading states
    simulateLoadingStates();
});

// Initialize Bootstrap Modals
function initializeModals() {
    demoModal = new bootstrap.Modal(document.getElementById('demoModal'));
    contactModal = new bootstrap.Modal(document.getElementById('contactModal'));
}

// Show Demo Modal
function showDemoModal() {
    demoModal.show();
}

// Show Contact Modal
function showContactModal() {
    contactModal.show();
}

// Initialize Animations
function initializeAnimations() {
    // Intersection Observer for fade-in animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in-up');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe all feature cards and pricing cards
    document.querySelectorAll('.feature-card, .pricing-card, .testimonial-card').forEach(card => {
        observer.observe(card);
    });
}

// Smooth Scrolling for Anchor Links
function initializeSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
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

// Navbar Effects
function initializeNavbarEffects() {
    const navbar = document.querySelector('.navbar');
    
    window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
            navbar.classList.add('shadow-sm');
            navbar.style.backgroundColor = 'rgba(31, 119, 180, 0.95)';
        } else {
            navbar.classList.remove('shadow-sm');
            navbar.style.backgroundColor = '';
        }
    });

    // Active navigation highlighting
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');

    window.addEventListener('scroll', function() {
        let current = '';
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.clientHeight;
            if (window.scrollY >= (sectionTop - 200)) {
                current = section.getAttribute('id');
            }
        });

        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === `#${current}`) {
                link.classList.add('active');
            }
        });
    });
}

// Initialize Counter Animations
function initializeCounters() {
    const counters = document.querySelectorAll('.display-5, .fw-bold');
    
    const counterObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const target = entry.target;
                const text = target.textContent;
                
                // Check if it's a number with % or contains digits
                if (text.match(/\d+[%]?/)) {
                    animateCounter(target, text);
                    counterObserver.unobserve(target);
                }
            }
        });
    }, { threshold: 0.5 });

    counters.forEach(counter => {
        counterObserver.observe(counter);
    });
}

// Animate Counter
function animateCounter(element, finalText) {
    const match = finalText.match(/(\d+)([%]?)/);
    if (!match) return;
    
    const finalNumber = parseInt(match[1]);
    const suffix = match[2];
    const duration = 2000; // 2 seconds
    const steps = 60;
    const increment = finalNumber / steps;
    let current = 0;
    
    const timer = setInterval(() => {
        current += increment;
        if (current >= finalNumber) {
            element.textContent = finalNumber + suffix;
            clearInterval(timer);
        } else {
            element.textContent = Math.floor(current) + suffix;
        }
    }, duration / steps);
}

// Simulate Loading States (for demo purposes)
function simulateLoadingStates() {
    // Add loading class to cards initially
    const cards = document.querySelectorAll('.feature-card, .pricing-card');
    cards.forEach((card, index) => {
        card.classList.add('loading');
        setTimeout(() => {
            card.classList.remove('loading');
        }, 500 + (index * 100));
    });
}

// Form Validation and Submission
function validateContactForm() {
    const form = document.querySelector('#contactModal form');
    const inputs = form.querySelectorAll('input[required], textarea[required]');
    let isValid = true;

    inputs.forEach(input => {
        if (!input.value.trim()) {
            input.classList.add('is-invalid');
            isValid = false;
        } else {
            input.classList.remove('is-invalid');
        }
    });

    return isValid;
}

// Handle Demo Scheduling
document.addEventListener('click', function(e) {
    if (e.target.textContent === 'Schedule Demo') {
        if (validateContactForm()) {
            // Simulate form submission
            const button = e.target;
            const originalText = button.textContent;
            button.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Scheduling...';
            button.disabled = true;

            setTimeout(() => {
                button.innerHTML = '<i class="fas fa-check me-2"></i>Demo Scheduled!';
                button.classList.remove('btn-primary');
                button.classList.add('btn-success');
                
                setTimeout(() => {
                    contactModal.hide();
                    // Reset form and button
                    setTimeout(() => {
                        button.innerHTML = originalText;
                        button.classList.remove('btn-success');
                        button.classList.add('btn-primary');
                        button.disabled = false;
                        document.querySelector('#contactModal form').reset();
                    }, 1000);
                }, 1500);
            }, 2000);
        }
    }
});

// Simulate Real-time Data Updates (for demo effect)
function simulateRealTimeUpdates() {
    const stats = [
        { selector: '.col-4:nth-child(1) h3', baseValue: 1247, variance: 5 },
        { selector: '.col-4:nth-child(2) h3', baseValue: 45623, variance: 50 }
    ];

    stats.forEach(stat => {
        const element = document.querySelector(stat.selector);
        if (element) {
            setInterval(() => {
                const newValue = stat.baseValue + Math.floor(Math.random() * stat.variance);
                element.textContent = newValue.toLocaleString();
            }, 5000);
        }
    });
}

// Initialize real-time updates after page load
setTimeout(simulateRealTimeUpdates, 3000);

// Keyboard Navigation
document.addEventListener('keydown', function(e) {
    // ESC key closes modals
    if (e.key === 'Escape') {
        if (demoModal._isShown) demoModal.hide();
        if (contactModal._isShown) contactModal.hide();
    }
    
    // Enter key in contact form
    if (e.key === 'Enter' && e.target.closest('#contactModal')) {
        e.preventDefault();
        const scheduleButton = document.querySelector('#contactModal .btn-primary');
        if (scheduleButton) scheduleButton.click();
    }
});

// Add hover effects to buttons
document.querySelectorAll('.btn').forEach(button => {
    button.addEventListener('mouseenter', function() {
        this.style.transform = 'translateY(-2px)';
    });
    
    button.addEventListener('mouseleave', function() {
        this.style.transform = 'translateY(0)';
    });
});

// Parallax Effect for Hero Section
window.addEventListener('scroll', function() {
    const scrolled = window.pageYOffset;
    const hero = document.querySelector('.hero-section');
    if (hero) {
        hero.style.transform = `translateY(${scrolled * 0.5}px)`;
    }
});

// Cookie Consent (Simple Implementation)
function showCookieConsent() {
    if (!localStorage.getItem('cookieConsent')) {
        const cookieBar = document.createElement('div');
        cookieBar.className = 'position-fixed bottom-0 start-0 end-0 bg-dark text-white p-3 shadow';
        cookieBar.style.zIndex = '9999';
        cookieBar.innerHTML = `
            <div class="container d-flex align-items-center justify-content-between flex-wrap">
                <div class="me-3">
                    <span>We use cookies to enhance your experience. By continuing to visit this site you agree to our use of cookies.</span>
                </div>
                <div>
                    <button class="btn btn-outline-light btn-sm me-2" onclick="acceptCookies()">Accept</button>
                    <button class="btn btn-link text-light btn-sm" onclick="declineCookies()">Decline</button>
                </div>
            </div>
        `;
        document.body.appendChild(cookieBar);
    }
}

function acceptCookies() {
    localStorage.setItem('cookieConsent', 'accepted');
    document.querySelector('.position-fixed.bottom-0').remove();
}

function declineCookies() {
    localStorage.setItem('cookieConsent', 'declined');
    document.querySelector('.position-fixed.bottom-0').remove();
}

// Show cookie consent after a delay
setTimeout(showCookieConsent, 2000);

// Analytics Simulation (for demo purposes)
function trackEvent(event, category, action) {
    console.log(`Analytics: ${category} - ${action} - ${event}`);
    // In production, this would integrate with Google Analytics or similar
}

// Track button clicks
document.addEventListener('click', function(e) {
    if (e.target.matches('.btn')) {
        const buttonText = e.target.textContent.trim();
        trackEvent('click', 'button', buttonText);
    }
});

// Performance Monitoring
window.addEventListener('load', function() {
    const loadTime = performance.timing.loadEventEnd - performance.timing.navigationStart;
    console.log(`Page load time: ${loadTime}ms`);
    
    // Track Core Web Vitals (simplified)
    if ('performance' in window && 'measure' in performance) {
        setTimeout(() => {
            const fcp = performance.getEntriesByName('first-contentful-paint')[0];
            if (fcp) {
                console.log(`First Contentful Paint: ${fcp.startTime}ms`);
            }
        }, 0);
    }
});

// Service Worker Registration (for PWA features)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        navigator.serviceWorker.register('/sw.js')
            .then(function(registration) {
                console.log('ServiceWorker registration successful');
            })
            .catch(function(error) {
                console.log('ServiceWorker registration failed');
            });
    });
}

console.log('DataSight AI website loaded successfully! 🚀');
