from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat, NoEncryption
from cryptography.hazmat.backends import default_backend
from datetime import datetime, timedelta




def generate_keys_and_csr(common_name):
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )

    public_key = private_key.public_key()
    csr = x509.CertificateSigningRequestBuilder().subject_name(x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, common_name),
    ])).add_extension(
        x509.SubjectAlternativeName([x509.DNSName(common_name)]),
        critical=False,
    ).sign(private_key, hashes.SHA256())
    private_key_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )
    public_key_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    csr_bytes = csr.public_bytes(serialization.Encoding.PEM)
    return private_key_bytes, public_key_bytes, csr_bytes

common_name = ""
private_key, public_key, csr = generate_keys_and_csr(common_name)

with open("reciever/private_key.pem", "w") as file:
    file.write(private_key.decode())
with open("reciever/public_key.pem", "w") as file:
    file.write(public_key.decode())
with open("reciever/csr.pem", "w") as file:
    file.write(csr.decode())


    
ca_private_key_path = "CA/server.key"  # Path to the CA's private key
ca_certificate_path = "CA/server.crt"  # Path to the CA's certificate

with open(ca_private_key_path, "rb") as f:
    ca_private_key = serialization.load_pem_private_key(
        f.read(),
        password=None,  
    )
with open(ca_certificate_path, "rb") as f:
    ca_cert = x509.load_pem_x509_certificate(f.read())
with open("reciever/csr.pem", "rb") as f:
    user_csr = x509.load_pem_x509_csr(f.read())

if user_csr.is_signature_valid:
    subject = user_csr.subject
    issuer = ca_cert.subject
    certificate = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(user_csr.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.utcnow())
        .not_valid_after(datetime.utcnow() + timedelta(days=365))  # 1 year validity
        .sign(ca_private_key, hashes.SHA256())
    )
    with open("reciever/user_certificate.pem", "wb") as f:
        f.write(certificate.public_bytes(Encoding.PEM))

