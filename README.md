# Image Editor

A desktop photo editor built with Python, customtkinter, and Pillow. Supports common image adjustments, filters, cropping, and more — all in a clean, modern UI.

---

## Features

- **Adjustments** — Brightness, Contrast, Exposure, Saturation, and Highlights via intuitive sliders
- **Crop** — Interactive crop tool with draggable corner handles
- **Flip** — Horizontal flip
- **Rotate** — Rotate left or right in 90° increments
- **Filters** — One-click filter presets with live thumbnails
- **Undo** — Step back through your edits
- **Save** — Export as PNG, JPG, or BMP

---

## Screenshots



---

## Tech Stack

| Tool          | Purpose             |
| Python        | Core language       |
| customtkinter | Modern UI framework |
| Pillow (PIL)  | Image processing    |
| CTkMessagebox | Dialog boxes        |

---

## Installation

**1. Clone the repository**
```bash
git clone https://github.com/sushh12/Image-Editing-Application.git
cd Image-Editing-Application
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Run the app**
```bash
python gui.py
```

---

## Requirements

- Python 3.8+
- Dependencies listed in `requirements.txt`

---

## Project Structure

```
Image-Editing-Application/
├── gui.py            # Main app window and core logic
├── editPanel.py      # Adjustment sliders, crop, flip, rotate
├── filterPanel.py    # Filter presets with thumbnails
├── icons/            # UI icons
└── requirements.txt  # Python dependencies
```

---

