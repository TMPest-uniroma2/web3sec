# Lab 001: Foundational Understanding of PKI

This lab is designed to give participants a practical understanding of the cryptographic and certificate-based trust mechanisms used in blockchain networks and secure communications. The exercises focus on Public Key Infrastructure (PKI), digital certificates, and real-world tools for certificate inspection and validation.

## Objectives

- Trace the process of resolving a domain to an IP and retrieving its SSL certificate
- Analyze the certificate chain and inspect fields manually
- Validate revocation status using OCSP and CRL
- Create a self-signed SSL certificate
- Generate a custom CA and issue signed certificates through a local CA manager

## Prerequisites

- Linux shell (native or WSL)
- Installed tools: `nslookup`, `nmap`, `openssl`, `sslscan`, `curl`, `bash`
- CA Manager tool (install via `./camanager/scripts/install.sh`)

## Tasks

### 1. Inspect TLS Connection from Domain to Certificate

**Steps:**

```bash
# Resolve domain
nslookup example.com

# Port scan to identify open services
nmap example.com -p 443

# Retrieve and inspect SSL/TLS information
sslscan example.com:443

# Manually retrieve and view certificate with OpenSSL
openssl s_client -connect example.com:443
````

Analyze:

* Subject and issuer fields
* Validity dates
* Key usage and extensions
* Certificate chain (Root CA, Intermediate, Leaf)

---

### 2. Verify Certificate Revocation

Use the provided script (`verify-cert.sh`) to check the revocation status of a certificate using OCSP and CRL:

```bash
./certificate-validation/verify-cert.sh example.com
```

This will:

* Extract the certificate
* Parse OCSP/CRL distribution points
* Perform live checks

---

### 3. Generate a Self-Signed SSL Certificate

Use OpenSSL to generate a new key and certificate:

```bash
openssl genpkey -algorithm RSA -out server.key
openssl req -new -key server.key -out server.csr
openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt
```

You can inspect the certificate:

```bash
openssl x509 -in server.crt -text -noout
```

---

### 4. Use CA Manager to Simulate a Certificate Authority

Navigate to the `./camanager/` directory and use the tool to:

* Generate a Root CA certificate
* Create an intermediate CA
* Sign leaf certificates from the CA chain

```bash
camanager native -o ./certs -c config.ini
```

Validate the chain with:

```bash
openssl verify -CAfile full-chain.pem test.local.crt
```

---

## Deliverables

* Extracted certificate fields from a real domain
* Output of OCSP/CRL check script
* Self-signed certificate files
* CA-signed certificate issued via camanager

