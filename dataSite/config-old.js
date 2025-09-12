const PLATFORM_CONFIG = {
    api: {
        baseUrl: 'https://analyticacoreai.netlify.app/.netlify/functions',
        endpoints: {
            payment: '/checkout',
            contact: '/contact',
            upload: '/upload',
            subscription: '/create-subscription'
        }
    },
    companyName: 'AnalyticaCore AI',
    email: 'analyticacoreai@outlook.com',
    website: 'https://analyticacoreai.ie',
    pricing: {
        starter: { name: 'Starter', price: 199, priceId: 'price_starter_eur_199' },
        professional: { name: 'Professional', price: 399, priceId: 'price_professional_eur_399' },
        enterprise: { name: 'Enterprise', price: 799, priceId: 'price_enterprise_eur_799' }
    }
};

// Redirect to subscription page for proper registration
function handlePayment(planType) {
    window.location.href = `subscribe.html?plan=${planType}`;
}

// Support old pricing page calls
function subscribeToPlan(planName, price) {
    let planType = 'starter';
    if (planName === 'professional' || price === 399) planType = 'professional';
    if (planName === 'business' || planName === 'enterprise' || price === 799) planType = 'enterprise';
    
    window.location.href = `subscribe.html?plan=${planType}`;
}

const API = {
    async call(endpoint, data = null, method = 'GET') {
        const url = PLATFORM_CONFIG.api.baseUrl + endpoint;
        const options = { method, headers: { 'Content-Type': 'application/json' } };
        if (data && method !== 'GET') options.body = JSON.stringify(data);
        const response = await fetch(url, options);
        return await response.json();
    },
    async submitContact(formData) {
        return await this.call('/contact', formData, 'POST');
    },
    async uploadFile(formData) {
        const response = await fetch(PLATFORM_CONFIG.api.baseUrl + '/upload', { method: 'POST', body: formData });
        return await response.json();
    }
};

function handleContactForm(event) {
    event.preventDefault();
    const form = event.target;
    const formData = new FormData(form);
    const submitButton = form.querySelector('button[type="submit"]');
    submitButton.textContent = 'Sending...';
    submitButton.disabled = true;
    const contactData = {
        name: formData.get('name'),
        email: formData.get('email'),
        company: formData.get('company'),
        message: formData.get('message')
    };
    API.submitContact(contactData).then(response => {
        if (response.success) {
            alert('Message sent successfully!');
            form.reset();
        } else throw new Error(response.error);
    }).catch(error => {
        alert('Failed to send message: ' + error.message);
    }).finally(() => {
        submitButton.textContent = 'Send Message';
        submitButton.disabled = false;
    });
}

document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.payment-button, .btn-primary, .btn-plan').forEach(button => {
        if (button.dataset.plan || button.textContent.includes('Subscribe') || button.onclick) {
            button.addEventListener('click', (e) => {
                e.preventDefault();
                let planType = button.dataset.plan;
                if (!planType) {
                    const text = button.textContent.toLowerCase();
                    if (text.includes('starter') || text.includes('199')) planType = 'starter';
                    else if (text.includes('professional') || text.includes('399')) planType = 'professional';
                    else if (text.includes('enterprise') || text.includes('799')) planType = 'enterprise';
                }
                if (planType) handlePayment(planType);
            });
        }
    });
    const contactForm = document.querySelector('form');
    if (contactForm && contactForm.querySelector('input[type="email"]')) {
        contactForm.addEventListener('submit', handleContactForm);
    }
});
