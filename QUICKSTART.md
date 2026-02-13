# Quick Start Guide

Get up and running with the IEC 62443 Attack Path Annotator in 5 minutes.

## Installation (One-Time Setup)

### 1. Install Python
If you don't have Python installed:
- Download from https://www.python.org/downloads/
- During installation, ✅ check "Add Python to PATH"

### 2. Install Dependencies
Open PowerShell or Command Prompt:
```bash
pip install Pillow
```

That's it! You're ready to go.

## Basic Usage

### Every Time You Use the Tool:

**Step 1: Copy Your Diagram**
- Open your network diagram (Visio, PowerPoint, PNG, etc.)
- Copy the image to clipboard (Ctrl+C)

**Step 2: Run the Tool**
```bash
python attack_path_annotator.py
```

**Step 3: Annotate**
- Right-click where attack starts → "Create Arrow"
- Drag to attack destination
- Select attack type (Zone Breach, Lateral Movement, etc.)
- Repeat for all attack paths

**Step 4: Save**
- Click "Finish & Save PDF"
- Choose location and filename
- Done!

## Common Workflows

### Single Attack Path
1. Copy diagram → Run tool
2. Right-click start → Create Arrow → Drag → Select type
3. Save PDF

### Multiple Paths
1. Copy diagram → Run tool
2. For each attack path:
   - Right-click start → Create Arrow → Drag → Select type
3. Save PDF with all paths

### Fixing Mistakes
- Right-click near arrow start → "Delete Arrow"
- Or right-click → "Clear All Arrows" to start over
- Then redraw

## Keyboard Shortcuts

- **Ctrl+C**: Copy diagram (in source app)
- **Right-click**: Context menu
- **Left-click + Drag**: Draw arrow (after selecting "Create Arrow")

## Tips

✅ **DO:**
- Copy high-resolution diagrams for best PDF quality
- Use crosshairs for precise alignment
- Resize window to see full diagram

❌ **DON'T:**
- Try to edit after saving (make changes before "Finish & Save PDF")
- Forget to copy image before running tool

## Troubleshooting

**"No image found in clipboard"**
→ Copy the image again before running the tool

**Tool won't start**
→ Make sure Python and Pillow are installed

**Arrows disappear**
→ They're still there - try resizing the window to refresh

## Next Steps

- Read full README.md for advanced features
- Customize attack labels in the code
- Share your annotated diagrams!

---

**Need help?** Open an issue on GitHub or check the full README.md
