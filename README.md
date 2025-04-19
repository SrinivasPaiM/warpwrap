---

# 🌐 Cloudflare WARP Manager (Modern Windows Edition)

A sleek desktop GUI app built with **Python + CustomTkinter** to manage **Cloudflare WARP** VPN using the `warp-cli`.  
Includes network tools, Steam/Epic Games launcher detection, DNS leak testing, and dynamic status updates.

---

## 🚀 Features

- ✅ **Enable/Disable Cloudflare WARP** with one click  
- 🟢 Live status indicator for WARP connection  
- 🧠 Auto-detect and warn if Steam or Epic Games Launcher is running  
- 🌐 Open [DNS Leak Test](https://www.dnsleaktest.com/) directly  
- 🎨 Toggle between Light, Dark, and System themes  
- 🧠 Keyboard shortcut: `Ctrl + Shift + Q` to toggle WARP  
- 🛠️ Beautiful **CustomTkinter** UI with icons and theme switching

---

## 📦 Requirements

- Python 3.8+
- Cloudflare WARP + WARP CLI  
  Download from [https://1.1.1.1](https://1.1.1.1)

### Python Dependencies

Install with:

```bash
pip install customtkinter CTkMessagebox pillow psutil
```

---

## 🧰 How to Run

```bash
python warp_manager.py
```

Or double-click the `warp_manager.py` file if Python is configured correctly.

---

## 🔒 Create Executable (.exe)

Want to turn it into a `.exe`?

### Step-by-Step using `auto-py-to-exe`:

1. Install the tool:
    ```bash
    pip install auto-py-to-exe
    ```

2. Run:
    ```bash
    auto-py-to-exe
    ```

3. In the GUI:
   - Script Location: Select your `warp_manager.py`
   - Onefile: ✅ Check
   - Window based: ✅ Check (to hide terminal)
   - Add your `warpwraplogo.png` as **Additional Files**
   - Icon (optional): Add a `.ico` file for the app

4. Click **Convert .py to .exe**

Your `.exe` will be in the `output` folder.

---

## 💻 Development Setup

You can edit the UI or functions in **PyCharm** or **VS Code**.  
The file structure is simple:

```
/your-folder
│
├── warp_manager.py
├── warpwraplogo.png
└── README.md
```
