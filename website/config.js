const PLATFORM_CONFIG = {
    api: { baseUrl: '/api' },
    pricing: {
        starter: { name: 'Starter', price: 199 },
        professional: { name: 'Professional', price: 399 },
        enterprise: { name: 'Enterprise', price: 799 }
    }
};

function handlePayment(planType) {
    console.log('Redirecting to subscription page for:', planType);
    window.location.href = `subscribe.html?plan=${planType}`;
}

function subscribeToPlan(planName, price) {
    console.log('Subscribe function called:', planName, price);
    let planType = 'starter';
    
    // Fix the mapping based on plan name, not price (since price might be wrong)
    if (planName === 'professional') planType = 'professional';
    if (planName === 'business' || planName === 'enterprise') planType = 'enterprise';
    
    console.log('Mapped to plan type:', planType);
    handlePayment(planType);
}

// Also support direct plan detection from button context
function detectPlanFromButton(button) {
    const text = button.textContent.toLowerCase();
    const container = button.closest('.pricing-card, .plan-card, .card');
    const containerText = container ? container.textContent.toLowerCase() : '';
    
    if (text.includes('starter') || containerText.includes('starter') || containerText.includes('199')) {
        return 'starter';
    }
    if (text.includes('professional') || containerText.includes('professional') || containerText.includes('399')) {
        return 'professional';
    }
    if (text.includes('enterprise') || containerText.includes('enterprise') || containerText.includes('799')) {
        return 'enterprise';
    }
    return 'starter'; // default
}

document.addEventListener('DOMContentLoaded', function() {
    console.log('AnalyticaCore AI subscription system loaded');
    
    // Handle all subscription buttons
    document.querySelectorAll('a[href="#"], button').forEach(button => {
        if (button.textContent.includes('Subscribe') || 
            button.onclick || 
            button.getAttribute('onclick')) {
            
            button.addEventListener('click', function(e) {
                e.preventDefault();
                
                // Try to detect plan from button context
                const planType = detectPlanFromButton(button);
                console.log('Button clicked, detected plan:', planType);
                handlePayment(planType);
            });
        }
    });
});
