from transformers import pipeline
from cryptography.fernet import Fernet
import numpy as np
import json

# emotion classifier
emotion_model = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base",
    top_k=None
)

# encryption setup
key = Fernet.generate_key()
cipher = Fernet(key)


def get_user_text():
    return input("Enter message: ")


def detect_emotion_embedding(text):

    results = emotion_model(text)[0]

    labels = []
    scores = []

    for r in results:
        labels.append(r["label"])
        scores.append(r["score"])

    embedding = np.array(scores)

    return labels, embedding


def encrypt_text(text):
    return cipher.encrypt(text.encode()).decode()


def encrypt_payload(payload):
    return cipher.encrypt(payload.encode()).decode()


def decrypt_payload(payload):
    return cipher.decrypt(payload.encode()).decode()


def main():

    text = get_user_text()

    labels, embedding = detect_emotion_embedding(text)

    encrypted_text = encrypt_text(text)

    message = {
        "ciphertext": encrypted_text,
        "emotion_embedding": embedding.tolist(),
        "labels": labels
    }

    payload = json.dumps(message)

    final_encrypted = encrypt_payload(payload)

    print("\nEncrypted Output:")
    print(final_encrypted)

    # Demonstrate decryption
    decrypted_payload = decrypt_payload(final_encrypted)
    data = json.loads(decrypted_payload)

    original_text = cipher.decrypt(data["ciphertext"].encode()).decode()

    print("\nDecrypted Output:")
    print("Original Message:", original_text)
    print("Emotion Labels:", data["labels"])
    print("Emotion Embedding:", data["emotion_embedding"])


if __name__ == "__main__":
    main()