from transformers import pipeline, logging
from cryptography.fernet import Fernet
import numpy as np
import json

# Silence transformer logs
logging.set_verbosity_error()

print("\nLoading Emotion Model...\n")

# Emotion detection model
emotion_model = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base",
    top_k=None
)

# ----------------------------
# Split Key Encryption
# ----------------------------

text_key = Fernet.generate_key()
payload_key = Fernet.generate_key()

text_cipher = Fernet(text_key)
payload_cipher = Fernet(payload_key)

# ----------------------------
# Emotion Embedding Generator
# ----------------------------

def generate_emotion_embedding(text, threshold=0.5):

    results = emotion_model(text)[0]

    labels = []
    scores = []

    for r in results:
        if r["score"] >= threshold:
            labels.append(r["label"])
            scores.append(r["score"])

    # fallback if nothing passes threshold
    if not labels:
        best = max(results, key=lambda x: x["score"])
        labels.append(best["label"])
        scores.append(best["score"])

    embedding = np.array(scores)

    return labels, embedding.tolist()


# ----------------------------
# Encryption Functions
# ----------------------------

def encrypt_text(text):
    return text_cipher.encrypt(text.encode()).decode()


def decrypt_text(ciphertext):
    return text_cipher.decrypt(ciphertext.encode()).decode()


def encrypt_payload(data):
    return payload_cipher.encrypt(data.encode()).decode()


def decrypt_payload(data):
    return payload_cipher.decrypt(data.encode()).decode()


# ----------------------------
# Encrypt Workflow
# ----------------------------

def encrypt_message():

    text = input("\nEnter message to encrypt:\n> ")

    labels, embedding = generate_emotion_embedding(text)

    encrypted_text = encrypt_text(text)

    payload = {
        "ciphertext": encrypted_text,
        "emotion_embedding": embedding,
        "labels": labels
    }

    payload_string = json.dumps(payload)

    final_payload = encrypt_payload(payload_string)

    print("\nEncrypted Payload:")
    print(final_payload)

    print("\nDetected Emotion:")
    print(labels)


# ----------------------------
# Decrypt Workflow
# ----------------------------

def decrypt_message():

    payload = input("\nEnter encrypted payload:\n> ")

    decrypted_payload = decrypt_payload(payload)

    data = json.loads(decrypted_payload)

    original_text = decrypt_text(data["ciphertext"])

    print("\nOriginal Message:")
    print(original_text)

    print("\nEmotion:")
    print(data["labels"])

    print("\nEmotion Embedding:")
    print(data["emotion_embedding"])


# ----------------------------
# CLI Menu
# ----------------------------

def main():

    while True:

        print("\nEmotion Cipher CLI")
        print("------------------")
        print("1. Encrypt Message")
        print("2. Decrypt Message")
        print("3. Exit")

        choice = input("\nSelect option: ")

        if choice == "1":
            encrypt_message()

        elif choice == "2":
            decrypt_message()

        elif choice == "3":
            print("\nExiting...")
            break

        else:
            print("\nInvalid option")


if __name__ == "__main__":
    main()