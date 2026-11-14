---
id: DOC-5
title: Evidence for a copier-cat short CLI alias
---

# Short CLI alias

## Decision

Use **`ccc`** as the local CLI alias, while retaining **`copier-cat`** as the
product name, Python distribution name, registry identity, and unambiguous
executable.

The maintainer selected this package/binary split after reviewing the PyPI
collision. The existing `CCC` distribution is Cloud Custom Connections, a
Django CRM/marketing application for contacts, lead capture, and automated
email/SMS/voice campaigns. Its metadata points to `github.com/CloudPR/CCC` and
its only listed release, 2.0.1, was uploaded on 2019-01-29. It is not a template
manager or an apparent executable conflict; `ccc` is not installed locally.
The collision affects the registry token, not this distinct alias. No PEP 541
name-transfer action is proposed.

[PyPI metadata](https://pypi.org/pypi/CCC/json) was checked on 2026-11-14.
This decision does not claim the `ccc` package name or install any executable.

`tpls` remains the mechanically clear fallback if the local alias later proves
confusing. `ktc` has an existing Kendo template precompiler and `tstack` has
strong developer-tool identities, so neither is preferred.

## Evidence

Target: public Python CLI; PyPI/Git distribution, with optional dotagents skill
packaging. Current implementation is Python; no Rust port is planned. Target
platforms are macOS and Linux. The package/binary split is deliberate:
`copier-cat` owns the distribution and product identity; the short token is only
a convenience executable.

`check-name` from the naming skill was run with `--only pypi,github` on
2026-11-14. GitHub returned `unknown` for the final candidate checks, so
`check-name` alone did not establish full clearance. A direct web brand search
supplemented it for `ktc` and `tpls`; it does not prove global availability.

| Token | Result | Reason |
| --- | --- | --- |
| `tpls` | PyPI free; not installed; no comparable template/developer CLI found in direct search | Best current short-alias candidate. A weak plural abbreviation, but acceptable beside `copier-cat`. |
| `ktc` | PyPI free; not installed; GitHub check unknown | Existing Kendo template precompiler `jquense/node-ktc` and other KTC developer tools make the template-domain collision material. |
| `tstack` | PyPI free; GitHub check initially successful | Strong `tstack/lnav` developer-tool identity and `t3dotgg/tstack`; also evokes Haskell Stack. |
| `ccc` | PyPI taken (`CCC`, 2019) | Not clear. No PEP 541 action proposed. |
| `cct` | PyPI taken (`cct`, 2016) | Not clear. |
| `ccat` | PyPI taken; `owenthereal/ccat` exists | Not clear. |
| `pcc` | PyPI taken | Not clear. |
| `cca` | PyPI taken | Not clear. |
| `pcat` | PyPI taken | Not clear. |
| `cpcat` | PyPI taken | Not clear. |
| `tcat` | PyPI taken; `marcomorain/tcat` exists | Not clear. |
| `kt` | PyPI taken; widely associated with Kotlin | Not clear. |
| `stak` | PyPI taken | Not clear. |

`/usr/bin/cc` is the system C compiler, so `cc` is disqualified regardless of
registry availability.

## Open choice

Adopt `tpls`, keep only `copier-cat`, or run a wider naming council if the
maintainer wants a more distinctive public identity. No executable, package,
symlink, or documentation alias is changed by this report.
