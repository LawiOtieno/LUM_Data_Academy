
from PIL import Image
import os

def create_favicon():
    """Create favicon from logo image"""
    try:
        # Open the logo image
        logo_path = 'core/static/core/img/logo.jpg'
        if not os.path.exists(logo_path):
            print(f"Logo file not found at: {logo_path}")
            return False
            
        # Open and process the image
        img = Image.open(logo_path)
        
        # Convert to RGBA if not already
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # Create a circular mask
        size = min(img.size)
        img = img.resize((size, size), Image.Resampling.LANCZOS)
        
        # Create circular mask
        mask = Image.new('L', (size, size), 0)
        from PIL import ImageDraw
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, size, size), fill=255)
        
        # Apply the circular mask
        img.putalpha(mask)
        
        # Create multiple favicon sizes
        sizes = [16, 32, 48, 64, 128, 256]
        
        # Save as ICO file (contains multiple sizes)
        favicon_path = 'core/static/core/img/favicon.ico'
        img.save(favicon_path, format='ICO', sizes=[(s, s) for s in sizes])
        
        # Also save individual PNG sizes for web use
        for size in sizes:
            resized = img.resize((size, size), Image.Resampling.LANCZOS)
            png_path = f'core/static/core/img/favicon-{size}x{size}.png'
            resized.save(png_path, format='PNG')
        
        print("✅ Favicon generated successfully!")
        print(f"📁 ICO file: {favicon_path}")
        print(f"📁 PNG files: favicon-{sizes[0]}x{sizes[0]}.png to favicon-{sizes[-1]}x{sizes[-1]}.png")
        return True
        
    except Exception as e:
        print(f"❌ Error creating favicon: {e}")
        return False

if __name__ == "__main__":
    create_favicon()
