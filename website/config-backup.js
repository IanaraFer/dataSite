const PLATFORM_CONFIG = {
    api: {
        baseUrl: 'https://analyticacoreai.netlify.app/.netlify/functions',
        endpoints: {
            payment: '/checkout',
            contact: '/contact',
            upload: '/upload'
        }
    },
    companyName: 'AnalyticaCore AI',
    email: 'information@analyticacoreai.ie',
    website: 'https://analyticacoreai.ie',
    pricing: {
        starter: { name: 'Starter', price: 199, priceId: 'price_starter_eur_199' },
        professional: { name: 'Professional', price: 399, priceId: 'price_professional_eur_399' },
        enterprise: { name: 'Enterprise', price: 799, priceId: 'price_enterprise_eur_799' }
    }
};

const API = {
    async call(endpoint, data = null, method = 'GET') {
        const url = PLATFORM_CONFIG.api.baseUrl + endpoint;
        const options = { method, headers: { 'Content-Type': 'application/json' } };
        if (data && method !== 'GET') options.body = JSON.stringify(data);
        const response = await fetch(url, options);
        return await response.json();
    },
    async createCheckoutSession(planType) {
        const plan = PLATFORM_CONFIG.pricing[planType];
        return await this.call('/checkout', { planType, priceId: plan.priceId, amount: plan.price }, 'POST');
    },
    async submitContact(formData) {
        return await this.call('/contact', formData, 'POST');
    },
    async uploadFile(formData) {
        const response = await fetch(PLATFORM_CONFIG.api.baseUrl + '/upload', { method: 'POST', body: formData });
        return await response.json();
    }
};

function handlePayment(planType) {
    const button = event.target;
    button.textContent = 'Processing...';
    button.disabled = true;
    API.createCheckoutSession(planType).then(response => {
        if (response.sessionUrl) window.location.href = response.sessionUrl;
        else throw new Error(response.error);
    }).catch(error => {
        alert('Payment failed: ' + error.message);
        button.textContent = 'Subscribe';
        button.disabled = false;
    });
}

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
    document.querySelectorAll('.payment-button, .btn-primary').forEach(button => {
        if (button.dataset.plan || button.textContent.includes('Subscribe')) {
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
