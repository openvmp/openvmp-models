import os


def get_models_dir():
    lib_dir = os.path.dirname(__file__)
    models = os.path.join(lib_dir, os.pardir)
    return os.path.realpath(models)
