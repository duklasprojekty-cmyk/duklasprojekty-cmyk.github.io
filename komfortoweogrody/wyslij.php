<?php
// Komfortowe Ogrody – wysyłka formularzy (kontakt i wycena) bezpośrednio na skrzynkę firmy.
// Działa na serwerze z PHP (Hostinger). Na podglądzie github.io PHP nie działa – wtedy strona
// sama przełącza się na otwarcie programu pocztowego.

$DO     = 'kontakt@komfortoweogrody.pl';   // adres, na który trafiają zapytania
$NADAWCA = 'kontakt@komfortoweogrody.pl';  // adres w domenie (musi istnieć w hPanel → E-maile)
$TEL    = '+48 600 927 502';

$ajax = isset($_SERVER['HTTP_X_REQUESTED_WITH']);
function odpowiedz($ok, $tekst, $kod = 200) {
    global $ajax;
    http_response_code($kod);
    if ($ajax) {
        header('Content-Type: application/json; charset=utf-8');
        echo json_encode(['ok' => $ok, 'message' => $tekst], JSON_UNESCAPED_UNICODE);
    } else {
        header('Content-Type: text/html; charset=utf-8');
        echo '<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Komfortowe Ogrody</title>'
           . '<body style="font-family:system-ui,sans-serif;max-width:560px;margin:15vh auto;padding:0 16px;line-height:1.5">'
           . '<h1>' . ($ok ? 'Dziękujemy!' : 'Nie udało się wysłać') . '</h1><p>' . htmlspecialchars($tekst) . '</p><p><a href="/">Wróć na stronę</a></p></body>';
    }
    exit;
}
date_default_timezone_set('Europe/Warsaw');
header('Cache-Control: no-store');
header('X-Robots-Tag: noindex');

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') odpowiedz(false, 'Formularz wysyła się z podstron Kontakt i Wycena.', 405);

// Zapytanie musi przyjść z tej samej strony
$origin = $_SERVER['HTTP_ORIGIN'] ?? ($_SERVER['HTTP_REFERER'] ?? '');
$host = $_SERVER['HTTP_HOST'] ?? '';
$bezPortu = function ($h) { return preg_replace('/^www\./', '', strtolower(preg_replace('/:\d+$/', '', (string)$h))); };
if ($origin && $bezPortu(parse_url($origin, PHP_URL_HOST)) !== $bezPortu($host)) odpowiedz(false, 'Nieprawidłowe źródło zapytania.', 403);
$host = $bezPortu($host);

// Pułapka na boty: ukryte pole „firma” – udajemy sukces
if (!empty($_POST['firma'])) odpowiedz(true, 'Dziękujemy za kontakt!');

$jedna = function ($v, $max) { return mb_substr(trim(preg_replace('/[\r\n\t]+/', ' ', (string)$v)), 0, $max); };
$typ   = ($_POST['typ'] ?? '') === 'wycena' ? 'wycena' : 'kontakt';
$imie  = $jedna($_POST['name'] ?? '', 100);
$email = $jedna($_POST['email'] ?? '', 150);
$tel   = $jedna($_POST['phone'] ?? '', 40);
$tresc = trim((string)($_POST['tresc'] ?? ($_POST['message'] ?? '')));
$tresc = mb_substr(str_replace("\r\n", "\n", $tresc), 0, 6000);

if (!filter_var($email, FILTER_VALIDATE_EMAIL)) odpowiedz(false, 'Podaj poprawny adres e-mail.', 422);
if ($tresc === '') odpowiedz(false, 'Wpisz treść wiadomości.', 422);

// Prosty limit: najwyżej 5 wiadomości z jednego adresu IP w ciągu 10 minut
$ip = $_SERVER['REMOTE_ADDR'] ?? '0';
$plik = sys_get_temp_dir() . '/ko_form_' . md5($ip) . '.json';
$teraz = time();
$slady = array_filter((array)@json_decode(@file_get_contents($plik), true), function ($t) use ($teraz) { return $t > $teraz - 600; });
if (count($slady) >= 5) odpowiedz(false, 'Wysłano już kilka wiadomości. Spróbuj za kilka minut albo zadzwoń: ' . $TEL . '.', 429);

$temat = ($typ === 'wycena' ? 'Zapytanie o wycenę' : 'Zapytanie ze strony') . ($imie !== '' ? ' – ' . $imie : '');
$cialo = $tresc . "\n\n—\n"
       . ($imie !== '' ? $imie . "\n" : '') . $email . ($tel !== '' ? "\ntel. " . $tel : '')
       . "\n\nWysłano z formularza na stronie " . $host . ' (' . date('Y-m-d H:i') . ').'
       . "\nOdpowiedz na tę wiadomość, a odpowiedź trafi bezpośrednio do klienta.";

$naglowki = implode("\r\n", [
    'From: =?UTF-8?B?' . base64_encode('Formularz Komfortowe Ogrody') . '?= <' . $NADAWCA . '>',
    'Reply-To: ' . ($imie !== '' ? '=?UTF-8?B?' . base64_encode($imie) . '?= ' : '') . '<' . $email . '>',
    'MIME-Version: 1.0',
    'Content-Type: text/plain; charset=UTF-8',
    'Content-Transfer-Encoding: 8bit',
    'X-Mailer: komfortoweogrody.pl',
]);
$wyslano = @mail($DO, '=?UTF-8?B?' . base64_encode($temat) . '?=', $cialo, $naglowki, '-f' . $NADAWCA);

if (!$wyslano) odpowiedz(false, 'Nie udało się wysłać wiadomości. Zadzwoń: ' . $TEL . ' albo napisz na ' . $DO . '.', 500);

$slady[] = $teraz;
@file_put_contents($plik, json_encode(array_values($slady)));
odpowiedz(true, $typ === 'wycena'
    ? 'Zapytanie o wycenę zostało wysłane. Odezwiemy się najszybciej, jak to możliwe.'
    : 'Wiadomość została wysłana. Odpowiemy najszybciej, jak to możliwe.');
