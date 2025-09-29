'use strict'

const nodemailer = require('nodemailer')

module.exports = async (req, res) => {
	res.setHeader('Access-Control-Allow-Origin', '*')
	res.setHeader('Access-Control-Allow-Headers', 'Content-Type')
	res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS')
	if (req.method === 'OPTIONS') return res.status(200).end()
	if (req.method !== 'POST') return res.status(405).json({ error: 'Method Not Allowed' })

	try {
		const { name, email, message } = req.body || {}
		if (!email || !message) return res.status(400).json({ error: 'Missing fields' })

		const transporter = nodemailer.createTransport({
			host: process.env.SMTP_HOST,
			port: Number(process.env.SMTP_PORT || 587),
			secure: false,
			auth: {
				user: process.env.SMTP_USER,
				pass: process.env.SMTP_PASS
			}
		})

		await transporter.sendMail({
			from: process.env.MAIL_FROM || process.env.SMTP_USER,
			to: process.env.MAIL_TO || process.env.SMTP_USER,
			subject: `Website contact: ${name || 'Visitor'}`,
			text: `From: ${name || 'Visitor'} <${email}>\n\n${message}`
		})

		return res.status(200).json({ success: true })
	} catch (error) {
		console.error('Email error:', error)
		return res.status(500).json({ error: 'Failed to send email' })
	}
}

