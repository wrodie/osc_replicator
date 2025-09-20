def flatten_osc_args(args):
    """Recursively flatten and filter OSC arguments to only valid types."""
    _OSC_ARG_TYPES = (str, int, float, bool, type(None))
    flat = []

    def _flatten(item):
        if isinstance(item, (tuple, list)):
            for sub in item:
                _flatten(sub)
        elif isinstance(item, _OSC_ARG_TYPES):
            flat.append(item)

    _flatten(args)
    return flat
