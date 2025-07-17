# 🛠️ Project Setup Using [UV](https://github.com/astral-sh/uv)

This guide explains how to set up and manage a Python project using **UV**, a fast Python package manager and virtual environment tool.

---

## 📁 1. Initialize a New Project

```bash
uv init <project_name>
cd <project_name>
```

This creates a new UV project with a `pyproject.toml` file.

---

## 🐍 2. Create a Virtual Environment

```bash
uv venv
```

This manually creates a `.venv` directory for your project.

---

## ▶️ 3. Activate the Virtual Environment

**Windows:**

```bash
.venv\Scripts\activate
```

**Unix/Linux/macOS:**

```bash
source .venv/bin/activate
```

---

## 🚀 4. Run a Python File Using UV

```bash
uv run <file_name.py>
```

---


## 📜 5. Run a File as a Script from `pyproject.toml`

Organize your code in a `src/` directory, and define your entry point in the `pyproject.toml` using the `[project.scripts]` section.

### 🗂️ Project Structure Example

```
my_project/
├── pyproject.toml
├── src/
│   ├── __init__.py
│   └── main.py
```

### 📄 `src/main.py`

```python
def main():
    print("Hello from UV script!")
```

### 📝 `pyproject.toml`

```toml
[project]
name = "my_project"
version = "0.1.0"
description = "A sample UV project with scripts"
authors = [{ name = "Your Name", email = "you@example.com" }]
requires-python = ">=3.12"

[project.scripts]
hello = "hello.main:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src"]
```

### ▶️ Run the Script

```bash
uv run hello
```

---

Let me know if you want the full updated `README.md` with this included!

## ➕ 6. Add a Package

```bash
uv add <package_name>
```

---

## ➖ 7. Remove a Package

```bash
uv remove <package_name>
```

---

## 🔄 8. Sync Packages from `pyproject.toml`

```bash
uv sync
```

This installs or updates all dependencies listed in the `pyproject.toml` file.

---

## 🌳 9. View Dependency Tree

```bash
uv tree
```

This shows a tree view of all installed dependencies.

---

## ⬆️ 10. Update All Packages in Lock File

To upgrade all dependencies:

```bash
uv lock --upgrade
uv sync
```