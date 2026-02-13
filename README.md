# IEC 62443 Attack Path Annotator

A specialized Python GUI tool for annotating network diagrams with attack paths for IEC 62443 cybersecurity risk assessments. Designed for OT (Operational Technology) security professionals working with industrial control systems.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.6%2B-blue.svg)

## Overview

This tool streamlines the process of creating visual attack path documentation for IEC 62443 risk assessments. It allows you to quickly mark up network diagrams showing how attackers can breach zone boundaries and move through SCADA/DCS systems.

### Key Features

- 🎯 **Clipboard Integration** - Load network diagrams directly from clipboard
- 🎨 **Visual Attack Paths** - Draw red arrows with precise crosshair guides
- 🏷️ **Attack Type Labels** - Categorize paths (Zone Breach, Lateral Movement, Privilege Escalation)
- 🔄 **Dynamic Resizing** - Image and annotations scale automatically with window
- 🗑️ **Easy Editing** - Right-click context menu to add/delete arrows
- 📄 **PDF Export** - Save annotated diagrams at original resolution for reports

## Installation

### Prerequisites

- Python 3.6 or higher
- tkinter (usually included with Python)

### Install Dependencies

```bash
pip install Pillow
```

### Platform-Specific tkinter Installation

**Ubuntu/Debian:**
```bash
sudo apt-get install python3-tk
```

**macOS:**
tkinter is included with Python from python.org

**Windows:**
tkinter is included with Python from python.org

## Usage

### Quick Start

1. **Copy your network diagram** (from Visio, PowerPoint, etc.) to clipboard
2. **Run the tool:**
   ```bash
   python attack_path_annotator.py
   ```
3. **Create attack paths:**
   - Right-click → "Create Arrow"
   - Drag from attack source to target
   - Select attack type from dialog
4. **Save as PDF** when complete

### Detailed Workflow

#### Creating Attack Arrows

1. Right-click at the **start point** of the attack path
2. Select **"Create Arrow"** from menu
3. **Drag** to the end point (blue crosshairs guide your positioning)
4. **Release** mouse button
5. **Select attack type:**
   - Zone Boundary Breach
   - Lateral Movement
   - Privilege Escalation
6. Click **OK**

#### Deleting Arrows

- Right-click near the **start point** of an arrow (within 15 pixels)
- Select **"Delete Arrow"**
- Or use **"Clear All Arrows"** to remove everything

#### Saving Your Work

1. Click **"Finish & Save PDF"**
2. Choose save location and filename
3. Annotated diagram exports at original resolution

### Tips & Tricks

- **Horizontal arrows**: Text automatically offsets upward for better readability
- **Window resize**: Annotations scale perfectly when resizing the window
- **Crosshairs**: Blue crosshairs appear while drawing for precise alignment
- **Reload**: Use "Reload from Clipboard" to start fresh with a new diagram

## Use Cases

### OT Security Risk Assessments

- Document attack paths through SCADA systems
- Visualize zone and conduit vulnerabilities
- Create evidence for IEC 62443 compliance
- Support consequence-based risk analysis

### Network Security Reviews

- Mark up network segmentation diagrams
- Show lateral movement possibilities
- Identify security control gaps
- Create executive briefing materials

## IEC 62443 Context

This tool supports the following IEC 62443 activities:

- **Zone & Conduit Analysis** - Visualize security boundaries
- **Risk Assessment** - Document attack scenarios
- **Security Level Verification** - Show potential breaches
- **Countermeasure Planning** - Identify control placement needs

## Customization

### Adding Custom Attack Types

Edit the `attack_labels` list in the code (around line 35):

```python
self.attack_labels = [
    "Zone Boundary Breach",
    "Lateral Movement",
    "Privilege Escalation",
    "Data Exfiltration",          # Add your own
    "Command Injection",           # Add your own
]
```

### Styling

All arrows are red by default for visibility in risk documentation. The code can be modified to support:
- Different colors
- Line styles (dashed, dotted)
- Arrow sizes
- Font styles

## Technical Details

- **Language**: Python 3
- **GUI Framework**: tkinter
- **Image Processing**: Pillow (PIL)
- **Export Format**: PDF at 100 DPI
- **Coordinate Handling**: Automatic scaling between display and original resolution

## Troubleshooting

### No image found in clipboard
- Ensure you've copied an image (not a file path)
- Try copying from image viewer or snipping tool

### tkinter not found
- Windows/macOS: Reinstall Python from python.org
- Linux: `sudo apt-get install python3-tk`

### Arrows not in saved PDF
- Make sure arrows are visible before clicking "Finish & Save PDF"
- Check that the file actually saved to your chosen location

## Contributing

Contributions are welcome! This tool was created for the OT security community. If you have ideas for improvements:

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License

MIT License - Free for commercial and personal use

## Author

Created for OT cybersecurity professionals performing IEC 62443 risk assessments.

## Acknowledgments

Built to address the real-world needs of industrial control system security practitioners who need to quickly document attack paths in zone and conduit diagrams.

---

**Note**: This tool is for documentation purposes. Always follow responsible disclosure and authorization practices when performing security assessments.
