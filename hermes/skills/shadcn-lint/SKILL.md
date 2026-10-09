---
name: shadcn-lint
description: Set up, run or tune @shadcn/lint (ESLint/Oxlint plugin for Tailwind v4 design systems) in a frontend project, or explain its rules such as no-restyle, no-raw-colors, no-arbitrary-values, no-inline-styles, no-unknown-classes and require-static-classes.
license: MIT
---

# @shadcn/lint

Source: [shadcn-ui/lint](https://github.com/shadcn-ui/lint) `SETUP.md` (MIT, commit recorded in Agent-setup shared/skills/SOURCES.md). @shadcn/lint is a lint plugin package, installed in the frontend project that owns the lint configuration. Install it when a Tailwind v4 frontend project exists; this skill holds the agent procedure.

Rule references are in `references/` (`rules.md`, `rules/*.md`, `design-systems.md`, `how-it-works.md`, `troubleshooting.md`, framework notes `react.md`, `vue.md`, `svelte.md`). Read the one the task needs.


Install and register `@shadcn/lint` in the user's project. For a setup-only
request, preserve the existing rule policy and leave new rules disabled. When
the project's current design contract or the user's request specifies rules,
configure those rules in the project and verify them against its components
and theme.

Read the setup and configuration documentation ([references/README.md](references/README.md), section "Get started")
before making changes. The examples there enable rules; use only the plugin
and parser setup for a setup-only request. Apply the project's selected rules
when the task includes design-system enforcement.

## Inspect the project

- Detect the package manager from the project metadata and lockfile.
- Determine whether this is a single project or a monorepo/workspace.
  Find the apps, shared UI packages, lint configs, and task runner.
- Use the existing ESLint or Oxlint setup. If both are present, register
  the plugin with the one that checks UI files, without duplicating it.
  If neither is present, set up Oxlint, or ESLint when the UI files are
  `.svelte` or `.vue`. Check Node.js and linter version
  compatibility against the documentation.
- Find the component directories, import aliases, and Tailwind v4 themes.
  Use `components.json` where available. For custom setups, consult the
  [discovery documentation](references/how-it-works.md)
  and configure only the settings the project needs.

## Install and register the plugin

Use the project's package manager. Install dependencies in the package
that owns the lint configuration. In a workspace, follow the existing
shared-config and dependency conventions.

Preserve existing rules, parsers, scripts, and ignores. Register the
plugin through `plugins` for ESLint or `jsPlugins` for Oxlint. Keep the
framework's parser configuration; add a JSX/TSX parser setup if needed.
For setup-only work, register the plugin without a new preset or rule. When
rules are part of the task, add only the rules and overrides supported by the
project's design contract; define component variants and tokens before
enforcing them. Use [the adoption guide](references/adoption.md) for an
existing project with findings.

In a Svelte or Vue project, templates are linted under ESLint only, with
`svelte-eslint-parser` or `vue-eslint-parser`. Register the plugin in the
ESLint block that covers `.svelte` or `.vue` files. If the project has
only Oxlint, keep it and tell the user that Oxlint checks the `<script>`
blocks and that templates need ESLint. See the
[Vue](references/vue.md) and [Svelte](references/svelte.md) documentation.

In a workspace, account for shared component imports and each app's
theme. Scope any discovery settings to the relevant apps and packages.
Avoid replacing app-specific settings with one workspace-wide value.

Ensure the lint command works with the project's scripts and workspace
task runner. Reuse the existing command where possible; add one if needed.

## Verify and hand off

Run the relevant lint commands to check that the configuration loads.
Separate configuration errors from existing lint findings. When rules were
configured, verify that representative allowed and violating classes produce
the expected results. With no new rules enabled, the check verifies setup.

Tell the user:

- What was installed and which configuration files changed.
- How to run lint, including workspace commands where applicable.
- Which rules and overrides were configured, or that setup-only work kept
  the existing rule policy.
- Where to adjust rules, and where to read the
  [available rules](https://github.com/shadcn-ui/lint/blob/main/README.md#rules)
  and [configuration examples](references/design-systems.md).

Use the current project design contract and the user's choices to determine
which rules apply and what each component allows.

## Rules at a glance

| Rule | What it catches |
|---|---|
| `no-restyle` | Restyling a component with `className` |
| `no-raw-colors` | Raw colors such as `bg-pink-500` |
| `no-arbitrary-values` | Arbitrary values such as `p-[13px]` |
| `no-inline-styles` | Inline styles and `<style>` elements |
| `no-unknown-classes` | Classes Tailwind cannot generate |
| `require-static-classes` | Component classes the linter cannot read, such as `` `bg-${color}` `` |

Rule options: `references/rules.md`. Adding rules over time: `references/adoption.md`.
