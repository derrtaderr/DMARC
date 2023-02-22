import dns.resolver
import re

def check_dmarc(domain):
    try:
        answers = dns.resolver.resolve(f"_dmarc.{domain}", 'TXT')
        for rdata in answers:
            if "v=DMARC1" in rdata.to_text():
                return True
        return False
    except dns.resolver.NXDOMAIN:
        return False

def check_dkim(domain):
    try:
        answers = dns.resolver.resolve(f"default._domainkey.{domain}", 'TXT')
        for rdata in answers:
            if "v=DKIM1" in rdata.to_text():
                return True
        return False
    except dns.resolver.NXDOMAIN:
        return False

def check_spf(domain):
    try:
        answers = dns.resolver.resolve(f"{domain}", 'TXT')
        for rdata in answers:
            if "v=spf1" in rdata.to_text():
                return True
        return False
    except dns.resolver.NXDOMAIN:
        return False

def check_spamhaus_zen(domain):
    try:
        answers = dns.resolver.resolve(f"zen.spamhaus.org", 'A', 'IN', domain)
        for rdata in answers:
            if rdata.address == '127.0.0.2':
                return True
        return False
    except dns.resolver.NoAnswer:
        return "NoAnswer: The DNS response does not contain an answer to the question."
    except dns.resolver.NXDOMAIN:
        return False
def get_email_provider(domain):
    try:
        answers = dns.resolver.resolve(f"{domain}", 'MX')
        return answers[0].to_text().split(" ")[1][:-1]
    except dns.resolver.NXDOMAIN:
        return None

email = input("Enter an email address: ")
match = re.search(r'@([\w.]+)', email)
if match:
    domain = match.group(1)
    print(f"DMARC: {check_dmarc(domain)}")
    print(f"DKIM: {check_dkim(domain)}")
    print(f"SPF: {check_spf(domain)}")
    print(f"Spamhaus BL: {check_spamhaus_zen(domain)}")
    email_provider = get_email_provider(domain)
    if email_provider:
        print(f"Email provider: {email_provider}")
    else:
        print("Invalid email address")
else:
    print("Invalid email address")



