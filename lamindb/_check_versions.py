from bionty import __version__ as bionty_v
from lndb import __version__ as lndb_v
from lnschema_core import __version__ as lnschema_core_v
from nbproject import __version__ as nbproject_v
from packaging import version

if version.parse(lndb_v) != version.parse("0.36.0"):
    raise RuntimeError("Upgrade lndb! pip install lndb==0.36.0")

if version.parse(lnschema_core_v) != version.parse("0.29.1"):
    raise RuntimeError("lamindb needs lnschema_core==0.29.1")

if version.parse(bionty_v) != version.parse("0.7.0"):
    raise RuntimeError("lamindb needs bionty==0.7.0")

if version.parse(nbproject_v) < version.parse("0.8.2"):
    raise RuntimeError("lamindb needs nbproject>=0.8.2")

# ensure that the lamin package is not installed
try:
    import lamin  # noqa

    raise RuntimeError(
        "Please run: pip uninstall lamin\nIn case you used the lamin Python API, please"
        " now use: import lamindb.setup as lnsetup"
    )
except ImportError:
    pass
