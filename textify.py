from PIL import Image
from tkinter import Tk, filedialog
import sys

# Function to display custom ASCII art
def print_ascii_art():
    ascii_art = """
    888                      888    d8b  .d888          
    888                      888    Y8P d88P"           
    888                      888        888             
    888888  .d88b.  888  888 888888 888 888888 888  888 
    888    d8P  Y8b `Y8bd8P' 888    888 888    888  888 
    888    88888888   X88K   888    888 888    888  888 
    Y88b.  Y8b.     .d8""8b. Y88b.  888 888    Y88b 888 
     "Y888  "Y8888  888  888  "Y888 888 888     "Y88888 
                                                888 
                                           Y8b d88P 
                                            "Y88P" 

    https://github.com/nginx0                                        
                                             
    """
    print(ascii_art)

# Function to choose an ASCII character set
def choose_ascii_set():
    sets = {
        "1": "@%#*+=-:. ",
        "2": "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. ",
        "3": ".:-=+*#%@",
    }
    while True:
        print("\nChoose an ASCII character set:")
        for key, value in sets.items():
            print(f"{key}: {value}")
        choice = input("Enter the number of your choice: ")
        if choice in sets:
            return sets[choice]
        else:
            print("Invalid choice. Please choose a valid option.")

# Function to choose image size
def choose_size_option():
    size_options = {
        "1": "Small",
        "2": "Medium",
        "3": "Large",
        "4": "Original Size"
    }
    while True:
        print("\nChoose the size of the ASCII art:")
        for key, value in size_options.items():
            print(f"{key}: {value}")
        choice = input("Enter the number of your choice: ")
        if choice in size_options:
            return size_options[choice]
        else:
            print("Invalid choice. Please choose a valid option.")

def resize_image(image, size_option="medium", maintain_aspect_ratio=True):
    width, height = image.size
    size_map = {
        "Small": 50,
        "Medium": 100,
        "Large": 200,
        "Original Size": width
    }
    new_width = size_map.get(size_option, 100)
    aspect_ratio = height / width if maintain_aspect_ratio else 1
    new_height = int(aspect_ratio * new_width * 0.55)
    resized_image = image.resize((new_width, new_height))
    return resized_image

def grayscale_image(image):
    return image.convert("L")

def map_pixels_to_ascii(image):
    pixels = image.getdata()
    ascii_str = ""
    for i, pixel in enumerate(pixels):
        if i % (len(pixels) // 100) == 0:  # Update progress every 1%
            sys.stdout.write(f"\rProcessing: {i * 100 // len(pixels)}%")
            sys.stdout.flush()
        ascii_str += ASCII_CHARS[min(pixel // (256 // len(ASCII_CHARS)), len(ASCII_CHARS) - 1)]
    sys.stdout.write("\rProcessing: 100%\n")
    return ascii_str

def convert_image_to_ascii(image, size_option="Medium", maintain_aspect_ratio=True):
    image = resize_image(image, size_option, maintain_aspect_ratio)
    image = grayscale_image(image)

    ascii_str = map_pixels_to_ascii(image)
    img_width = image.width

    ascii_art = "\n".join([ascii_str[i:i + img_width] for i in range(0, len(ascii_str), img_width)])
    return ascii_art

def save_ascii_to_file(ascii_art):
    save_path = input("\nEnter the file name to save the ASCII art (leave blank to skip): ")
    if save_path:
        with open(save_path, 'w') as f:
            f.write(ascii_art)
        print(f"ASCII art saved to {save_path}")

def display_ascii_in_console(ascii_art):
    print("\nASCII Art Preview:")
    print(ascii_art)

def main():
    # Print the custom ASCII art at the very beginning
    print_ascii_art()
    
    # Choose ASCII character set
    global ASCII_CHARS
    ASCII_CHARS = choose_ascii_set()
    
    # Hide the root Tk window
    Tk().withdraw()

    # Open file dialog with correct filters
    image_path = filedialog.askopenfilename(
        title="Select an Image File", 
        filetypes=[
            ("JPEG files", "*.jpg *.jpeg"),
            ("PNG files", "*.png"),
            ("All files", "*.*")
        ]
    )

    if not image_path:
        print("No file selected. Exiting...")
        return

    try:
        image = Image.open(image_path)
    except FileNotFoundError:
        print("File not found. Please try again.")
        return
    except OSError as e:
        print(f"Cannot open image. Unsupported file format or file is corrupted. Error: {e}")
        return

    # Choose image size
    size_option = choose_size_option()

    # Ask if the user wants to maintain the aspect ratio
    maintain_aspect_ratio = input("\nMaintain aspect ratio? (y/n): ").strip().lower() == "y"

    # Convert the image to ASCII
    ascii_art = convert_image_to_ascii(image, size_option, maintain_aspect_ratio)
    
    # Display the ASCII art
    display_ascii_in_console(ascii_art)
    
    # Optionally save the ASCII art to a file
    save_ascii_to_file(ascii_art)

if __name__ == "__main__":
    main()
