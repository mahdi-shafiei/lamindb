from lamindb_setup.core._docs import doc_args
from lamindb_setup.core.upath import UPath, create_path

from lamindb.models import Storage


@property  # type: ignore
@doc_args(Storage.path.__doc__)
def path(self) -> UPath:
    """{}"""  # noqa: D415
    access_token = self._access_token if hasattr(self, "_access_token") else None
    return create_path(self.root, access_token=access_token)


Storage.path = path  # type: ignore
