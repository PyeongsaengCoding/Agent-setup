---
name: product-monetization-requirements
description: "Use when defining paid access, ad removal, or renewals."
---

# Product Monetization Requirements

Use alongside the product-brief workflow when product planning includes paid access, banner removal, introductory offers, or renewals. Keep product-specific prices, durations, and decisions in the owning product contract.

## Procedure

1. Read the owning requirements and identify explicit owner decisions separately from assistant suggestions. Replace superseded durations and flows in the current contract. Ask only about unresolved choices that materially change charging or access.
2. Define the offer trigger, whether introductory access is free or paid, payment-success requirement, entitlement start, expiry, and the path for declining purchase. Use the owner's explicit free/paid decision for introductory access. When wording mixes a trial with a purchase invitation and the introductory charge remains unclear, confirm that charge before recording paid access. Apply owner corrections to both the current contract and acceptance checks. Preserve a requested first actual banner exposure trigger rather than substituting installation time or first launch.
3. Specify renewal separately from billing duration. For a yearly product with manual renewal, require an explicit user purchase for each term. Carry a no-automatic-billing decision into product configuration, purchase copy, confirmation, and expiry behavior; calling a product a subscription leaves renewal behavior unspecified.
4. Present introductory cost, access duration, and renewal behavior together at the offer decision. For free introductory access, explicitly label the offer and start button as free, activate access without a payment-success requirement, and state whether payment-method registration is required. Keep free activation and subsequent paid annual purchase as distinct stages; copying paid-purchase wording into a free offer misstates when the user is charged. At the paid decision, display price and term together. When requested, display `자동결제 없음` on both introductory and annual offers and require explicit purchase for each paid term.
5. Define free activation, purchase success, cancellation, failure, restoration, reinstall, and expiry transitions. Keep free and paid ad-removal entitlements separate from temporary ad-click suppression, and identify every banner placement covered by each mechanism. Preserve the owner's chosen free-use fallback when an offer is declined or access expires.
   - Before answering whether a banner timer exists or how long it lasts, trace the contract field to its definition and response construction in the owning source. Distinguish background execution interval, banner display trigger/duration, and post-click suppression; these control different events.
   - Check whether the timer is a fixed source constant or an editable setting before describing it as configurable. Derive the duration from the implementation with a calculation tool, and keep locally observed values separate from deployed configuration and host behavior. A field name or generic contract alone establishes neither the duration nor production enforcement.
   - When changing suppression duration, align the runtime value, affected host behavior, user-facing click explanation, and acceptance checks. Keep product-specific timer values in the product contract rather than this skill.
6. Update the authoritative contract and its acceptance checks together. Include offer trigger and copy, configured renewal mode, confirmed purchase, all affected placements, expiry fallback, and explicit repurchase. For generator-document changes, verify the entry document still links to the contract, check required clauses, and run `git diff --check`; choose additional tests by the changed execution path.
7. Report the changed purchase flow briefly. Separate verified document requirements from exercised payment configuration and real user-flow evidence; leave prices or period-calculation details explicitly open when the owner has not selected them.

## Completion gate

- Introductory access has an explicit paid/free decision and start event.
- Every term has explicit expiry and renewal behavior.
- Purchase copy and configured charging behavior have matching acceptance checks.
- Covered ad placements and purchase-state transitions are specified.
- Verification claims match the actual checks performed.
