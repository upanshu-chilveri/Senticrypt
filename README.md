
# Senticrypt
Emotion-Aware Dual-Key Encryption System

Senticrypt is a hackathon project that introduces a new approach to secure communication by combining Natural Language Processing (NLP) and cryptography.

Instead of treating messages as plain text before encryption, Senticrypt first analyzes the emotional context of the sentence, converts that emotion into vector embeddings, and then integrates the emotional representation into a dual-key encryption mechanism.

The result is an emotion-aware encryption pipeline that not only protects the content of a message but also encodes its emotional signature in a secure, structured form.

The system uses a RoBERTa-based emotion classifier, vector embeddings derived from emotional states, and a dual key encryption architecture to securely transform messages while preserving contextual meaning.

### Access at - https://senticrypt-deploymenet-q76y7kb9h-upanshu-chilveris-projects.vercel.app

---

## Problem Statement

Traditional encryption systems treat messages as pure data, ignoring contextual meaning such as tone, sentiment, or emotion.

However, in many communication systems:

Emotional context influences interpretation

Messages may require semantic awareness

Security systems rarely integrate AI-based language understanding

Senticrypt addresses this gap by introducing a semantic preprocessing layer before encryption.

---

# Core Idea

Senticrypt performs the following steps:

* A user inputs a message.

* The message is analyzed using RoBERTa emotion classification.

* The detected emotion is converted into a vector embedding.

* The emotional vector contributes to the encryption pipeline.

* The encrypted output is generated using dual-key encryption.

* The emotion is visualized using emoji representation.

* This creates a pipeline where emotion becomes part of the encrypted representation of the message.

<img height="640" alt="ChatGPT Image Mar 7, 2026, 03_53_26 PM" src="https://github.com/user-attachments/assets/5a6e7230-860c-4656-b60d-a885c4250a42" />


# Demo Video is in Project Repo

## Installation

#### CLI Implementation

The CLI is named "Senticrypt_cli.py"

Run the Python file and a CLI version of the app can be used.



#### Local download
Clone the repository

```bash
git clone https://github.com/upanshu-chilveri/Senticrypt.git
```

Move into the directory

```bash
cd Senticrypt
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the backend server

```bash
python manage.py runserver
```

---
# Encryption Pipeline

The encryption pipeline integrates semantic analysis with cryptographic transformation.

* Step 1
User enters text.

* Step 2
RoBERTa processes the text and predicts the emotional class.

* Step 3
Emotion is converted into an embedding vector.

* Step 4
A secondary encryption key is derived from the vector.

* Step 5
Message encryption occurs using:

Primary Key
+
Emotion-Derived Secondary Key

* Step 6
Encrypted output is generated.
