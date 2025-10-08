#!/usr/bin/env python3
"""
Simple script to create an application icon for Tech Trends Harvester
Creates a 256x256 PNG icon with a chart/trends design
Author: Rich Lewis
"""

try:
    from PIL import Image, ImageDraw, ImageFont
    import os
    
    # Create a 256x256 image with a gradient background
    size = 256
    img = Image.new('RGB', (size, size), color='#2c3e50')
    draw = ImageDraw.Draw(img)
    
    # Draw a simple trending line chart
    # Background circle
    draw.ellipse([20, 20, 236, 236], fill='#34495e', outline='#3498db', width=4)
    
    # Draw trending line (upward trend)
    points = [
        (60, 180),
        (90, 150),
        (120, 130),
        (150, 100),
        (180, 80),
        (210, 60)
    ]
    draw.line(points, fill='#2ecc71', width=6, joint='curve')
    
    # Draw data points
    for point in points:
        draw.ellipse([point[0]-6, point[1]-6, point[0]+6, point[1]+6], 
                     fill='#27ae60', outline='#2ecc71', width=2)
    
    # Draw "TTH" text
    try:
        # Try to use a system font
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 60)
    except:
        font = ImageFont.load_default()
    
    text = "TTH"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    text_x = (size - text_width) // 2
    text_y = (size - text_height) // 2 + 20
    
    draw.text((text_x, text_y), text, fill='#ecf0f1', font=font)
    
    # Save the icon
    icon_path = os.path.join(os.path.dirname(__file__), 'icon.png')
    img.save(icon_path)
    print(f"Icon created: {icon_path}")
    
    # Also save smaller versions
    for icon_size in [128, 64, 32, 16]:
        small = img.resize((icon_size, icon_size), Image.Resampling.LANCZOS)
        small_path = os.path.join(os.path.dirname(__file__), f'icon_{icon_size}.png')
        small.save(small_path)
        print(f"Icon created: {small_path}")
    
    print("\nTo use this icon in the app, add to mainwindow.py:")
    print("  icon_path = os.path.join(base_dir, 'assets', 'icon.png')")
    print("  self.setWindowIcon(QtGui.QIcon(icon_path))")
    
except ImportError:
    print("PIL (Pillow) not installed. Install with: pip install Pillow")
    print("Or create an icon manually and save as assets/icon.png")
