// SUBSCRIPTION FIX - Makes Subscribe buttons work
function subscribeToPlan(planName, price) {
    console.log('Subscribe clicked:', planName, price);
    
    let planType = 'starter';
    if (planName === 'professional') planType = 'professional';
    if (planName === 'business' || planName === 'enterprise') planType = 'enterprise';
    
    console.log('Redirecting to plan:', planType);
    window.location.href = 'subscribe.html?plan=' + planType;
}

// Handle all subscribe buttons
document.addEventListener('DOMContentLoaded', function() {
    console.log('Subscription system loaded');
    
    // Find all subscribe buttons
    const buttons = document.querySelectorAll('a');
    buttons.forEach(button => {
        if (button.textContent.includes('Subscribe')) {
            button.addEventListener('click', function(e) {
                e.preventDefault();
                console.log('Subscribe button clicked via event listener');
                
                const container = button.closest('.card, .pricing-card, .col');
                const text = container ? container.textContent : '';
                
                let planType = 'starter';
                if (text.includes('399') || text.includes('Professional')) {
                    planType = 'professional';
                } else if (text.includes('799') || text.includes('Enterprise')) {
                    planType = 'enterprise';
                }
                
                console.log('Detected plan:', planType);
                window.location.href = 'subscribe.html?plan=' + planType;
            });
        }
    });
});
