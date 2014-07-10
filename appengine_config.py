
# --- START GAELIC IMPORTER ---

def gaelic_fix_path(path):
    import sys, os
    base = os.path.dirname(__file__)
    lib = os.path.join(base, path)
    if not lib in sys.path:
        sys.path.append(lib)


gaelic_fix_path('lib')

# --- END GAELIC IMPORTER ---

