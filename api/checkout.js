'use strict'

const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY)

module.exports = async (req, res) => {
	res.setHeader('Access-Control-Allow-Origin', '*')
	res.setHeader('Access-Control-Allow-Headers', 'Content-Type')
	res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS')
	if (req.method === 'OPTIONS') return res.status(200).end()
	if (req.method !== 'POST') return res.status(405).json({ error: 'Method Not Allowed' })

	try {
		const { plan = 'starter' } = req.body || {}
		const prices = {
			starter: process.env.STRIPE_PRICE_STARTER,
			professional: process.env.STRIPE_PRICE_PROFESSIONAL,
			enterprise: process.env.STRIPE_PRICE_ENTERPRISE
		}
		const priceId = prices[plan]
		if (!priceId) return res.status(400).json({ error: 'Invalid plan' })

		const session = await stripe.checkout.sessions.create({
			payment_method_types: ['card'],
			line_items: [{ price: priceId, quantity: 1 }],
			mode: 'subscription',
			success_url: `${process.env.SITE_URL || 'https://analyticacoreai.netlify.app'}/success.html?session_id={CHECKOUT_SESSION_ID}`,
			cancel_url: `${process.env.SITE_URL || 'https://analyticacoreai.netlify.app'}/pricing.html`
		})

		return res.status(200).json({ url: session.url })
	} catch (error) {
		console.error('Stripe error:', error)
		return res.status(500).json({ error: error.message })
	}
}

