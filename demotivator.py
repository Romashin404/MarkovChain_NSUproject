# demotivator.py
from PIL import Image, ImageDraw, ImageFont
import os

class DemotivatorMaker:
    def __init__(self, border=10, bottom_height=120):
        self.border = border
        self.bottom_height = bottom_height
        self.font_path = "/System/Library/Fonts/Helvetica.ttc"

    def _wrap_text(self, draw, text, font, max_width):
        words = text.split()
        lines = []
        current_line = ""
        
        for word in words:
            test_line = f"{current_line} {word}".strip()
            bbox = draw.textbbox((0, 0), test_line, font=font)
            if bbox[2] <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        return lines

    def make(self, img_path, text, output_path, max_width=300, max_font_size=50):
        img = Image.open(img_path).convert("RGB")
        if img.width > max_width:
            ratio = max_width / img.width
            new_height = int(img.height * ratio)
            img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
        
        w, h = img.size
        canvas_w = w + self.border * 2
        canvas_h = h + self.bottom_height + self.border * 2

        title = text.split('.')[0].strip().upper()

        draw_temp = ImageDraw.Draw(Image.new("RGB", (1, 1)))
        font_size = max_font_size
        
        while font_size >= 20:
            try:
                font = ImageFont.truetype(self.font_path, font_size)
            except:
                font = ImageFont.load_default()
            
            lines = self._wrap_text(draw_temp, title, font, w - 20)
            
            bbox = draw_temp.textbbox((0, 0), "A", font=font)
            line_height = bbox[3] - bbox[1]
            line_spacing = 10  
            total_height = line_height * len(lines) + line_spacing * (len(lines) - 1)
            
            if total_height <= self.bottom_height - 20:
                break
            font_size -= 2
        
        try:
            font = ImageFont.truetype(self.font_path, font_size)
        except:
            font = ImageFont.load_default()

        canvas = Image.new("RGB", (canvas_w, canvas_h), "black")
        canvas.paste(img, (self.border, self.border))
        draw = ImageDraw.Draw(canvas)
        
        draw.rectangle(
            [self.border-2, self.border-2, w+self.border+2, h+self.border+2],
            outline="white", width=2
        )

        line_height = draw.textbbox((0, 0), "A", font=font)[3]
        line_spacing = 10
        total_text_height = line_height * len(lines) + line_spacing * (len(lines) - 1)
        y_start = h + self.border + (self.bottom_height - total_text_height) // 2
        
        for i, line in enumerate(lines):
            bbox = draw.textbbox((0, 0), line, font=font)
            line_w = bbox[2] - bbox[0]
            y_pos = y_start + i * (line_height + line_spacing) 
            draw.text(((canvas_w - line_w) / 2, y_pos), line, fill="white", font=font)

        os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
        canvas.save(output_path, "JPEG", quality=95)
        print(f"Демотиватор сохранён: {output_path}")