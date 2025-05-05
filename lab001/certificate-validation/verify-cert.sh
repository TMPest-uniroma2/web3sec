#!/usr/bin/env bash

# CRL Check
echo " ================ CRL Check =============== "
echo "[*] Downloading cert for google.com"
openssl s_client -connect google.com:443 -showcerts 2>&1 < /dev/null > cert.pem
echo "[*] Saved to: cert.pem"

CRL_URL="$(openssl x509 -noout -text -in cert.pem | grep CRL -A 2 | grep -oP 'http://.*')"
echo "[+] CRL Url: $CRL_URL"
wget "$CRL_URL" -O cert.crl 2>/dev/null

openssl crl -inform DER -in cert.crl -outform PEM -out crl.pem

if [ -f "chain.pem" ]; then
  rm -f "chain.pem"
fi

OLDIFS=$IFS; IFS=':' certificates=$(openssl s_client -connect google.com:443 -showcerts -tlsextdebug 2>&1 </dev/null | sed -n '/-----BEGIN/,/-----END/ {/-----BEGIN/ s/^/:/; p}'); for certificate in ${certificates#:}; do echo $certificate >> chain.pem ; done; IFS=$OLDIFS
cat chain.pem crl.pem > crl_chain.pem
openssl verify -crl_check -CAfile crl_chain.pem cert.pem

echo " =============== OCSP Check =============== "
echo "[*] Downloading cert for google.com"
openssl s_client -connect google.com:443 -showcerts 2>&1 < /dev/null > cert.pem
echo "[*] Saved to: cert.pem"

awk '/-----BEGIN CERTIFICATE-----/ {count++} count > 1' cert.pem > root.pem
OCSP_URL=$(openssl x509 -noout -ocsp_uri -in cert.pem)
echo "[+] OCSP Url: $OCSP_URL"
openssl ocsp -issuer root.pem -cert cert.pem -text -url "$OCSP_URL" 2>/dev/null | grep "cert.pem"

rm -f crl.pem
rm -f cert.crl
rm -f chain.pem
rm -f cert.pem
rm -f root.pem
rm -f crl_chain.pem
