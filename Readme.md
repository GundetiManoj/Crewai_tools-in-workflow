## 🤖 CrewAI Multi-Tool Collection

A comprehensive collection of AI-powered tools built with CrewAI framework, featuring document analysis, code review, text processing, API testing, and much more. This repository demonstrates the power of multi-agent AI systems for various automation tasks.

## ✨ Features

### 🔧 Code Analysis Tools
- **Bug Detection & Fixing**: Automatically detect and fix code bugs
- **Performance Optimization**: Analyze and optimize code performance
- **Security Vulnerability Scanner**: Identify and fix security issues
- **External API Detector**: Find all external API calls in code

### 📄 Document Processing Tools
- **Document Parser**: Extract structured data from PDFs using Google Document AI
- **Text Summarization**: Generate concise summaries of long texts
- **Document Comparison**: Compare two documents and highlight differences
- **Document Classification**: Categorize documents into predefined categories

### 🌐 API & Integration Tools
- **API Invocation Tool**: Validate and execute API requests with LLM validation
- **XML to JSON Converter**: Convert XML data to JSON format
- **Translation Bot**: Translate text between multiple languages

### ✍️ Text Processing Tools
- **Text Correction**: Fix spelling, grammar, and factual errors
- **Text Elaboration**: Expand text with relevant details and context
- **Persona Style Changer**: Rewrite text in different personas/styles

### 🔍 Computer Vision Tools
- **Face Verification**: Compare faces to determine if they belong to the same person



## Setup Instructions


### Using Python 3.11 Virtual Environment

At the time of writing, we need a Python virtual environment with Python 3.11.

#### Option 1: Python 3.11 is Already Installed

##### Step 1: Verify Python 3.11 Installation

```bash
python3.11 --version
```

##### Step 2: Create a Virtual Environment

```bash
python3.11 -m venv .venv
```

This creates a `.venv` folder in your current directory.

##### Step 3: Activate the Virtual Environment

- **macOS/Linux:**
  
  ```bash
  source .venv/bin/activate
  ```

- **Windows:**
  
  ```cmd
  .venv\Scripts\activate
  ```

You should see `(.venv)` in your terminal prompt.

##### Step 4: Verify the Python Version

```bash
python --version
```

##### Step 5: Install Packages

```bash
pip install -r requirements.txt
```

Requirements.txt
```
crewai-tools
crewai
langchain-community
onnxruntime
transformers
langchain_groq
torch
google-search-results

```

---

#### Option 2: Install Python 3.11

If you don’t have Python 3.11, follow the steps below for your OS.

##### **macOS (Using Homebrew)**

```bash
brew install python@3.11
```

##### **Ubuntu/Debian**

```bash
sudo apt update
sudo apt install python3.11 python3.11-venv
```

##### **Windows (Using Windows Installer)**

1. Go to [Python Downloads](https://www.python.org/downloads/release/python-3110/).
2. Download the installer for Python 3.11.
3. Run the installer and ensure **"Add Python 3.11 to PATH"** is checked.

### Verify Installation

```bash
python3.11 --version
```

## Notebooks

In the activated environment, run

```bash
python3 -m jupyter notebook
