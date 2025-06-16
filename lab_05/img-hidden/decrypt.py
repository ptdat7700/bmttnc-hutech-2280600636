import sys
from PIL import Image

def decode_image(encoded_image_path):
    img = Image.open(encoded_image_path)
    width, height = img.size
    binary_message = ""

    for row in range(height):
        for col in range(width):
            pixel = img.getpixel((col, row))
            for color_channel in range(3):
                # Lấy bit cuối cùng của mỗi màu (LSB)
                binary_message += format(pixel[color_channel], '08b')[-1]
                
                # Kiểm tra dấu hiệu kết thúc thông điệp '1111111111111110'
                if binary_message[-16:] == '1111111111111110':
                    binary_message = binary_message[:-16]  # Xóa dấu hiệu kết thúc
                    message = ""
                    for i in range(0, len(binary_message), 8):
                        byte = binary_message[i:i+8]
                        message += chr(int(byte, 2))
                    return message
    return ""  # Nếu không tìm thấy dấu hiệu kết thúc

def main():
    if len(sys.argv) != 2:
        print("Usage: python decrypt.py <encoded_image_path>")
        return
    encoded_image_path = sys.argv[1]
    decoded_message = decode_image(encoded_image_path)
    print("Decoded message:", decoded_message)

if __name__ == "__main__":
    main()
