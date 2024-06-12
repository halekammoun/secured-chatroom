from cryptography import x509
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.x509 import load_pem_x509_certificate

def verify_certificate_signature(user_cert_path, ca_cert_path):
    try:
        with open(ca_cert_path, "rb") as f:
            ca_certificate = load_pem_x509_certificate(f.read())
    

        ca_public_key = ca_certificate.public_key()

        with open(user_cert_path, "rb") as f:
            user_cert = load_pem_x509_certificate(f.read())

        ca_public_key.verify(
            user_cert.signature,
            user_cert.tbs_certificate_bytes,
            padding.PKCS1v15(),
            user_cert.signature_hash_algorithm,
        )
        return True
    except:
        return False


result = verify_certificate_signature('reciever/user_certificate.pem', 'CA/server.crt')


