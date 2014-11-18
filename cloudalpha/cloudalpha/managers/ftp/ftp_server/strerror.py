import pyftpdlib.handlers  # @UnusedImport

""""Redifine pyftpdlib.handlers._sterror function."""
pyftpdlib.handlers._strerror = lambda err: str(err)
