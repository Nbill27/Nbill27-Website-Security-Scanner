import requests
import socket
import ssl
import whois
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re
from datetime import datetime
import time
from colorama import Fore, Style, init

# Inisialisasi warna untuk output konsol
init(autoreset=True)

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
HEADERS = {"User-Agent": USER_AGENT}

def get_response(url, timeout=5):
    """ Mengambil respons dari URL dengan penanganan error. """
    try:
        return requests.get(url, headers=HEADERS, timeout=timeout, allow_redirects=True)
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}⛔ Koneksi error: {str(e)}")
        return None

def check_http_status(url):
    """ Mengecek status HTTP dan waktu respon. """
    start_time = time.time()
    response = get_response(url)
    load_time = time.time() - start_time

    if response:
        server_header = response.headers.get('Server', 'Tidak diketahui')
        return (
            f"{Fore.CYAN}🛡 Status HTTP: {response.status_code}\n"
            f"{Fore.CYAN}⏱ Waktu respon: {load_time:.2f}s\n"
            f"{Fore.CYAN}📡 Server: {server_header}"
        )
    return f"{Fore.RED}⛔ Website tidak dapat diakses!"

def check_ssl(url):
    """ Mengecek validitas sertifikat SSL/TLS. """
    try:
        hostname = urlparse(url).hostname
        context = ssl.create_default_context()

        with socket.create_connection((hostname, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                if not cert:
                    return f"{Fore.RED}⛔ SSL tidak ditemukan atau tidak valid!"

                issuer = dict(x[0] for x in cert.get('issuer', []))
                valid_from = datetime.strptime(cert['notBefore'], '%b %d %H:%M:%S %Y %Z')
                valid_to = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                remaining_days = (valid_to - datetime.now()).days

        return (
            f"{Fore.GREEN}🔒 SSL Valid hingga: {valid_to.strftime('%Y-%m-%d')}\n"
            f"{Fore.GREEN}📅 Sisa hari: {remaining_days}\n"
            f"{Fore.GREEN}🏢 Penerbit: {issuer.get('organizationName', 'Tidak diketahui')}"
        )
    except Exception as e:
        return f"{Fore.RED}⛔ Error SSL: {str(e)}"

def check_security_headers(url):
    """ Mengecek keberadaan security headers. """
    response = get_response(url)
    if not response:
        return ""

    headers = response.headers
    security_headers = {
        'Content-Security-Policy': '❌',
        'X-Content-Type-Options': '❌',
        'X-Frame-Options': '❌',
        'X-XSS-Protection': '❌',
        'Strict-Transport-Security': '❌'
    }

    for header in security_headers.keys():
        if header in headers:
            security_headers[header] = '✅'

    results = [f"{Fore.CYAN}🛡 Security Headers:"]
    for header, status in security_headers.items():
        results.append(f"{Fore.GREEN if status == '✅' else Fore.RED}{header}: {status}")

    return "\n".join(results)

def check_sensitive_paths(url):
    """ Mengecek endpoint sensitif yang mungkin terbuka. """
    base_url = f"{urlparse(url).scheme}://{urlparse(url).hostname}"
    sensitive_paths = [
        '/admin', '/wp-admin', '/.env',
        '/.git/config', '/phpinfo.php', '/server-status'
    ]

    results = []
    for path in sensitive_paths:
        test_url = base_url + path
        response = get_response(test_url)
        if response and response.status_code == 200:
            results.append(f"{Fore.RED}⚠️ Ditemukan: {test_url}")

    return "\n".join(results) if results else f"{Fore.GREEN}✅ Tidak ditemukan path sensitif"

def check_xss_sqli(url):
    """ Menguji kerentanan XSS dan SQL Injection. """
    xss_payload = "<script>alert('XSS')</script>"
    sqli_payload = "' OR 1=1--"

    vulnerabilities = []

    # Test XSS
    test_url = f"{url}?search={xss_payload}"
    response = get_response(test_url)
    if response and xss_payload in response.text:
        vulnerabilities.append(f"{Fore.RED}⛔ XSS Vulnerable!")

    # Test SQLi
    test_url = f"{url}?id={sqli_payload}"
    response = get_response(test_url)
    if response and any(err in response.text.lower() for err in ['sql', 'syntax', 'database', 'mysql', 'error']):
        vulnerabilities.append(f"{Fore.RED}⛔ SQLi Vulnerable!")

    return "\n".join(vulnerabilities) if vulnerabilities else f"{Fore.GREEN}✅ Tidak ditemukan XSS/SQLi"

def check_email_leaks(url):
    """ Mengecek kebocoran email di halaman website. """
    response = get_response(url)
    if not response:
        return ""

    emails = set(re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', response.text))
    emails = {email for email in emails if not email.endswith(('example.com', 'test.com'))}

    if emails:
        return f"{Fore.RED}⚠️ Email terpapar: {', '.join(emails)}"
    return f"{Fore.GREEN}✅ Tidak ada email terpapar"

def scan_website(url):
    """ Memulai scanning keamanan pada website. """
    print(f"\n{Fore.YELLOW}🔍 Memulai scan keamanan untuk: {url}")
    print(f"{Fore.MAGENTA}=== HASIL PEMERIKSAAN ==={Style.RESET_ALL}")

    checks = [
        ("Status HTTP", check_http_status),
        ("SSL/TLS", check_ssl),
        ("Header Keamanan", check_security_headers),
        ("Path Sensitif", check_sensitive_paths),
        ("Kerentanan", check_xss_sqli),
        ("Kebocoran Email", check_email_leaks)
    ]

    for name, func in checks:
        print(f"\n{Fore.BLUE}=== {name} ===")
        print(func(url))

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Website Security Scanner')
    parser.add_argument('url', help='URL website yang akan di-scan')
    args = parser.parse_args()

    scan_website(args.url)
