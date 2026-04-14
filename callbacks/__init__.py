"""Callback registration — importing submodules triggers @callback decoration."""

import callbacks.build  # noqa: F401
import callbacks.manage  # noqa: F401
import callbacks.admin  # noqa: F401
