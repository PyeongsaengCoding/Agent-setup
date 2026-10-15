# User design-reference workflow

Use when researching design references or translating a selected reference into a UI system for this user.

- Read the project's reference-selection requirements before recommending or implementing. Present the required candidate count with original links, readable screens, evidence coverage, and recommended adoption elements; let the user choose before implementation.
- Distinguish directly exercised demos from documentation screenshots. Describe UX flow verification separately from visual inspection, and verify a reference's underlying design system before naming it.
- Treat the selected primary reference as the source of visual direction, including palette, typography, spacing, radius, borders, and shadows. Translate these into shadcn theme tokens and variants, then present the rendered result for approval. Avoid requiring the user to separately choose every token after choosing a reference.
- Use secondary references for specific workflow patterns while retaining one coherent visual theme. Adapt for Korean readability, accessibility, product states, and viewport constraints.
- Configure @shadcn/lint around the approved theme and component contracts. Keep official shadcn agent-skill installation, lint-plugin installation, rule activation, and actual execution as separate observed steps.
- Keep platform support explicit. Confirm compatibility before applying web shadcn components or lint tooling to native iOS or React Native work.
