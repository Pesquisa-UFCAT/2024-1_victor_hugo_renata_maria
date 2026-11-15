from pathlib import Path
import runpy
globals().update(runpy.run_path(str(Path(__file__).resolve().parents[1]/'conf_shared.py'), init_globals={'SITE_LANGUAGE':'pt'}))
