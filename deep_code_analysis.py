#!/usr/bin/env python3
"""
🔬 TIEFE CODE ANALYSE - FRONTRUNNER OUTFITTERS
Vollständige technische Forensik mit Python
"""

import requests
import json
import ssl
import socket
import hashlib
import base64
import re
import time
from datetime import datetime
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import whois
from cryptography import x509
from cryptography.hazmat.backends import default_backend
import subprocess
import sys

class DeepCodeAnalyzer:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36'
        })
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'domain_analysis': {},
            'security_analysis': {},
            'code_analysis': {},
            'network_analysis': {},
            'ssl_analysis': {},
            'dns_analysis': {},
            'infrastructure_analysis': {}
        }
    
    def analyze_domain(self, domain):
        """Domain-Analyse mit WHOIS und DNS"""
        print(f"Analysiere Domain: {domain}")
        
        try:
            # WHOIS Analyse
            w = whois.whois(domain)
            self.results['domain_analysis']['whois'] = {
                'registrar': w.registrar,
                'creation_date': str(w.creation_date) if w.creation_date else None,
                'expiration_date': str(w.expiration_date) if w.expiration_date else None,
                'updated_date': str(w.last_updated) if w.last_updated else None,
                'name_servers': w.name_servers,
                'registrant': w.registrant,
                'admin_email': w.admin_email,
                'tech_email': w.tech_email
            }
        except Exception as e:
            self.results['domain_analysis']['whois_error'] = str(e)
        
        # DNS Analyse
        try:
            ip_info = socket.gethostbyname_ex(domain)
            self.results['dns_analysis'] = {
                'hostname': ip_info[0],
                'aliases': ip_info[1],
                'ip_addresses': ip_info[2],
                'reverse_lookup': {}
            }
            
            # Reverse DNS Lookup
            for ip in ip_info[2]:
                try:
                    reverse = socket.gethostbyaddr(ip)
                    self.results['dns_analysis']['reverse_lookup'][ip] = reverse[0]
                except:
                    self.results['dns_analysis']['reverse_lookup'][ip] = "No reverse DNS"
                    
        except Exception as e:
            self.results['dns_analysis']['error'] = str(e)
    
    def analyze_ssl_certificate(self, domain):
        """SSL/Zertifikat-Analyse"""
        print(f"Analysiere SSL-Zertifikat: {domain}")
        
        try:
            # SSL-Zertifikat abrufen
            context = ssl.create_default_context()
            with socket.create_connection((domain, 443), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=domain) as ssock:
                    cert_der = ssock.getpeercert(binary_form=True)
                    cert_pem = ssock.getpeercert()
                    
                    # Zertifikat parsen
                    cert = x509.load_der_x509_certificate(cert_der, default_backend())
                    
                    self.results['ssl_analysis'] = {
                        'subject': dict(cert_pem['subject']),
                        'issuer': dict(cert_pem['issuer']),
                        'version': cert.version.name,
                        'serial_number': str(cert.serial_number),
                        'not_before': cert_pem['notBefore'],
                        'not_after': cert_pem['notAfter'],
                        'signature_algorithm': cert.signature_algorithm_oid._name,
                        'public_key_algorithm': cert.public_key().__class__.__name__,
                        'key_size': cert.public_key().key_size if hasattr(cert.public_key(), 'key_size') else None,
                        'subject_alt_names': cert_pem.get('subjectAltName', []),
                        'fingerprint_sha256': hashlib.sha256(cert_der).hexdigest(),
                        'days_until_expiry': (datetime.strptime(cert_pem['notAfter'], '%b %d %H:%M:%S %Y %Z') - datetime.now()).days
                    }
        except Exception as e:
            self.results['ssl_analysis']['error'] = str(e)
    
    def analyze_website_code(self, url):
        """Tiefen-Code-Analyse der Website"""
        print(f"Analysiere Website-Code: {url}")
        
        try:
            response = self.session.get(url, timeout=30, allow_redirects=True)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # HTML-Struktur Analyse
            self.results['code_analysis']['html_structure'] = {
                'title': soup.title.string if soup.title else None,
                'meta_tags': self._analyze_meta_tags(soup),
                'head_tags': len(soup.find_all('head')),
                'body_tags': len(soup.find_all('body')),
                'total_elements': len(soup.find_all()),
                'div_count': len(soup.find_all('div')),
                'script_tags': self._analyze_scripts(soup),
                'link_tags': self._analyze_links(soup),
                'img_tags': self._analyze_images(soup),
                'forms': self._analyze_forms(soup)
            }
            
            # JavaScript-Analyse
            self.results['code_analysis']['javascript'] = self._analyze_javascript(soup)
            
            # CSS-Analyse
            self.results['code_analysis']['css'] = self._analyze_css(soup)
            
            # Security Headers
            self.results['security_analysis']['headers'] = dict(response.headers)
            self.results['security_analysis']['security_headers'] = self._check_security_headers(response.headers)
            
            # Content-Analyse
            self.results['code_analysis']['content'] = self._analyze_content(soup, response.text)
            
        except Exception as e:
            self.results['code_analysis']['error'] = str(e)
    
    def _analyze_meta_tags(self, soup):
        """Meta-Tags analysieren"""
        meta_tags = []
        for meta in soup.find_all('meta'):
            tag_data = {
                'name': meta.get('name', meta.get('property', '')),
                'content': meta.get('content', ''),
                'charset': meta.get('charset', ''),
                'http_equiv': meta.get('http-equiv', '')
            }
            if tag_data['name'] or tag_data['content']:
                meta_tags.append(tag_data)
        return meta_tags
    
    def _analyze_scripts(self, soup):
        """Script-Tags analysieren"""
        scripts = []
        for script in soup.find_all('script'):
            script_data = {
                'src': script.get('src', ''),
                'type': script.get('type', ''),
                'async': script.has_attr('async'),
                'defer': script.has_attr('defer'),
                'integrity': script.get('integrity', ''),
                'crossorigin': script.get('crossorigin', ''),
                'content_length': len(script.string) if script.string else 0
            }
            scripts.append(script_data)
        return scripts
    
    def _analyze_links(self, soup):
        """Link-Tags analysieren"""
        links = []
        for link in soup.find_all('link'):
            link_data = {
                'rel': link.get('rel', []),
                'href': link.get('href', ''),
                'type': link.get('type', ''),
                'sizes': link.get('sizes', ''),
                'media': link.get('media', ''),
                'crossorigin': link.get('crossorigin', '')
            }
            links.append(link_data)
        return links
    
    def _analyze_images(self, soup):
        """Image-Tags analysieren"""
        images = []
        for img in soup.find_all('img'):
            img_data = {
                'src': img.get('src', ''),
                'alt': img.get('alt', ''),
                'width': img.get('width', ''),
                'height': img.get('height', ''),
                'loading': img.get('loading', ''),
                'srcset': img.get('srcset', '')
            }
            images.append(img_data)
        return images
    
    def _analyze_forms(self, soup):
        """Formulare analysieren"""
        forms = []
        for form in soup.find_all('form'):
            form_data = {
                'action': form.get('action', ''),
                'method': form.get('method', ''),
                'enctype': form.get('enctype', ''),
                'target': form.get('target', ''),
                'input_count': len(form.find_all('input')),
                'textarea_count': len(form.find_all('textarea')),
                'select_count': len(form.find_all('select')),
                'has_validation': not form.has_attr('novalidate')
            }
            forms.append(form_data)
        return forms
    
    def _analyze_javascript(self, soup):
        """JavaScript-Analyse"""
        js_analysis = {
            'external_scripts': [],
            'inline_scripts': [],
            'frameworks_detected': [],
            'tracking_scripts': [],
            'security_issues': []
        }
        
        for script in soup.find_all('script'):
            src = script.get('src', '')
            if src:
                js_analysis['external_scripts'].append(src)
                # Framework Detection
                if any(fw in src.lower() for fw in ['jquery', 'react', 'angular', 'vue']):
                    js_analysis['frameworks_detected'].append(src)
                # Tracking Detection
                if any(tracker in src.lower() for tracker in ['google-analytics', 'facebook', 'hotjar', 'doubleclick']):
                    js_analysis['tracking_scripts'].append(src)
            elif script.string:
                js_analysis['inline_scripts'].append({
                    'length': len(script.string),
                    'has_eval': 'eval(' in script.string,
                    'has_innerhtml': 'innerHTML' in script.string,
                    'has_documentwrite': 'document.write' in script.string
                })
        
        return js_analysis
    
    def _analyze_css(self, soup):
        """CSS-Analyse"""
        css_analysis = {
            'external_stylesheets': [],
            'inline_styles': [],
            'style_tags': []
        }
        
        # Link tags für CSS
        for link in soup.find_all('link'):
            if link.get('rel') and 'stylesheet' in link.get('rel'):
                css_analysis['external_stylesheets'].append({
                    'href': link.get('href', ''),
                    'integrity': link.get('integrity', ''),
                    'crossorigin': link.get('crossorigin', '')
                })
        
        # Style tags
        for style in soup.find_all('style'):
            css_analysis['style_tags'].append({
                'length': len(style.string) if style.string else 0,
                'has_important': '!important' in style.string if style.string else False
            })
        
        return css_analysis
    
    def _analyze_content(self, soup, html_content):
        """Content-Analyse"""
        content_analysis = {
            'text_length': len(soup.get_text()),
            'word_count': len(soup.get_text().split()),
            'language_detection': self._detect_language(soup.get_text()),
            'has_tracking_pixels': bool(soup.find_all('img', src=re.compile(r'facebook|google|doubleclick', re.I))),
            'has_iframes': len(soup.find_all('iframe')),
            'comments': self._analyze_html_comments(soup),
            'hidden_elements': len(soup.find_all(style="display:none")) + len(soup.find_all(style="visibility:hidden"))
        }
        
        return content_analysis
    
    def _detect_language(self, text):
        """Einfache Spracherkennung"""
        german_words = ['der', 'die', 'das', 'und', 'ist', 'mit', 'für', 'auf', 'von', 'zu']
        english_words = ['the', 'and', 'is', 'for', 'with', 'from', 'to', 'of', 'in', 'at']
        
        words = text.lower().split()[:100]  # Erste 100 Wörter analysieren
        
        german_count = sum(1 for word in words if word in german_words)
        english_count = sum(1 for word in words if word in english_words)
        
        if german_count > english_count:
            return 'German'
        elif english_count > german_count:
            return 'English'
        else:
            return 'Unknown'
    
    def _analyze_html_comments(self, soup):
        """HTML-Kommentare analysieren"""
        comments = []
        for comment in soup.find_all(string=lambda text: isinstance(text, type(soup.string)) and text.strip().startswith('<!--')):
            comments.append(comment.strip())
        return comments
    
    def _check_security_headers(self, headers):
        """Security Headers prüfen"""
        security_headers = {
            'x_frame_options': headers.get('X-Frame-Options', 'MISSING'),
            'x_content_type_options': headers.get('X-Content-Type-Options', 'MISSING'),
            'x_xss_protection': headers.get('X-XSS-Protection', 'MISSING'),
            'strict_transport_security': headers.get('Strict-Transport-Security', 'MISSING'),
            'content_security_policy': headers.get('Content-Security-Policy', 'MISSING'),
            'referrer_policy': headers.get('Referrer-Policy', 'MISSING')
        }
        return security_headers
    
    def analyze_network_infrastructure(self, domain):
        """Netzwerk-Infrastruktur Analyse"""
        print(f"Analysiere Netzwerk-Infrastruktur: {domain}")
        
        try:
            # IP-Geolokalisierung (einfach)
            ip = socket.gethostbyname(domain)
            
            # Traceroute (Windows)
            try:
                traceroute_result = subprocess.run(['tracert', domain], capture_output=True, text=True, timeout=30)
                self.results['network_analysis']['traceroute'] = traceroute_result.stdout
            except:
                self.results['network_analysis']['traceroute'] = "Traceroute failed"
            
            # Ping Test
            try:
                ping_result = subprocess.run(['ping', '-n', '4', domain], capture_output=True, text=True, timeout=10)
                self.results['network_analysis']['ping'] = ping_result.stdout
            except:
                self.results['network_analysis']['ping'] = "Ping failed"
            
            self.results['network_analysis']['target_ip'] = ip
            
        except Exception as e:
            self.results['network_analysis']['error'] = str(e)
    
    def generate_report(self, output_file):
        """Bericht generieren"""
        print(f"Generiere Bericht: {output_file}")
        
        # JSON-Bericht
        with open(output_file.replace('.md', '.json'), 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False, default=str)
        
        # Markdown-Bericht
        report_md = self._generate_markdown_report()
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report_md)
    
    def _generate_markdown_report(self):
        """Markdown-Bericht generieren"""
        md = []
        md.append("# TIEFE CODE ANALYSE - FRONTRUNNER OUTFITTERS\n")
        md.append(f"**Analyse-Datum**: {self.results['timestamp']}\n")
        
        # Domain-Analyse
        if 'whois' in self.results['domain_analysis']:
            md.append("## DOMAIN ANALYSE\n")
            whois = self.results['domain_analysis']['whois']
            md.append(f"- **Registrar**: {whois.get('registrar', 'N/A')}")
            md.append(f"- **Erstellt**: {whois.get('creation_date', 'N/A')}")
            md.append(f"- **Laeuft ab**: {whois.get('expiration_date', 'N/A')}")
            md.append(f"- **Nameserver**: {', '.join(whois.get('name_servers', []))}")
            md.append("")
        
        # SSL-Analyse
        if 'subject' in self.results['ssl_analysis']:
            md.append("## SSL/ZERTIFIKAT ANALYSE\n")
            ssl = self.results['ssl_analysis']
            md.append(f"- **Aussteller**: {ssl.get('issuer', {}).get('commonName', 'N/A')}")
            md.append(f"- **Subject**: {ssl.get('subject', {}).get('commonName', 'N/A')}")
            md.append(f"- **Gueltig bis**: {ssl.get('not_after', 'N/A')}")
            md.append(f"- **Tage bis zum Ablauf**: {ssl.get('days_until_expiry', 'N/A')}")
            md.append(f"- **Algorithmus**: {ssl.get('signature_algorithm', 'N/A')}")
            md.append("")
        
        # Code-Analyse
        if 'html_structure' in self.results['code_analysis']:
            md.append("## CODE ANALYSE\n")
            html = self.results['code_analysis']['html_structure']
            md.append(f"- **Titel**: {html.get('title', 'N/A')}")
            md.append(f"- **Total Elements**: {html.get('total_elements', 0)}")
            md.append(f"- **Script Tags**: {len(html.get('script_tags', []))}")
            md.append(f"- **External Scripts**: {len([s for s in html.get('script_tags', []) if s.get('src')])}")
            md.append(f"- **Forms**: {len(html.get('forms', []))}")
            md.append("")
        
        # Security-Analyse
        if 'security_headers' in self.results['security_analysis']:
            md.append("## SECURITY ANALYSE\n")
            headers = self.results['security_analysis']['security_headers']
            md.append("### Security Headers:")
            for header, value in headers.items():
                status = "OK" if value != "MISSING" else "MISSING"
                md.append(f"- {status} **{header}**: {value}")
            md.append("")
        
        # Netzwerk-Analyse
        if 'target_ip' in self.results['network_analysis']:
            md.append("## NETZWERK ANALYSE\n")
            net = self.results['network_analysis']
            md.append(f"- **Target IP**: {net.get('target_ip', 'N/A')}")
            md.append(f"- **Ping**: {'Erfolgreich' if 'ping' in net else 'Fehlgeschlagen'}")
            md.append(f"- **Traceroute**: {'Erfolgreich' if 'traceroute' in net else 'Fehlgeschlagen'}")
            md.append("")
        
        return "\n".join(md)

def main():
    """Hauptfunktion"""
    print("Starte tiefe Code-Analyse...")
    
    analyzer = DeepCodeAnalyzer()
    
    # Domain analysieren
    analyzer.analyze_domain("frontrunneroutfitters.com")
    
    # SSL-Zertifikat analysieren
    analyzer.analyze_ssl_certificate("frontrunneroutfitters.com")
    
    # Website-Code analysieren (nach Redirect)
    analyzer.analyze_website_code("https://www.dometic.com/en-de")
    
    # Netzwerk-Infrastruktur analysieren
    analyzer.analyze_network_infrastructure("www.dometic.com")
    
    # Bericht generieren
    analyzer.generate_report("deep_code_analysis_report.md")
    
    print("Analyse abgeschlossen! Berichte erstellt:")
    print("- deep_code_analysis_report.md")
    print("- deep_code_analysis_report.json")

if __name__ == "__main__":
    main()
