'use strict'

module.exports = async (req, res) => {
	res.setHeader('Access-Control-Allow-Origin', '*')
	res.setHeader('Access-Control-Allow-Headers', 'Content-Type')
	res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS')
	if (req.method === 'OPTIONS') return res.status(200).end()
	if (req.method !== 'POST') return res.status(405).json({ error: 'Method Not Allowed' })

	// Minimal Netlify-style form capture passthrough. Just accept and 204 to not break UX
	try {
		return res.status(204).end()
	} catch (e) {
		return res.status(204).end()
	}
}

