# 🔐 Python Security & Cryptography Mastery

## Complete Professional Guide to Secure Python Development

---

## Table of Contents

1. [Cryptography Fundamentals](#cryptography-fundamentals)
2. [Password Security](#password-security)
3. [Symmetric Encryption](#symmetric-encryption)
4. [Asymmetric Encryption](#asymmetric-encryption)
5. [Digital Signatures](#digital-signatures)
6. [SSL/TLS and Certificates](#ssltls-and-certificates)
7. [Secure API Development](#secure-api-development)
8. [OWASP Top 10 Prevention](#owasp-top-10-prevention)
9. [Secrets Management](#secrets-management)
10. [Security Testing](#security-testing)
11. [Production Security Patterns](#production-security-patterns)

---

## 1. Cryptography Fundamentals

### 1.1 Hashing (One-Way Functions)

```python
import hashlib
import hmac
from typing import str, bytes

class SecureHasher:
    """Professional hashing utilities"""

    @staticmethod
    def sha256_hash(data: str) -> str:
        """SHA-256 hash - cryptographically secure"""
        return hashlib.sha256(data.encode()).hexdigest()

    @staticmethod
    def sha512_hash(data: str) -> str:
        """SHA-512 hash - even stronger"""
        return hashlib.sha512(data.encode()).hexdigest()

    @staticmethod
    def hmac_hash(data: str, key: str) -> str:
        """HMAC - Hash-based Message Authentication Code"""
        return hmac.new(
            key.encode(),
            data.encode(),
            hashlib.sha256
        ).hexdigest()

    @staticmethod
    def verify_hmac(data: str, key: str, signature: str) -> bool:
        """Verify HMAC signature - prevents tampering"""
        expected = hmac.new(
            key.encode(),
            data.encode(),
            hashlib.sha256
        ).hexdigest()

        # Use compare_digest to prevent timing attacks
        return hmac.compare_digest(expected, signature)

# Usage
hasher = SecureHasher()

# Basic hashing
data = "sensitive information"
hash_value = hasher.sha256_hash(data)
print(f"SHA-256: {hash_value}")

# Message authentication
secret_key = "my-secret-key-keep-this-safe"
message = "Transfer $1000 to account 12345"
signature = hasher.hmac_hash(message, secret_key)

# Verify message hasn't been tampered
is_valid = hasher.verify_hmac(message, secret_key, signature)
print(f"Message authentic: {is_valid}")
```

### 1.2 Password Hashing with Salt and Pepper

```python
import bcrypt
import secrets
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

class PasswordManager:
    """Production-grade password security"""

    def __init__(self):
        self.ph = PasswordHasher(
            time_cost=3,        # Number of iterations
            memory_cost=65536,  # Memory usage (64 MB)
            parallelism=4,      # Number of parallel threads
            hash_len=32,        # Length of hash
            salt_len=16         # Length of salt
        )
        # Pepper - stored separately from database (environment variable)
        self.pepper = "STORE_THIS_IN_ENV_VAR_NOT_DB"

    def hash_password_bcrypt(self, password: str) -> str:
        """Hash password with bcrypt (industry standard)"""
        # Bcrypt automatically handles salt
        salt = bcrypt.gensalt(rounds=12)  # 12 rounds = 2^12 iterations
        hashed = bcrypt.hashpw(password.encode(), salt)
        return hashed.decode()

    def verify_password_bcrypt(self, password: str, hashed: str) -> bool:
        """Verify password with bcrypt"""
        return bcrypt.checkpw(password.encode(), hashed.encode())

    def hash_password_argon2(self, password: str) -> str:
        """Hash password with Argon2 (most secure, winner of PHC)"""
        # Add pepper before hashing
        peppered = password + self.pepper
        return self.ph.hash(peppered)

    def verify_password_argon2(self, password: str, hashed: str) -> bool:
        """Verify password with Argon2"""
        try:
            peppered = password + self.pepper
            self.ph.verify(hashed, peppered)

            # Check if rehashing is needed (parameters changed)
            if self.ph.check_needs_rehash(hashed):
                print("Password needs rehashing with updated parameters")

            return True
        except VerifyMismatchError:
            return False

    def generate_secure_password(self, length: int = 16) -> str:
        """Generate cryptographically secure password"""
        # Use secrets module, not random!
        alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*"
        return ''.join(secrets.choice(alphabet) for _ in range(length))

    def generate_token(self, nbytes: int = 32) -> str:
        """Generate secure token for password reset, API keys, etc."""
        return secrets.token_urlsafe(nbytes)

# Usage
pm = PasswordManager()

# Register new user
password = "MyS3cur3P@ssw0rd!"
hashed = pm.hash_password_argon2(password)
print(f"Hashed password: {hashed}")

# Login - verify password
is_valid = pm.verify_password_argon2("MyS3cur3P@ssw0rd!", hashed)
print(f"Login successful: {is_valid}")

# Generate password reset token
reset_token = pm.generate_token()
print(f"Reset token: {reset_token}")
```

---

## 2. Symmetric Encryption (AES)

```python
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import os
import base64

class SymmetricEncryption:
    """Professional symmetric encryption"""

    def __init__(self):
        self.backend = default_backend()

    # Method 1: Fernet (Easiest, Recommended for Most Cases)
    def generate_fernet_key(self) -> bytes:
        """Generate Fernet encryption key"""
        return Fernet.generate_key()

    def encrypt_fernet(self, data: str, key: bytes) -> bytes:
        """Encrypt with Fernet (AES-128 in CBC mode)"""
        f = Fernet(key)
        return f.encrypt(data.encode())

    def decrypt_fernet(self, encrypted_data: bytes, key: bytes) -> str:
        """Decrypt with Fernet"""
        f = Fernet(key)
        return f.decrypt(encrypted_data).decode()

    # Method 2: AES-256 (More Control, Production Use)
    def encrypt_aes_256(self, data: str, key: bytes) -> dict:
        """
        Encrypt with AES-256 in CBC mode
        Returns: dict with iv and encrypted data
        """
        # Generate random IV (Initialization Vector)
        iv = os.urandom(16)

        # Create cipher
        cipher = Cipher(
            algorithms.AES(key),  # key must be 32 bytes for AES-256
            modes.CBC(iv),
            backend=self.backend
        )

        # Pad data to block size (16 bytes for AES)
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(data.encode()) + padder.finalize()

        # Encrypt
        encryptor = cipher.encryptor()
        encrypted = encryptor.update(padded_data) + encryptor.finalize()

        return {
            'iv': base64.b64encode(iv).decode(),
            'encrypted': base64.b64encode(encrypted).decode()
        }

    def decrypt_aes_256(self, encrypted_data: dict, key: bytes) -> str:
        """Decrypt AES-256"""
        # Decode from base64
        iv = base64.b64decode(encrypted_data['iv'])
        encrypted = base64.b64decode(encrypted_data['encrypted'])

        # Create cipher
        cipher = Cipher(
            algorithms.AES(key),
            modes.CBC(iv),
            backend=self.backend
        )

        # Decrypt
        decryptor = cipher.decryptor()
        padded_data = decryptor.update(encrypted) + decryptor.finalize()

        # Unpad
        unpadder = padding.PKCS7(128).unpadder()
        data = unpadder.update(padded_data) + unpadder.finalize()

        return data.decode()

# Usage
enc = SymmetricEncryption()

# Simple Fernet encryption
print("=== Fernet Encryption ===")
key = enc.generate_fernet_key()
print(f"Key: {key.decode()}")

secret_message = "This is highly confidential information!"
encrypted = enc.encrypt_fernet(secret_message, key)
print(f"Encrypted: {encrypted}")

decrypted = enc.decrypt_fernet(encrypted, key)
print(f"Decrypted: {decrypted}")

# Advanced AES-256 encryption
print("\n=== AES-256 Encryption ===")
aes_key = os.urandom(32)  # 256 bits
encrypted_data = enc.encrypt_aes_256("Top secret data!", aes_key)
print(f"Encrypted data: {encrypted_data}")

decrypted_data = enc.decrypt_aes_256(encrypted_data, aes_key)
print(f"Decrypted: {decrypted_data}")
```

### 2.1 File Encryption

```python
import os
from pathlib import Path
from cryptography.fernet import Fernet

class FileEncryptor:
    """Encrypt and decrypt files securely"""

    def __init__(self, key: bytes = None):
        self.key = key or Fernet.generate_key()
        self.fernet = Fernet(self.key)

    def save_key(self, filepath: str):
        """Save encryption key to file"""
        with open(filepath, 'wb') as f:
            f.write(self.key)
        print(f"⚠️  Key saved to {filepath} - KEEP THIS SAFE!")

    def load_key(self, filepath: str):
        """Load encryption key from file"""
        with open(filepath, 'rb') as f:
            self.key = f.read()
        self.fernet = Fernet(self.key)

    def encrypt_file(self, input_file: str, output_file: str = None):
        """Encrypt entire file"""
        if output_file is None:
            output_file = input_file + '.encrypted'

        # Read file
        with open(input_file, 'rb') as f:
            data = f.read()

        # Encrypt
        encrypted_data = self.fernet.encrypt(data)

        # Write encrypted file
        with open(output_file, 'wb') as f:
            f.write(encrypted_data)

        print(f"✓ File encrypted: {output_file}")
        return output_file

    def decrypt_file(self, input_file: str, output_file: str = None):
        """Decrypt entire file"""
        if output_file is None:
            output_file = input_file.replace('.encrypted', '.decrypted')

        # Read encrypted file
        with open(input_file, 'rb') as f:
            encrypted_data = f.read()

        # Decrypt
        data = self.fernet.decrypt(encrypted_data)

        # Write decrypted file
        with open(output_file, 'wb') as f:
            f.write(data)

        print(f"✓ File decrypted: {output_file}")
        return output_file

    def encrypt_directory(self, directory: str):
        """Encrypt all files in directory"""
        path = Path(directory)
        encrypted_files = []

        for file in path.rglob('*'):
            if file.is_file() and not file.name.endswith('.encrypted'):
                encrypted = self.encrypt_file(str(file))
                encrypted_files.append(encrypted)
                # Optionally delete original
                # file.unlink()

        print(f"✓ Encrypted {len(encrypted_files)} files")
        return encrypted_files

# Usage
encryptor = FileEncryptor()

# Save key for later use
encryptor.save_key('encryption.key')

# Encrypt a file
encryptor.encrypt_file('sensitive_data.txt')

# Decrypt later
encryptor.load_key('encryption.key')
encryptor.decrypt_file('sensitive_data.txt.encrypted', 'recovered_data.txt')
```

---

## 3. Asymmetric Encryption (RSA)

```python
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend

class AsymmetricEncryption:
    """RSA public/private key cryptography"""

    def __init__(self):
        self.backend = default_backend()
        self.private_key = None
        self.public_key = None

    def generate_keypair(self, key_size: int = 4096):
        """
        Generate RSA key pair
        key_size: 2048 (minimum), 4096 (recommended)
        """
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=key_size,
            backend=self.backend
        )
        self.public_key = self.private_key.public_key()
        print(f"✓ Generated {key_size}-bit RSA keypair")

    def save_private_key(self, filename: str, password: str = None):
        """Save private key to file (encrypted with password)"""
        # Encrypt private key with password
        encryption = serialization.BestAvailableEncryption(password.encode()) if password else serialization.NoEncryption()

        pem = self.private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=encryption
        )

        with open(filename, 'wb') as f:
            f.write(pem)
        print(f"✓ Private key saved: {filename}")

    def save_public_key(self, filename: str):
        """Save public key to file"""
        pem = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        with open(filename, 'wb') as f:
            f.write(pem)
        print(f"✓ Public key saved: {filename}")

    def load_private_key(self, filename: str, password: str = None):
        """Load private key from file"""
        with open(filename, 'rb') as f:
            self.private_key = serialization.load_pem_private_key(
                f.read(),
                password=password.encode() if password else None,
                backend=self.backend
            )
        self.public_key = self.private_key.public_key()

    def load_public_key(self, filename: str):
        """Load public key from file"""
        with open(filename, 'rb') as f:
            self.public_key = serialization.load_pem_public_key(
                f.read(),
                backend=self.backend
            )

    def encrypt(self, message: str) -> bytes:
        """Encrypt with public key (anyone can encrypt)"""
        encrypted = self.public_key.encrypt(
            message.encode(),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return encrypted

    def decrypt(self, encrypted_message: bytes) -> str:
        """Decrypt with private key (only owner can decrypt)"""
        decrypted = self.private_key.decrypt(
            encrypted_message,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return decrypted.decode()

# Usage - Secure Communication Example
print("=== Alice wants to send Bob a secret message ===\n")

# Bob generates keypair and shares public key
bob = AsymmetricEncryption()
bob.generate_keypair(key_size=2048)  # Smaller key for demo
bob.save_public_key('bob_public.pem')
bob.save_private_key('bob_private.pem', password='bob_secret_password')

# Alice loads Bob's public key
alice = AsymmetricEncryption()
alice.load_public_key('bob_public.pem')

# Alice encrypts message with Bob's public key
secret_message = "Bob, the nuclear codes are 12345"
encrypted = alice.encrypt(secret_message)
print(f"Alice encrypted: {encrypted[:50]}...")

# Alice sends encrypted message to Bob...

# Bob decrypts with his private key
bob_receiver = AsymmetricEncryption()
bob_receiver.load_private_key('bob_private.pem', password='bob_secret_password')
decrypted = bob_receiver.decrypt(encrypted)
print(f"Bob decrypted: {decrypted}")
```

---

## 4. Digital Signatures

```python
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature

class DigitalSignature:
    """Sign and verify messages to ensure authenticity"""

    def __init__(self):
        self.private_key = None
        self.public_key = None

    def generate_keypair(self):
        """Generate signing keypair"""
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        self.public_key = self.private_key.public_key()

    def sign_message(self, message: str) -> bytes:
        """Sign message with private key"""
        signature = self.private_key.sign(
            message.encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return signature

    def verify_signature(self, message: str, signature: bytes, public_key=None) -> bool:
        """Verify signature with public key"""
        key = public_key or self.public_key

        try:
            key.verify(
                signature,
                message.encode(),
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except InvalidSignature:
            return False

# Usage - Software Distribution Example
print("=== Software Publisher Signs Release ===\n")

# Publisher generates keypair
publisher = DigitalSignature()
publisher.generate_keypair()

# Publisher creates software release
software_content = "MyApp v2.0 - installer.exe - checksum:abc123"

# Publisher signs the release
signature = publisher.sign_message(software_content)
print(f"Publisher signed release: {signature[:50]}...")

# User downloads software and signature
# User has publisher's public key (distributed securely)

# User verifies signature before installing
is_authentic = publisher.verify_signature(software_content, signature)
print(f"\n✓ Software authentic: {is_authentic}")

# Attacker tries to tamper
tampered_content = "MyApp v2.0 - installer.exe - checksum:xyz789 [MALWARE]"
is_tampered = publisher.verify_signature(tampered_content, signature)
print(f"✗ Tampered software verified: {is_tampered}")
```

---

## 5. OWASP Top 10 Prevention in Python

### 5.1 SQL Injection Prevention

```python
import sqlite3
from typing import List, Tuple
import re

class SecureDatabase:
    """SQL injection prevention"""

    def __init__(self, db_path: str):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    # ❌ VULNERABLE - NEVER DO THIS
    def get_user_vulnerable(self, username: str):
        """VULNERABLE to SQL injection!"""
        query = f"SELECT * FROM users WHERE username = '{username}'"
        # Attacker input: admin' OR '1'='1
        # Executed: SELECT * FROM users WHERE username = 'admin' OR '1'='1'
        # Returns ALL users!
        return self.cursor.execute(query).fetchall()

    # ✅ SECURE - Always use parameterized queries
    def get_user_secure(self, username: str):
        """SECURE - parameterized query"""
        query = "SELECT * FROM users WHERE username = ?"
        return self.cursor.execute(query, (username,)).fetchall()

    def get_users_by_role_secure(self, role: str, active: bool):
        """SECURE - multiple parameters"""
        query = """
            SELECT id, username, email
            FROM users
            WHERE role = ? AND active = ?
        """
        return self.cursor.execute(query, (role, active)).fetchall()

    def search_users_secure(self, search_term: str):
        """SECURE - even with LIKE"""
        # Sanitize input - remove SQL wildcards
        safe_term = search_term.replace('%', '').replace('_', '')
        query = "SELECT * FROM users WHERE username LIKE ?"
        return self.cursor.execute(query, (f'%{safe_term}%',)).fetchall()

# Using SQLAlchemy ORM (Even More Secure)
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    email = Column(String(100))
    role = Column(String(20))

class SecureUserRepository:
    """ORM prevents SQL injection automatically"""

    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def get_user_by_username(self, username: str) -> User:
        """ORM automatically parameterizes"""
        return self.session.query(User).filter(
            User.username == username
        ).first()

    def search_users(self, search_term: str) -> List[User]:
        """Safe search with ORM"""
        return self.session.query(User).filter(
            User.username.like(f'%{search_term}%')
        ).all()
```

### 5.2 XSS (Cross-Site Scripting) Prevention

```python
import html
import re
from markupsafe import escape
from bleach import clean

class XSSPrevention:
    """Prevent XSS attacks"""

    @staticmethod
    def escape_html(user_input: str) -> str:
        """Escape HTML entities"""
        return html.escape(user_input)

    @staticmethod
    def sanitize_html(user_input: str, allowed_tags: List[str] = None) -> str:
        """
        Clean HTML, allowing only safe tags
        Use for rich text editors, comments, etc.
        """
        if allowed_tags is None:
            allowed_tags = ['p', 'br', 'strong', 'em', 'u', 'a']

        allowed_attributes = {
            'a': ['href', 'title'],
        }

        # Remove dangerous HTML
        clean_html = clean(
            user_input,
            tags=allowed_tags,
            attributes=allowed_attributes,
            strip=True
        )

        return clean_html

    @staticmethod
    def sanitize_url(url: str) -> str:
        """Validate and sanitize URLs"""
        # Only allow http, https, mailto
        if not re.match(r'^(https?://|mailto:)', url):
            return ''

        # Block javascript: protocol
        if 'javascript:' in url.lower():
            return ''

        return url

# Flask example
from flask import Flask, request, render_template_string

app = Flask(__name__)
xss = XSSPrevention()

@app.route('/comment', methods=['POST'])
def submit_comment():
    user_comment = request.form.get('comment', '')

    # ❌ VULNERABLE
    # return f"<div>{user_comment}</div>"  # XSS if user inputs <script>alert('XSS')</script>

    # ✅ SECURE - Option 1: Escape everything
    safe_comment = xss.escape_html(user_comment)
    return f"<div>{safe_comment}</div>"

    # ✅ SECURE - Option 2: Allow some HTML tags
    # safe_comment = xss.sanitize_html(user_comment)
    # return f"<div>{safe_comment}</div>"

# Jinja2 templates auto-escape by default
template = """
<div class="comment">
    {{ comment }}  <!-- Auto-escaped! -->
</div>
"""

@app.route('/display')
def display_comment():
    user_comment = request.args.get('comment', '')
    # Jinja2 automatically escapes variables
    return render_template_string(template, comment=user_comment)
```

### 5.3 CSRF (Cross-Site Request Forgery) Prevention

```python
from flask import Flask, session, request, abort
from flask_wtf.csrf import CSRFProtect
import secrets

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(32)

# Enable CSRF protection globally
csrf = CSRFProtect(app)

# Manual CSRF token generation
class CSRFProtection:
    """Manual CSRF protection"""

    @staticmethod
    def generate_csrf_token() -> str:
        """Generate CSRF token"""
        if '_csrf_token' not in session:
            session['_csrf_token'] = secrets.token_hex(32)
        return session['_csrf_token']

    @staticmethod
    def validate_csrf_token(token: str) -> bool:
        """Validate CSRF token"""
        if '_csrf_token' not in session:
            return False

        return secrets.compare_digest(session['_csrf_token'], token)

@app.route('/transfer', methods=['POST'])
def transfer_money():
    # Get CSRF token from form
    csrf_token = request.form.get('csrf_token')

    # Validate token
    if not CSRFProtection.validate_csrf_token(csrf_token):
        abort(403, "Invalid CSRF token")

    # Process transfer
    amount = request.form.get('amount')
    recipient = request.form.get('recipient')
    # ... perform transfer

    return "Transfer successful"

# HTML form includes CSRF token
"""
<form method="POST" action="/transfer">
    <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
    <input type="text" name="amount">
    <input type="text" name="recipient">
    <button type="submit">Transfer</button>
</form>
"""
```

### 5.4 Secure Authentication & Session Management

```python
from flask import Flask, session, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from datetime import timedelta
import secrets

app = Flask(__name__)
app.config.update(
    SECRET_KEY=secrets.token_hex(32),
    SESSION_COOKIE_SECURE=True,  # Only send over HTTPS
    SESSION_COOKIE_HTTPONLY=True,  # Prevent JavaScript access
    SESSION_COOKIE_SAMESITE='Lax',  # CSRF protection
    PERMANENT_SESSION_LIFETIME=timedelta(hours=1),  # Session timeout
    SESSION_COOKIE_NAME='__Host-session'  # Prevent subdomain attacks
)

login_manager = LoginManager()
login_manager.init_app(app)

class SecureUser(UserMixin):
    """Secure user model"""

    def __init__(self, user_id, username, password_hash):
        self.id = user_id
        self.username = username
        self.password_hash = password_hash
        self.failed_login_attempts = 0
        self.locked_until = None

    def verify_password(self, password: str) -> bool:
        """Verify password with bcrypt"""
        pm = PasswordManager()
        return pm.verify_password_argon2(password, self.password_hash)

    def is_locked(self) -> bool:
        """Check if account is locked"""
        if self.locked_until is None:
            return False

        from datetime import datetime
        return datetime.now() < self.locked_until

    def record_failed_login(self):
        """Record failed login attempt"""
        self.failed_login_attempts += 1

        # Lock account after 5 failed attempts
        if self.failed_login_attempts >= 5:
            from datetime import datetime, timedelta
            self.locked_until = datetime.now() + timedelta(minutes=30)

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    # Get user from database
    user = get_user_from_db(username)  # Implement this

    if not user:
        # Don't reveal if user exists or not
        return "Invalid credentials", 401

    if user.is_locked():
        return "Account locked. Try again later.", 403

    if not user.verify_password(password):
        user.record_failed_login()
        return "Invalid credentials", 401

    # Reset failed attempts on successful login
    user.failed_login_attempts = 0
    user.locked_until = None

    # Login user
    login_user(user, remember=True)

    # Regenerate session ID to prevent session fixation
    session.regenerate()

    return redirect(url_for('dashboard'))

@app.route('/dashboard')
@login_required
def dashboard():
    return "Welcome to your dashboard"
```

### 5.5 Input Validation & Sanitization

```python
from typing import Optional
import re
from email_validator import validate_email, EmailNotValidError

class InputValidator:
    """Professional input validation"""

    @staticmethod
    def validate_username(username: str) -> Tuple[bool, Optional[str]]:
        """
        Validate username
        Returns: (is_valid, error_message)
        """
        if not username:
            return False, "Username is required"

        if len(username) < 3:
            return False, "Username must be at least 3 characters"

        if len(username) > 20:
            return False, "Username must be less than 20 characters"

        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            return False, "Username can only contain letters, numbers, and underscores"

        return True, None

    @staticmethod
    def validate_email_address(email: str) -> Tuple[bool, Optional[str]]:
        """Validate email with comprehensive checks"""
        try:
            # Validate and normalize
            validated = validate_email(email, check_deliverability=True)
            return True, None
        except EmailNotValidError as e:
            return False, str(e)

    @staticmethod
    def validate_password_strength(password: str) -> Tuple[bool, List[str]]:
        """
        Validate password strength
        Returns: (is_valid, list_of_errors)
        """
        errors = []

        if len(password) < 12:
            errors.append("Password must be at least 12 characters")

        if not re.search(r'[A-Z]', password):
            errors.append("Password must contain at least one uppercase letter")

        if not re.search(r'[a-z]', password):
            errors.append("Password must contain at least one lowercase letter")

        if not re.search(r'[0-9]', password):
            errors.append("Password must contain at least one number")

        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            errors.append("Password must contain at least one special character")

        # Check against common passwords
        common_passwords = ['password123', 'qwerty123', 'admin123']
        if password.lower() in common_passwords:
            errors.append("Password is too common")

        return len(errors) == 0, errors

    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """Sanitize filename to prevent directory traversal"""
        # Remove path components
        filename = os.path.basename(filename)

        # Remove dangerous characters
        filename = re.sub(r'[^\w\s.-]', '', filename)

        # Prevent hidden files
        if filename.startswith('.'):
            filename = '_' + filename

        return filename

    @staticmethod
    def validate_phone_number(phone: str) -> Tuple[bool, Optional[str]]:
        """Validate phone number (US format)"""
        # Remove formatting
        digits = re.sub(r'\D', '', phone)

        if len(digits) != 10:
            return False, "Phone number must be 10 digits"

        return True, None

    @staticmethod
    def validate_credit_card(card_number: str) -> Tuple[bool, Optional[str]]:
        """Validate credit card with Luhn algorithm"""
        # Remove spaces and dashes
        card = re.sub(r'[\s-]', '', card_number)

        if not card.isdigit():
            return False, "Card number must contain only digits"

        if len(card) not in [13, 15, 16]:
            return False, "Invalid card number length"

        # Luhn algorithm
        def luhn_check(card_num: str) -> bool:
            digits = [int(d) for d in card_num]
            checksum = 0

            # Double every second digit from right
            for i in range(len(digits) - 2, -1, -2):
                digits[i] *= 2
                if digits[i] > 9:
                    digits[i] -= 9

            return sum(digits) % 10 == 0

        if not luhn_check(card):
            return False, "Invalid card number"

        return True, None

# Usage
validator = InputValidator()

# Validate username
is_valid, error = validator.validate_username("john_doe123")
print(f"Username valid: {is_valid}")

# Validate email
is_valid, error = validator.validate_email_address("user@example.com")
print(f"Email valid: {is_valid}")

# Validate password
is_valid, errors = validator.validate_password_strength("MyP@ssw0rd2024")
if not is_valid:
    print("Password errors:", errors)
```

---

## 6. Secrets Management

```python
import os
from pathlib import Path
from cryptography.fernet import Fernet
import json
from typing import Dict, Any

class SecretsManager:
    """Secure secrets management"""

    def __init__(self, secrets_file: str = '.secrets.encrypted'):
        self.secrets_file = secrets_file
        self.key = self._get_or_create_key()
        self.fernet = Fernet(self.key)
        self.secrets = self._load_secrets()

    def _get_or_create_key(self) -> bytes:
        """Get encryption key from environment or file"""
        # Best: Load from environment variable
        key_env = os.getenv('SECRETS_KEY')
        if key_env:
            return key_env.encode()

        # Alternative: Load from secure file outside project
        key_file = Path.home() / '.secrets_key'
        if key_file.exists():
            return key_file.read_bytes()

        # Create new key
        key = Fernet.generate_key()
        key_file.write_bytes(key)
        print(f"⚠️  Created new secrets key: {key_file}")
        return key

    def _load_secrets(self) -> Dict[str, Any]:
        """Load encrypted secrets"""
        if not Path(self.secrets_file).exists():
            return {}

        with open(self.secrets_file, 'rb') as f:
            encrypted = f.read()

        decrypted = self.fernet.decrypt(encrypted)
        return json.loads(decrypted)

    def _save_secrets(self):
        """Save encrypted secrets"""
        json_data = json.dumps(self.secrets, indent=2)
        encrypted = self.fernet.encrypt(json_data.encode())

        with open(self.secrets_file, 'wb') as f:
            f.write(encrypted)

    def set(self, key: str, value: Any):
        """Set secret value"""
        self.secrets[key] = value
        self._save_secrets()

    def get(self, key: str, default: Any = None) -> Any:
        """Get secret value"""
        return self.secrets.get(key, default)

    def delete(self, key: str):
        """Delete secret"""
        if key in self.secrets:
            del self.secrets[key]
            self._save_secrets()

    def list_keys(self) -> list:
        """List all secret keys"""
        return list(self.secrets.keys())

# Usage
secrets = SecretsManager()

# Store secrets
secrets.set('database_url', 'postgresql://user:pass@localhost/db')
secrets.set('api_key', 'sk_live_abc123xyz789')
secrets.set('aws_access_key', 'AKIAIOSFODNN7EXAMPLE')
secrets.set('aws_secret_key', 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY')

# Retrieve secrets
db_url = secrets.get('database_url')
api_key = secrets.get('api_key')

print("Secrets stored and encrypted!")

# Best practice: Use in application
class Config:
    """Application configuration with secrets"""

    def __init__(self):
        self.secrets = SecretsManager()

    @property
    def DATABASE_URL(self) -> str:
        return self.secrets.get('database_url')

    @property
    def API_KEY(self) -> str:
        return self.secrets.get('api_key')

    @property
    def SECRET_KEY(self) -> str:
        return self.secrets.get('secret_key', os.urandom(32).hex())
```

### 6.1 Environment Variables (Best Practice)

```python
import os
from dotenv import load_dotenv
from pathlib import Path

class EnvironmentConfig:
    """Load configuration from environment variables"""

    def __init__(self, env_file: str = '.env'):
        # Load .env file
        env_path = Path(env_file)
        if env_path.exists():
            load_dotenv(env_path)

        self.environment = os.getenv('ENVIRONMENT', 'development')

    # Database
    @property
    def DATABASE_URL(self) -> str:
        url = os.getenv('DATABASE_URL')
        if not url:
            raise ValueError("DATABASE_URL environment variable not set")
        return url

    # API Keys
    @property
    def OPENAI_API_KEY(self) -> str:
        key = os.getenv('OPENAI_API_KEY')
        if not key:
            raise ValueError("OPENAI_API_KEY not set")
        return key

    # AWS Credentials
    @property
    def AWS_ACCESS_KEY_ID(self) -> str:
        return os.getenv('AWS_ACCESS_KEY_ID', '')

    @property
    def AWS_SECRET_ACCESS_KEY(self) -> str:
        return os.getenv('AWS_SECRET_ACCESS_KEY', '')

    # Application
    @property
    def SECRET_KEY(self) -> str:
        key = os.getenv('SECRET_KEY')
        if not key:
            if self.environment == 'production':
                raise ValueError("SECRET_KEY must be set in production")
            # Generate random key for development
            return os.urandom(32).hex()
        return key

    @property
    def DEBUG(self) -> bool:
        return os.getenv('DEBUG', 'False').lower() == 'true'

    def validate(self):
        """Validate all required config is present"""
        required = [
            'DATABASE_URL',
            'SECRET_KEY',
        ]

        missing = []
        for var in required:
            if not os.getenv(var):
                missing.append(var)

        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")

# .env file example (NEVER commit to git!)
"""
# .env
ENVIRONMENT=production
DEBUG=False

DATABASE_URL=postgresql://user:password@localhost:5432/mydb
SECRET_KEY=super-secret-key-change-this

OPENAI_API_KEY=sk-...
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=...

EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
"""

# .gitignore (ALWAYS ignore secrets!)
"""
# .gitignore
.env
.env.*
.secrets.encrypted
*.key
secrets/
credentials/
"""
```

---

## 7. JWT (JSON Web Tokens) Security

```python
import jwt
from datetime import datetime, timedelta
from typing import Dict, Optional
import secrets

class JWTManager:
    """Secure JWT token management"""

    def __init__(self, secret_key: str = None, algorithm: str = 'HS256'):
        self.secret_key = secret_key or secrets.token_hex(32)
        self.algorithm = algorithm
        self.access_token_lifetime = timedelta(minutes=15)
        self.refresh_token_lifetime = timedelta(days=30)

    def create_access_token(self, user_id: int, additional_claims: Dict = None) -> str:
        """Create short-lived access token"""
        payload = {
            'user_id': user_id,
            'type': 'access',
            'exp': datetime.utcnow() + self.access_token_lifetime,
            'iat': datetime.utcnow(),
            'jti': secrets.token_hex(16),  # Unique token ID
        }

        if additional_claims:
            payload.update(additional_claims)

        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def create_refresh_token(self, user_id: int) -> str:
        """Create long-lived refresh token"""
        payload = {
            'user_id': user_id,
            'type': 'refresh',
            'exp': datetime.utcnow() + self.refresh_token_lifetime,
            'iat': datetime.utcnow(),
            'jti': secrets.token_hex(16),
        }

        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def verify_token(self, token: str, expected_type: str = 'access') -> Optional[Dict]:
        """Verify and decode token"""
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm]
            )

            # Verify token type
            if payload.get('type') != expected_type:
                return None

            return payload

        except jwt.ExpiredSignatureError:
            print("Token has expired")
            return None
        except jwt.InvalidTokenError as e:
            print(f"Invalid token: {e}")
            return None

    def refresh_access_token(self, refresh_token: str) -> Optional[str]:
        """Generate new access token from refresh token"""
        payload = self.verify_token(refresh_token, expected_type='refresh')

        if not payload:
            return None

        # Create new access token
        return self.create_access_token(payload['user_id'])

# Flask integration
from flask import Flask, request, jsonify
from functools import wraps

app = Flask(__name__)
jwt_manager = JWTManager()

def token_required(f):
    """Decorator to require valid JWT token"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Get token from Authorization header
        auth_header = request.headers.get('Authorization')
        if auth_header:
            try:
                token = auth_header.split(' ')[1]  # "Bearer <token>"
            except IndexError:
                return jsonify({'error': 'Invalid token format'}), 401

        if not token:
            return jsonify({'error': 'Token is missing'}), 401

        # Verify token
        payload = jwt_manager.verify_token(token)
        if not payload:
            return jsonify({'error': 'Invalid or expired token'}), 401

        # Pass user_id to route
        return f(user_id=payload['user_id'], *args, **kwargs)

    return decorated

@app.route('/login', methods=['POST'])
def login():
    """Login and get tokens"""
    username = request.json.get('username')
    password = request.json.get('password')

    # Verify credentials (implement this)
    user_id = verify_credentials(username, password)
    if not user_id:
        return jsonify({'error': 'Invalid credentials'}), 401

    # Generate tokens
    access_token = jwt_manager.create_access_token(
        user_id,
        additional_claims={'username': username, 'role': 'user'}
    )
    refresh_token = jwt_manager.create_refresh_token(user_id)

    return jsonify({
        'access_token': access_token,
        'refresh_token': refresh_token,
        'token_type': 'Bearer',
        'expires_in': 900  # 15 minutes
    })

@app.route('/refresh', methods=['POST'])
def refresh():
    """Refresh access token"""
    refresh_token = request.json.get('refresh_token')

    new_access_token = jwt_manager.refresh_access_token(refresh_token)
    if not new_access_token:
        return jsonify({'error': 'Invalid refresh token'}), 401

    return jsonify({
        'access_token': new_access_token,
        'token_type': 'Bearer'
    })

@app.route('/protected', methods=['GET'])
@token_required
def protected_route(user_id):
    """Protected route requiring valid token"""
    return jsonify({
        'message': f'Hello user {user_id}!',
        'data': 'This is protected data'
    })
```

---

## 8. Security Testing

```python
import requests
from typing import List, Dict
import time

class SecurityTester:
    """Automated security testing"""

    def __init__(self, base_url: str):
        self.base_url = base_url
        self.vulnerabilities = []

    def test_sql_injection(self, endpoint: str, params: Dict[str, str]):
        """Test for SQL injection vulnerabilities"""
        print(f"\n[*] Testing SQL injection on {endpoint}")

        sql_payloads = [
            "' OR '1'='1",
            "admin'--",
            "' OR '1'='1' --",
            "1' UNION SELECT NULL--",
            "'; DROP TABLE users--"
        ]

        for payload in sql_payloads:
            for param_name in params.keys():
                test_params = params.copy()
                test_params[param_name] = payload

                try:
                    response = requests.get(
                        f"{self.base_url}{endpoint}",
                        params=test_params
                    )

                    # Check for SQL errors in response
                    sql_errors = [
                        'SQL syntax',
                        'mysql_fetch',
                        'ORA-',
                        'PostgreSQL',
                        'SQLite'
                    ]

                    for error in sql_errors:
                        if error.lower() in response.text.lower():
                            self.vulnerabilities.append({
                                'type': 'SQL Injection',
                                'endpoint': endpoint,
                                'parameter': param_name,
                                'payload': payload,
                                'severity': 'CRITICAL'
                            })
                            print(f"  [!] Potential SQL injection: {param_name}={payload}")

                except Exception as e:
                    print(f"  [x] Error testing {param_name}: {e}")

    def test_xss(self, endpoint: str, params: Dict[str, str]):
        """Test for XSS vulnerabilities"""
        print(f"\n[*] Testing XSS on {endpoint}")

        xss_payloads = [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert('XSS')>",
            "javascript:alert('XSS')",
            "<svg/onload=alert('XSS')>"
        ]

        for payload in xss_payloads:
            for param_name in params.keys():
                test_params = params.copy()
                test_params[param_name] = payload

                try:
                    response = requests.get(
                        f"{self.base_url}{endpoint}",
                        params=test_params
                    )

                    # Check if payload appears unescaped in response
                    if payload in response.text:
                        self.vulnerabilities.append({
                            'type': 'XSS',
                            'endpoint': endpoint,
                            'parameter': param_name,
                            'payload': payload,
                            'severity': 'HIGH'
                        })
                        print(f"  [!] Potential XSS: {param_name}={payload}")

                except Exception as e:
                    print(f"  [x] Error testing {param_name}: {e}")

    def test_csrf(self, endpoint: str, method: str = 'POST'):
        """Test for CSRF protection"""
        print(f"\n[*] Testing CSRF protection on {endpoint}")

        try:
            if method == 'POST':
                # Try POST without CSRF token
                response = requests.post(
                    f"{self.base_url}{endpoint}",
                    data={'test': 'data'}
                )

                if response.status_code == 200:
                    self.vulnerabilities.append({
                        'type': 'CSRF',
                        'endpoint': endpoint,
                        'severity': 'HIGH',
                        'description': 'No CSRF protection detected'
                    })
                    print(f"  [!] No CSRF protection on {endpoint}")

        except Exception as e:
            print(f"  [x] Error testing CSRF: {e}")

    def test_authentication(self, login_endpoint: str):
        """Test authentication security"""
        print(f"\n[*] Testing authentication on {login_endpoint}")

        # Test for username enumeration
        response1 = requests.post(
            f"{self.base_url}{login_endpoint}",
            data={'username': 'existing_user', 'password': 'wrong_password'}
        )

        response2 = requests.post(
            f"{self.base_url}{login_endpoint}",
            data={'username': 'nonexistent_user', 'password': 'wrong_password'}
        )

        if response1.text != response2.text:
            self.vulnerabilities.append({
                'type': 'Username Enumeration',
                'endpoint': login_endpoint,
                'severity': 'MEDIUM',
                'description': 'Different error messages for valid/invalid users'
            })
            print(f"  [!] Username enumeration possible")

        # Test for brute force protection
        print("  [*] Testing brute force protection...")
        start_time = time.time()
        attempts = 0

        for i in range(20):
            response = requests.post(
                f"{self.base_url}{login_endpoint}",
                data={'username': 'test', 'password': f'wrong{i}'}
            )
            attempts += 1

            if response.status_code == 429:  # Too Many Requests
                print(f"  [+] Rate limiting detected after {attempts} attempts")
                break
        else:
            self.vulnerabilities.append({
                'type': 'No Brute Force Protection',
                'endpoint': login_endpoint,
                'severity': 'HIGH',
                'description': f'No rate limiting after {attempts} failed attempts'
            })
            print(f"  [!] No brute force protection detected")

    def test_headers(self):
        """Test security headers"""
        print(f"\n[*] Testing security headers")

        response = requests.get(self.base_url)
        headers = response.headers

        required_headers = {
            'X-Frame-Options': 'DENY or SAMEORIGIN',
            'X-Content-Type-Options': 'nosniff',
            'X-XSS-Protection': '1; mode=block',
            'Strict-Transport-Security': 'max-age=31536000',
            'Content-Security-Policy': 'Restrictive CSP'
        }

        for header, expected in required_headers.items():
            if header not in headers:
                self.vulnerabilities.append({
                    'type': 'Missing Security Header',
                    'header': header,
                    'expected': expected,
                    'severity': 'MEDIUM'
                })
                print(f"  [!] Missing header: {header}")

    def generate_report(self) -> Dict:
        """Generate security test report"""
        report = {
            'total_vulnerabilities': len(self.vulnerabilities),
            'by_severity': {
                'CRITICAL': [],
                'HIGH': [],
                'MEDIUM': [],
                'LOW': []
            }
        }

        for vuln in self.vulnerabilities:
            severity = vuln.get('severity', 'LOW')
            report['by_severity'][severity].append(vuln)

        return report

# Usage
tester = SecurityTester('http://localhost:5000')

# Run tests
tester.test_sql_injection('/search', {'q': 'test'})
tester.test_xss('/comment', {'text': 'test'})
tester.test_csrf('/transfer')
tester.test_authentication('/login')
tester.test_headers()

# Generate report
report = tester.generate_report()
print(f"\n\n=== Security Test Report ===")
print(f"Total vulnerabilities: {report['total_vulnerabilities']}")
for severity, vulns in report['by_severity'].items():
    if vulns:
        print(f"\n{severity}: {len(vulns)}")
        for vuln in vulns:
            print(f"  - {vuln}")
```

---

## 9. Production Security Checklist

### 9.1 Comprehensive Security Configuration

```python
from flask import Flask
from flask_talisman import Talisman
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import logging
from logging.handlers import RotatingFileHandler

def create_secure_app():
    """Create Flask app with all security measures"""

    app = Flask(__name__)

    # 1. Secret Key (from environment)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    # 2. Session Security
    app.config.update(
        SESSION_COOKIE_SECURE=True,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE='Lax',
        PERMANENT_SESSION_LIFETIME=1800,  # 30 minutes
    )

    # 3. HTTPS/Security Headers (Talisman)
    csp = {
        'default-src': "'self'",
        'script-src': "'self' 'unsafe-inline'",
        'style-src': "'self' 'unsafe-inline'",
        'img-src': "'self' data: https:",
    }

    Talisman(
        app,
        force_https=True,
        strict_transport_security=True,
        content_security_policy=csp,
        content_security_policy_nonce_in=['script-src']
    )

    # 4. Rate Limiting
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=["200 per day", "50 per hour"],
        storage_uri="redis://localhost:6379"
    )

    # 5. Logging
    if not app.debug:
        file_handler = RotatingFileHandler(
            'logs/security.log',
            maxBytes=10240000,
            backupCount=10
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Application startup')

    # 6. CORS (if needed)
    from flask_cors import CORS
    CORS(app, resources={
        r"/api/*": {
            "origins": ["https://yourdomain.com"],
            "methods": ["GET", "POST"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })

    return app, limiter

app, limiter = create_secure_app()

# Apply rate limiting to specific routes
@app.route('/api/login', methods=['POST'])
@limiter.limit("5 per minute")
def login():
    # Login logic
    pass

@app.route('/api/data', methods=['GET'])
@limiter.limit("100 per hour")
def get_data():
    # Data retrieval
    pass
```

---

## Summary: Security Best Practices

### ✅ Always Do

1. **Use parameterized queries** - Prevent SQL injection
2. **Hash passwords** with bcrypt/Argon2 - Never store plaintext
3. **Validate all input** - Never trust user input
4. **Escape output** - Prevent XSS
5. **Use HTTPS everywhere** - Encrypt all traffic
6. **Implement CSRF protection** - Prevent unauthorized actions
7. **Use secure session management** - HTTPOnly, Secure, SameSite cookies
8. **Rate limit** - Prevent brute force and DoS
9. **Keep dependencies updated** - Patch vulnerabilities
10. **Use environment variables for secrets** - Never hardcode credentials
11. **Implement proper logging** - Monitor for attacks
12. **Use Content Security Policy** - Prevent injection attacks

### ❌ Never Do

1. **Never store passwords in plaintext**
2. **Never use MD5/SHA for passwords** - Too fast, vulnerable to rainbow tables
3. **Never trust client-side validation** - Always validate server-side
4. **Never expose stack traces** in production
5. **Never commit secrets to Git**
6. **Never use outdated crypto** (DES, RC4, etc.)
7. **Never disable security features** in production
8. **Never use `eval()` on user input**
9. **Never rely on security through obscurity**
10. **Never skip security updates**

---

## Production Deployment Security

```dockerfile
# Dockerfile with security best practices
FROM python:3.11-slim

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Change ownership
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s \
  CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Run application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "app:app"]
```

This comprehensive security guide covers all essential aspects of Python security for professional development. Practice these patterns in every project!
