registry = []

def register(klass):
    """Adds the wrapped class to the registry"""
    registry.append(klass)
    return klass
