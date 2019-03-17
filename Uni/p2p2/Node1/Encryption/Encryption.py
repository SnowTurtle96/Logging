from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.serialization import load_pem_public_key
import logging


class Encryption:
    private_key = None
    public_key = None
    ciphertext = ''
    plaintext = ''

    def generate_keys(self):
        logging.info("Generating our asymmetric public and private key")
        private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=4096,
        backend=default_backend())

        self.public_key = private_key.public_key()
        self.private_key = private_key
        self.save_key(private_key, "privatekey")

    def getPrivateKey(self):
        logging.info("Retrieving our asymmetric private key")
        return self.private_key

    def getPublicKey(self):
        logging.info("Retreiving our asymmetric public key")
        pem_public_key = self.public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo)
        # pem = pem_public_key.splitlines()

        with open("publickey", 'wb') as pem_out:
            pem_out.write(pem_public_key)

        return pem_public_key



    def save_key(self, key, filename):
        logging.info("Saving our public/private key to file")
        pem = key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )

        with open(filename, 'wb') as pem_out:
            pem_out.write(pem)


    def encrypt(self, key, message):
        logging.info("Encrypting a message with asymmetric key")
        key = key.encode("utf-8")

        public_key = load_pem_public_key(key, default_backend())

        message = bytes(message, encoding="utf-8")
        ciphertext = public_key.encrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA1()),
            algorithm=hashes.SHA1(),
        label = None  ) )
        print(ciphertext)
        return ciphertext


    def decrypt(self, key, message):
        logging.info("Decrypting a message with asymmetric key")
        with open("privatekey", "rb") as key_file:
            private_key = serialization.load_pem_private_key(
            key_file.read(),
            password = None,
            backend = default_backend())
        message = private_key.decrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA1()),
            algorithm=hashes.SHA1(),
        label=None
    )
)

        return message







