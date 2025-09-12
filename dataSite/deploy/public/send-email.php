<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST');
header('Access-Control-Allow-Headers: Content-Type');

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $input = json_decode(file_get_contents('php://input'), true);
    
    $to = 'datasightai.founders@gmail.com';
    $subject = $input['subject'] ?? 'New DataSight AI Lead';
    $message = $input['message'] ?? 'New lead submission';
    $from = $input['from_email'] ?? 'noreply@datasightai.com';
    
    $headers = "From: DataSight AI <noreply@datasightai.com>\r\n";
    $headers .= "Reply-To: " . $from . "\r\n";
    $headers .= "Content-Type: text/plain; charset=UTF-8\r\n";
    $headers .= "X-Mailer: PHP/" . phpversion();
    
    $success = mail($to, $subject, $message, $headers);
    
    if ($success) {
        echo json_encode(['status' => 'success', 'message' => 'Email sent successfully']);
    } else {
        echo json_encode(['status' => 'error', 'message' => 'Failed to send email']);
    }
} else {
    echo json_encode(['status' => 'error', 'message' => 'Only POST method allowed']);
}
?>
