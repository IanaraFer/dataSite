<?php
// Simple PHP form handler for DataSight AI
// Upload this to your web server to handle form submissions

header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST');
header('Access-Control-Allow-Headers: Content-Type');

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['error' => 'Method not allowed']);
    exit;
}

// Get form data
$data = json_decode(file_get_contents('php://input'), true);

if (!$data) {
    $data = $_POST;
}

// Validate required fields
$required = ['firstName', 'lastName', 'email', 'company', 'phone', 'industry', 'revenue'];
foreach ($required as $field) {
    if (empty($data[$field])) {
        http_response_code(400);
        echo json_encode(['error' => "Missing required field: $field"]);
        exit;
    }
}

// Sanitize data
$lead = [
    'firstName' => htmlspecialchars($data['firstName']),
    'lastName' => htmlspecialchars($data['lastName']),
    'email' => filter_var($data['email'], FILTER_SANITIZE_EMAIL),
    'company' => htmlspecialchars($data['company']),
    'phone' => htmlspecialchars($data['phone']),
    'industry' => htmlspecialchars($data['industry']),
    'revenue' => htmlspecialchars($data['revenue']),
    'challenge' => htmlspecialchars($data['challenge'] ?? ''),
    'timestamp' => date('Y-m-d H:i:s'),
    'ip_address' => $_SERVER['REMOTE_ADDR'] ?? '',
    'user_agent' => $_SERVER['HTTP_USER_AGENT'] ?? ''
];

// Save to CSV file
$csvFile = 'leads.csv';
$isNewFile = !file_exists($csvFile);

$fp = fopen($csvFile, 'a');
if ($fp) {
    // Add headers if new file
    if ($isNewFile) {
        fputcsv($fp, array_keys($lead));
    }
    fputcsv($fp, $lead);
    fclose($fp);
}

// Send email notification
$to = 'datasightai.founders@gmail.com';
$subject = "🚀 NEW DATASIGHT AI LEAD: {$lead['firstName']} from {$lead['company']}";

$emailBody = "
🚀 NEW DATASIGHT AI LEAD ALERT!

👤 CONTACT INFORMATION:
Name: {$lead['firstName']} {$lead['lastName']}
Company: {$lead['company']}
Email: {$lead['email']}
Phone: {$lead['phone']}

🏢 BUSINESS DETAILS:
Industry: {$lead['industry']}
Annual Revenue: {$lead['revenue']}
Main Challenge: {$lead['challenge']}

⏰ SUBMISSION TIME: {$lead['timestamp']}
🌐 IP Address: {$lead['ip_address']}

📋 NEXT STEPS:
1. Call within 15 minutes for best conversion rates: {$lead['phone']}
2. Send personalized AI analysis via email: {$lead['email']}
3. Schedule demo call within 24 hours
4. Add to CRM with 'hot lead' status

💰 POTENTIAL VALUE:
Based on revenue range, this could be a €" . getLeadValue($lead['revenue']) . " opportunity.

---
Reply to this email to respond directly to the prospect.
This lead was generated from your DataSight AI free trial landing page.
";

$headers = [
    'From: DataSight AI <noreply@datasightai.com>',
    'Reply-To: ' . $lead['email'],
    'X-Mailer: PHP/' . phpversion(),
    'Content-Type: text/plain; charset=UTF-8'
];

$emailSent = mail($to, $subject, $emailBody, implode("\r\n", $headers));

// Send auto-reply to prospect
$autoReplySubject = "Thank you for your DataSight AI request, {$lead['firstName']}!";
$autoReplyBody = "
Hi {$lead['firstName']},

Thank you for your interest in DataSight AI! We've received your request for a free business health check.

🎯 What happens next:
• Our AI is analyzing your business profile right now
• You'll receive your comprehensive report within 15 minutes
• Our team will reach out within 24 hours to discuss your results

📊 Your personalized analysis will include:
✓ Revenue forecasting for {$lead['company']}
✓ Customer segmentation insights
✓ Growth opportunities specific to {$lead['industry']}
✓ 5 actionable recommendations with ROI estimates

Questions? Reply to this email or call us at +353 874502058.

Best regards,
The DataSight AI Team

P.S. Keep an eye on your inbox - your analysis report is on its way!
";

$autoReplyHeaders = [
    'From: DataSight AI <datasightai.founders@gmail.com>',
    'X-Mailer: PHP/' . phpversion(),
    'Content-Type: text/plain; charset=UTF-8'
];

mail($lead['email'], $autoReplySubject, $autoReplyBody, implode("\r\n", $autoReplyHeaders));

// Log the submission
error_log("New DataSight AI lead: {$lead['firstName']} {$lead['lastName']} from {$lead['company']} ({$lead['email']})");

// Return success response
echo json_encode([
    'success' => true,
    'message' => 'Lead submitted successfully',
    'lead_id' => $lead['timestamp'] . '_' . substr(md5($lead['email']), 0, 8),
    'email_sent' => $emailSent
]);

function getLeadValue($revenue) {
    $values = [
        'under-500k' => '2,500-5,000',
        '500k-1m' => '5,000-10,000', 
        '1m-5m' => '10,000-25,000',
        '5m-20m' => '25,000-75,000',
        'over-20m' => '50,000-150,000'
    ];
    return $values[$revenue] ?? '5,000-15,000';
}
?>
