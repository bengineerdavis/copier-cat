# Copier composition experiment evidence

This directory preserves the November 2026 experiments that established the
assembly design's empirical boundaries. It is separate from the synthetic
assembly UX prototype and from production code.

The archive contains 34 small source fixtures, observed outputs, and failure
artifacts. Nested Git metadata and bytecode caches were intentionally excluded.
The `rejdemo` answers file's absolute local template source was normalized to
`/example/base` for publication; no project data or secret is retained.

## What the experiments established

1. **Two ordinary renders do not compose.** Rendering the base and layer into
   one destination produced `conflict mise.toml`; the base survived and the
   layer's `roborev` contribution was lost.
2. **Text concatenation is not composition.** Repeating `[tools]` produced the
   parser error `Cannot declare ('tools',) twice`.
3. **Cross-root Jinja includes do not solve composition.** An include outside
   the template root raised `TemplateNotFound`; excluding a fragment directory
   also removed it from Jinja's search path.
4. **Copier hides underscore-prefixed data from templates.** The `_layers`
   ordering variable rendered as undefined.
5. **`{% do %}` was unavailable** in the tested Copier/Jinja configuration.
6. **Structured mappings can compose before one render.** `combined5` emits one
   valid TOML document from structured `tools` and `tasks` mappings. Its
   contributions retain `python`, `roborev`, and both task entries.
7. **A partial `--data` override replaces a whole mapping.** The experiment
   supplying only `tools={"python":"3.13"}` lost the existing `roborev` entry;
   unrelated `tasks` survived. Complete merged data must reach Copier as one
   input, or structured render results must be composed afterward.
8. **A rejected update hunk needs visible handling.** `rejdemo/mise.toml.rej`
   preserves the local edit that Copier did not apply, while the working file
   retained the template's test command. A forward-update runner must not
   report success while such rejected hunks remain unreviewed.
9. **Template iteration needs a committed, tagged fixture.** Copier resolves a
   Git template's recorded reference rather than its arbitrary working-tree
   edits. Test fixtures must commit and update their reference deliberately.

These observations motivated decision-7's native-render extraction followed by
structured composition. They do not establish compatibility for arbitrary
unmodified templates.

## Directory map

- `base/`, `layer/`: the two ordinary template fixtures.
- `combined/` through `combined4/`: unsuccessful or intermediate approaches.
- `combined5/`: the working structured-data render.
- `out*`, `probe-vis/`: observed render outputs and variable-visibility checks.
- `rejdemo/`: the rejected-hunk failure artifact.

## Reproduce the working structured-data fixture

From the repository root on this evidence branch:

```sh
uv run copier copy --defaults prototype/cc-composition-evidence/combined5 /example/output
```

Use an explicit disposable destination rather than `/example/output` in actual
use. The command renders a small synthetic TOML fixture only; it does not
render the real Python or agentic templates.

## Production ownership

CCC-24 owns the first real Python assembly slice. CCC-25 owns composition of
the independent agentic overlay through the existing composition engine. This
archive informs those tasks; it is not their implementation or test suite.
