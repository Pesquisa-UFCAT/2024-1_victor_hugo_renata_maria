# Environment Setup with uv

This guide explains how to set up the project environment using [`uv`](https://docs.astral.sh/uv/) and Python 3.12.

Python 3.12 is recommended because the PCE metamodel `.pkl` files were serialized with Python 3.12. Using another Python version may cause errors such as `SystemError: unknown opcode`.

## 1. Install uv

### Linux and macOS

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Windows PowerShell

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

After installation, check that `uv` is available:

```bash
uv --version
```

If the command is not recognized, close and reopen the terminal.

## 2. Open the Project Folder

From the terminal, go to the project root:

```powershell
cd C:\git-projetos\2024-1_victor_hugo_renata_maria
```

## 3. Install Python 3.12

`uv` can download and manage the Python version used by the project:

```bash
uv python install 3.12
```

## 4. Create the Virtual Environment

Create a local environment named `.venv` using Python 3.12:

```bash
uv venv --python 3.12 .venv
```

## 5. Activate the Environment

### Linux and macOS

```bash
source .venv/bin/activate
```

### Windows PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
```

### Windows Command Prompt

```bat
.venv\Scripts\activate.bat
```

Check that the environment is using Python 3.12:

```bash
python --version
```

Expected output:

```text
Python 3.12.x
```

## 6. Install Dependencies

With the environment activated, install the packages listed in `requirements.txt`:

```bash
uv pip install -r requirements.txt
```

The project pins `setuptools<81` because `UQpy 4.2.1` still imports `pkg_resources`. Newer `setuptools` versions may remove that module.

## 7. Run the PCE Dataset Generation Script

```powershell
python .\beam_problem_1\01_glam_real_data\training_pce.py
```

The script saves the generated CSV file at the project root:

```text
training_pce_dataset.csv
```

## 8. Open the Notebook

The equivalent notebook is:

```text
beam_problem_1/01_glam_real_data/training_pce.ipynb
```

Use the `.venv` Python 3.12 kernel when running it.

## 9. Deactivate the Environment

When finished, run:

```bash
deactivate
```

## Removing the Old Environment

The old `myenv` folder may be locked if a terminal, Jupyter kernel, or VS Code session is still using it.

Close anything using `myenv`, then run:

```powershell
Remove-Item -LiteralPath .\myenv -Recurse -Force
```

If Windows still reports `Access denied`, restart VS Code or Windows and run the command again.

## Command Summary

### Windows PowerShell

```powershell
cd C:\git-projetos\2024-1_victor_hugo_renata_maria
uv python install 3.12
uv venv --python 3.12 .venv
.\.venv\Scripts\Activate.ps1
uv pip install -r requirements.txt
python .\beam_problem_1\01_glam_real_data\training_pce.py
```

### Linux and macOS

```bash
uv python install 3.12
uv venv --python 3.12 .venv
source .venv/bin/activate
uv pip install -r requirements.txt
python beam_problem_1/01_glam_real_data/training_pce.py
```
