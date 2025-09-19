from PIL import Image

def custom_encrypt(message, key):
    encrypted = ''
    for i, char in enumerate(message):
        encrypted += chr((ord(char) + key + i) % 256)
    return encrypted

def custom_decrypt(encrypted, key):
    decrypted = ''
    for i, char in enumerate(encrypted):
        decrypted += chr((ord(char) - key - i) % 256)
    return decrypted

def hide_message(img_path, message, out_path, key):
    message = custom_encrypt(message, key) + chr(0)
    binary_msg = ''.join([format(ord(c), '08b') for c in message])
    img = Image.open(img_path)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    pixels = list(img.getdata())
    if len(binary_msg) > len(pixels) * 3:
        raise ValueError("Image is too small to hold the message.")
    new_pixels = []
    idx = 0
    for pixel in pixels:
        r, g, b = pixel
        if idx < len(binary_msg): r = (r & ~1) | int(binary_msg[idx]); idx += 1
        if idx < len(binary_msg): g = (g & ~1) | int(binary_msg[idx]); idx += 1
        if idx < len(binary_msg): b = (b & ~1) | int(binary_msg[idx]); idx += 1
        new_pixels.append((r, g, b))
    img.putdata(new_pixels)
    img.save(out_path)
    print(f"✅ Message hidden in '{out_path}'.")

def extract_message(img_path, key):
    img = Image.open(img_path)
    pixels = list(img.getdata())
    binary_msg = ""
    for pixel in pixels:
        for color in pixel:
            binary_msg += str(color & 1)
    chars = [binary_msg[i:i+8] for i in range(0, len(binary_msg), 8)]
    message = ""
    for char in chars:
        decoded = chr(int(char, 2))
        if decoded == chr(0): break
        message += decoded
    return custom_decrypt(message, key)

if __name__ == "__main__":
    print("\n🔐 StegoCrypt CLI Tool\n")
    print("1. Hide a message")
    print("2. Extract a message")
    choice = input("Enter your choice (1 or 2): ")
    if choice == '1':
        img_path = input("Enter input image path: ")
        out_path = input("Enter output image path: ")
        message = input("Enter the message to hide: ")
        key = int(input("Enter encryption key (number): "))
        hide_message(img_path, message, out_path, key)
    elif choice == '2':
        img_path = input("Enter stego image path: ")
        key = int(input("Enter decryption key (number): "))
        msg = extract_message(img_path, key)
        print("\n🕵️ Decoded message:", msg)
    else:
        print("Invalid choice.")
