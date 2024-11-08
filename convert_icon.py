from PIL import Image
import os

def create_simple_icon():
    # Create a simple colored square as icon
    img = Image.new('RGB', (64, 64), color='#2c3e50')
    
    # Save as ICO
    img.save("assets/icon.ico", format="ICO")
    print("Simple icon created successfully!")

if __name__ == "__main__":
    create_simple_icon()
