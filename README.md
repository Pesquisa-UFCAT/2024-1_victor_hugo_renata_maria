# Paper Victor Hugo and Renata Maria

## 1. How to Set Up a Python Virtual Environment and Install Requirements to use METApy locally

#### 1.1 Create the virtual environment (depends on your installation)
```bash
python3 -m venv myenv
# or
python -m venv myenv
# or
python3.10 -m venv myenv
```

#### 1.2 Activate the virtual environment  
```bash
source myenv/bin/activate # On Linux or macOS
myenv\Scripts\activate    # On Windows
```

#### 1.3 Install required packages
```bash
python.exe -m pip install --upgrade pip
pip install -r requirements.txt
```

#### 1.4 To deactivate the virtual environment
```bash
deactivate
```

## 2. Use pip-chill to manage your `requirements.txt` file  
  
#### 2.1 To install any packages or packages which are outside of `requirements.txt`
```bash
pip install your_package
```

#### 2.2 After installation, update the `requirements.txt` file
```bash
pip-chill > requirements.txt
```

# Notes

- [Important dataset](https://carbuai.pythonanywhere.com/about_us)  
- Dataset: `renata\rccarbonation.xlsx`

# Main papers
- [paper dataset](https://drive.google.com/open?id=1yzvW4NIV35N7V_6y5RW59U3tiGp_AwL6&usp=drive_fs)
- [board](https://wbd.ms/share/v2/aHR0cHM6Ly93aGl0ZWJvYXJkLm1pY3Jvc29mdC5jb20vYXBpL3YxLjAvd2hpdGVib2FyZHMvcmVkZWVtLzNkZTZjYzQ0MTA4MzQ1ODVhMDJjNGJhZjFhMTc4ZDI0X0JCQTcxNzYyLTEyRTAtNDJFMS1CMzI0LTVCMTMxRjQyNEUzRF84YTZiZTY1MS04MjYyLTRlN2MtYTQyOS00MzZlNmRiNTQ0ODU=)
# Documentation

The API reference for `functions.py` is built with Sphinx from the `docs/` folder:

```bash
uv sync --group docs
uv run sphinx-build -b html docs docs/_build/html
```

Then open `docs/_build/html/index.html`.
