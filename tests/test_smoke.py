import importlib.metadata

import copier


def test_package_imports_and_declares_copier_dependency() -> None:
    import copier_cat

    assert copier_cat.__doc__ is not None
    assert importlib.metadata.version("copier-cat")


def test_copier_is_importable_for_c2_diff_reuse() -> None:
    # The diff-sourcing decision (spec decision record) commits cc to
    # reusing copier's own update computation; this pins that the
    # dependency actually resolves in the harness venv.
    assert hasattr(copier, "__version__")
