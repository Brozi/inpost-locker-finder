# [Your solution name]

## Author

- **Name:** [Your full name]
- **Email:** [Your contact email]

## Overview

InPost Locker Finder (`ilf`) is a fast, 
user-friendly Command Line Interface (CLI) application that helps 
users locate InPost lockers (Paczkomat) and points across Poland directly from 
their terminal. It streamlines the process of finding operating points by 
allowing users to search by city or postal code, and instantly 
filter results by street, 24/7 availability, or Easy Access Zones. 
Its main advantage over already existing solutions is the reduced friction for 
advanced power users in the task of finding a suitable InPost point. Users can do so right 
from the comfort of their terminal, without needing to "click through" multiple menus.


## Demo & Description

[Describe your solution in detail. What does it do? How does it work? What approach did you take and why? Cover the key technical choices, architecture, and anything else that helps us understand your project without reading every line of code.]

If applicable, include:
- a link to the deployed solution
- screenshots of the UI or key outputs
- a short screen recording or demo video

## Technologies

[List the technologies, frameworks, and libraries you used. You can also explain why you decided to use them.]

## Build and run

### Prerequisites
- Python 3.9 or higher installed on your system.

### Installation Steps

**1. Clone the repository**
```bash
git clone https://github.com/Brozi/inpost-locker-finder.git
cd inpost-locker-finder
```

**2. Create and activate a virtual environment (Recommended)**
To keep the dependencies isolated, create a virtual environment inside the project folder:

*On Windows:*
```bash
python -m venv .venv
.venv\Scripts\activate
```

*On macOS/Linux:*
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**3. Install the application**
Install the package in editable mode. This automatically installs all required dependencies (Typer, Rich, Requests) and registers the global `ilf` command.
```bash
pip install -e .
```

### Running the Application

Once installed, you can use the `ilf` command directly in your terminal.

**Search for lockers:**
```bash
ilf find Kraków
ilf find "ul. Długa"
ilf find 32-064
```

**View the help menu:**
```bash
ilf --help
```

## Standalone Executables

If you prefer not to install the Python package, you can run the application as a compiled, standalone executable.

### Using Pre-built Releases
Pre-built binaries are generated automatically via GitHub Actions. You can download them from the **[Releases](../../releases)** page.

**On Windows:**
Open Command Prompt or PowerShell, navigate to the folder with the downloaded file, and run:
```cmd
.\ilf.exe find Kraków
```

**On macOS / Linux:**
You must grant execute permissions to the file before running it from the terminal:
```bash
# Rename the file (use mv ilf-macos ilf if on Mac)
mv ilf-linux ilf

# Make it executable
chmod +x ilf

# Run the app directly!
./ilf find Kraków
```

### Building Your Own Executable
You can bundle the application into a single executable file yourself using `PyInstaller`. Ensure you are inside your activated virtual environment.

**1. Install PyInstaller:**
```bash
pip install pyinstaller
```

**2. Build the binary:**
```bash
pyinstaller --name ilf --onefile src/ilf/__main__.py
```

**3. Run your built executable:**
The compiled file will be generated inside the `dist/` folder.
*On Windows:*
```cmd
.\dist\ilf.exe find Kraków
```
*On macOS/Linux:*
```bash
./dist/ilf find Kraków
```

### Build & run

[Step-by-step instructions to get your solution running from a clean clone of the repository. Be specific — commands, not just descriptions.]

```bash
# example:
# git clone <your-repo-url>
# cd <your-repo>
# ... your build/run commands here
```

## What I would do with more time

[If you had another week, what would you add, refactor, or change? Prioritize — what would you tackle first and why?]

## AI usage

[Did you use AI tools (ChatGPT, Copilot, Claude, etc.) while working on this? If yes, describe how — which parts did they help with, and how did you verify and adapt their output?]

## Anything else?

[Is there something we should know that doesn't fit the sections above? A design choice that needs context, a creative twist, a rabbit hole you went down — this is your space.]