# Secure Encrypted Chat

## Overview

This project is a secure encrypted chat application that utilizes advanced cryptographic techniques to ensure confidentiality and authenticity. The system implements AES-CBC for message encryption, Kyber for key encapsulation, and DSA for digital signatures, providing a robust and secure communication framework.

## Features

- **AES-CBC Encryption**: Ensures secure message encryption using the AES (Advanced Encryption Standard) in Cipher Block Chaining (CBC) mode.
- **Kyber Key Encapsulation**: Uses post-quantum cryptography to securely exchange AES keys.
- **DSA Digital Signatures**: Ensures message integrity and authenticity by signing Kyber public keys and messages.
- **User Authentication**: Verifies the identity of each participant through cryptographic signatures.
- **End-to-End Encryption**: Messages remain encrypted throughout the communication process, ensuring privacy.

## How It Works

1. **Key Exchange**: Kyber is used for secure key encapsulation, ensuring that only intended recipients can access the encryption keys.
2. **Message Encryption**: AES-CBC encrypts the messages before transmission, protecting them from interception.
3. **Digital Signature**: DSA is used to sign Kyber public keys and messages, ensuring authenticity and preventing tampering.
4. **Decryption & Verification**: The recipient decrypts the message using AES and verifies the sender's identity using the DSA signature.

## Installation & Execution

### Prerequisites

Ensure you have Python installed along with the necessary dependencies:

```bash
pip install -r requirements.txt
```

### Running the Chat Application

To start the chat program, simply execute:

```bash
python main.py
```

## Technologies Used

- **Python**: Core programming language for implementation.
- **PyCryptodome**: Used for AES encryption.
- **Kyber**: Post-quantum key encapsulation mechanism.
- **DSA (Digital Signature Algorithm)**: Provides message authentication and integrity.

## Security Considerations

- **Post-Quantum Security**: Kyber ensures resistance against quantum computing attacks.
- **Tamper-Proof Communication**: DSA signatures prevent unauthorized message modifications.
- **Confidentiality**: AES-CBC guarantees that messages remain private and unreadable to unauthorized entities.


