# Environment Setup with uv

This guide explains how to set up the project environment using [`uv`](https://docs.astral.sh/uv/) and Python 3.11.

The project pins Python `>=3.11,<3.12` in `pyproject.toml`. Note: the PCE metamodel `.pkl` files were reportedly serialized with Python 3.12, and loading them from another Python version may cause errors such as `SystemError: unknown opcode`. If you hit that error, re-check whether 3.12 is actually required for your `.pkl` files.

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

## 3. Sync the Environment

The project's dependencies are declared in `pyproject.toml` and pinned exactly in `uv.lock` (a lockfile, similar in spirit to the old `requirements.txt` but reproducible, with a resolved dependency graph). A single command downloads the pinned Python version (if needed), creates `.venv`, and installs every dependency:

```bash
uv sync
```

This is the same command whether `uv.lock` already exists (it's committed to this repo, so cloning and running `uv sync` reuses it as-is) or not (`uv sync` generates it first from `pyproject.toml`, then installs). You never need to run `uv lock` by hand unless you edited `pyproject.toml` manually instead of using `uv add`/`uv remove`.

The project pins `setuptools<81` because `UQpy 4.2.1` still imports `pkg_resources`. Newer `setuptools` versions may remove that module.

## 4. Activate the Environment

You don't strictly need to activate the environment — `uv run <command>` (see step 6) uses it automatically. Activating is convenient for interactive work (e.g. a plain Python shell).

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

Check that the environment is using Python 3.11:

```bash
python --version
```

Expected output:

```text
Python 3.11.x
```

## 5. Adding or Updating Dependencies

Do not edit `pyproject.toml`'s dependency list by hand for new packages. Instead:

```bash
uv add package_name
```

This resolves the new dependency, updates `pyproject.toml` and `uv.lock`, and installs it into `.venv`. To remove a dependency:

```bash
uv remove package_name
```

## 6. Run the PCE Dataset Generation Script

```powershell
uv run python .\beam_problem_1\01_glam_real_data\training_pce.py
```

The script saves the generated CSV file at the project root:

```text
training_pce_dataset.csv
```

## 7. Open the Notebook

The equivalent notebook is:

```text
beam_problem_1/01_glam_real_data/training_pce.ipynb
```

Use the `.venv` Python 3.11 kernel when running it.

## 8. Deactivate the Environment

If you activated the environment in step 4, deactivate it when finished:

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
uv sync
.\.venv\Scripts\Activate.ps1
uv run python .\beam_problem_1\01_glam_real_data\training_pce.py
```

### Linux and macOS

```bash
uv sync
source .venv/bin/activate
uv run python beam_problem_1/01_glam_real_data/training_pce.py
```
