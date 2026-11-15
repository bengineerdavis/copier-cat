# Assembly UX prototype evidence

This directory preserves the synthetic assembly-CLI interaction prototype used
during the November 2026 design sessions. It is evidence for CCC-11, CCC-14,
CCC-17, and the resulting implementation queue.

The two Python source files preserve the original prototype, with one
annotation-only corrections: the simulated result and local answers mappings
allow `None` because the initialization result uses that value. `prototype.py`
simulates stack selection, assembly, guided review,
output modes, configuration initialization, and failure handling.
`help_contract.py` supplies the shared human and machine-readable help model.

## Evidence boundary

This is not production code. It does not invoke Copier, render templates,
compose files, or run generated-project tests. Assembly destinations and
validation results are simulated. The smoke checks exercise only the simulated
interface; they do not validate an assembled project.

The `init` simulation can write a comment-only review marker when you explicitly
approve it and set `CCC_CONFIG_FILE` to an absolute disposable path. No such
environment variable is set by these checks. Do not use a real user
configuration path for this prototype.

The production implementation starts with CCC-24. CCC-26 owns the shared
command-discovery contract, and CCC-27 owns the optional conversational skill.

## Run the checks

From the repository root on the `prototype/cc-assembly-ux` branch:

```sh
uv run pytest prototype/cc-assembly-ux/test_prototype.py -q
```

Run the simulated interface directly:

```sh
python3 prototype/cc-assembly-ux/prototype.py --help
python3 prototype/cc-assembly-ux/prototype.py help --json
python3 prototype/cc-assembly-ux/prototype.py assemble example-project --stack example-stack --dry-run
python3 prototype/cc-assembly-ux/prototype.py assemble example-project --stack example-stack --json
```

Use `example-project` and `example-stack` only as harmless placeholders. JSON
alone produces a read-only plan. `--yes` approves only the simulated destination
write; it does not create a real project.

## Branch ownership

This evidence branch intentionally follows the existing
`prototype/cc-composition-cli` publication model. Production `main` links to
this branch rather than carrying the synthetic prototype or external workspace
paths. The older composition/phone-home HTML prototype remains separate.
