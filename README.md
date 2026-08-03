# Zetoken

Zetoken is a Python library for generating simple tokens.

---

## ⚠️ Security Warning & Usage Limitations

Zetoken is specifically designed to meet the needs of my project. This library was developed to handle WebSocket handshake processes across different programming languages. 

Its main purpose is to ensure that tokens can only be generated and decrypted by official applications within my project. Additionally, Zetoken is used to obfuscate identities, such as user IDs or other object IDs, when the data is transmitted through public spaces. 

Currently, Zetoken supports integration with Python, Node.js, and PHP.

However, to comply with the global cybersecurity standard "Don't roll your own crypto", I hereby declare that it is:

**NOT SUITABLE** for:
*   Storing highly sensitive data (banking infrastructure, credit cards, medical records)
*   Password hashing (primary passwords)
*   National-scale critical financial systems

**HIGHLY SUITABLE** for:
*   Quiz or online exam answer tokens
*   Ticket tokens or temporary access vouchers
*   Obfuscation (securely masking IDs or URL parameters)
*   Other non-financial application needs requiring mass token generation

---

## 🚀 Key Features

*   **Encryption**: Converts text data into unique numeric tokens
*   **Decryption**: Accurately restores numeric tokens back into the original text data
*   **Security**: Utilizes `keyId` (identifier / offset) and `secretKey` (primary key). Tokens can only be read by parties possessing the same keys.
*   **Time-Bound Tokens (TTL)**: Native support for auto-expiring tokens with built-in NTP Clock Skew tolerance (Leeway).

---

## ⚠️ Weaknesses & Limitations

Please note that Zetoken has several technical limitations:

*   Zetoken has not been audited by professional security experts. Therefore, to comply with global security standards, Zetoken is not yet suitable for financial, medical, or critical infrastructure scales.
*   The infancy of the algorithm potentially introduces zero-day security vulnerabilities. Therefore, for now, Zetoken should only be used for hashing non-risky or low-risk data.

---

## ⚠️ WARNING: ENV CONFIGURATION REQUIRED

This library **WILL NOT WORK** if you do not define the security keys.

Zetoken **does not have fallback keys** for security reasons. You **MUST** include the following configuration in your Environment system / `.env` file of your project:

```env
ZETOKEN_ACCESS_KEY_ID="your_unique_identity"
ZETOKEN_SECRET_KEY="your_secret_key"
ZETOKEN_ITERATIONS=1000


```

If the keys are not found in the ENV or function parameters, all encryption/decryption processes will fail and return a boolean value of `False`.

---

## 🛠️ Generator Tool

Use the following tool to generate our official cryptographic configuration components:

👉 **[OPEN ZETOKEN GENERATOR](https://anonputraid.github.io/zetoken.html)**

---

## 🧪 Stress Test Results (100,000 Iterations)

```text
==================================================
STARTING ULTIMATE STRESS TEST: 100,000 ITERATIONS (PURE PYTHON)
==================================================

Final Results:
- Total Execution Time : 281.71 seconds
- Average Encryption   : 1.43406 ms
- Average Decryption   : 1.37621 ms
- Worst Latency        : 165.5438 ms
- Total Failures       : 0
- Python Memory Delta  : 4.77 KB
==================================================


```

---

## ⚙️ System Requirements

Ensure your server or system meets the following modern standards:

* **Python >= 3.7**
* Third-party libraries: `cryptography`, `python-dotenv` (installed automatically)

---

## 📦 Installation

Use PIP (Python Package Installer). Dependencies will be downloaded automatically:

```bash
pip install zetoken


```

---

## 💻 Usage Instructions

### 1. Standard Usage (Automatically from ENV)

This method is the simplest as it automatically retrieves keys from the Environment system / `.env`.

```python
import os
from dotenv import load_dotenv
from zetoken import Zetoken

# Load environment variables from .env file
load_dotenv()

zetoken = Zetoken()

# Encode using KeyID, Secret, & Iterations from .env
token = zetoken.encode("Secret Message")

# Decode and perfectly restore to original text
original = zetoken.decode(token)


```

---

### 2. Sign & VerifySign Features (3-Layer Security / Manual KeyID)

Use this feature if you want to bind a token exclusively to an entity (e.g., User ID, Transaction Number). Even if the keys are compromised, `User A`'s token cannot be used by `User B`.

```python
import os
from dotenv import load_dotenv
from zetoken import Zetoken

# Load environment variables from .env file
load_dotenv()

zetoken = Zetoken()

user_id = "USER-9921"
data = "Exam Passed"

# SIGN: Locks the token using a combination of Master Access Key + userId + Master Secret Key
token = zetoken.sign(data, user_id)

# VERIFY: The token can only be opened and its integrity verified if the User ID is an exact match
result = zetoken.verify_sign(token, user_id)

if result is False:
    print("Fake token, manipulated, or incorrect KeyID!")


```

---

### 3. Time-Bound Tokens (TTL & Leeway)

You can generate tokens that automatically expire after a certain amount of time (Time-To-Live). Zetoken internally validates the expiration and provides a default `leeway` of 60 seconds to accommodate minor server clock desynchronization (NTP Clock Skew).

```python
import os
from dotenv import load_dotenv
from zetoken import Zetoken

load_dotenv()
zetoken = Zetoken()

# 1. ENCODE WITH EXPIRATION
# Add the `ttl` parameter (in seconds). E.g., 300 seconds = 5 minutes.
token = zetoken.encode("Self-destructing message", ttl=300)

# You can also use TTL with the Sign feature:
# token = zetoken.sign("Exam Passed", "USER-9921", ttl=300)


# 2. DECODE WITH AUTOMATIC TIME VALIDATION
# When decoding, Zetoken automatically checks the time. 
# It includes a default leeway of 60 seconds.
original = zetoken.decode(token)

if original is False:
    print("Token is either invalid, manipulated, or has expired!")
    
# Optional: You can customize the leeway time (in seconds)
# original = zetoken.decode(token, leeway=30)

```

---

## 📄 License

MIT License

Created by **Anonputraid**
