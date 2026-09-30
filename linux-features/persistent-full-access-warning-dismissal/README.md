# Persistent Full Access Warning Dismissal

The verified official Linux build 26.928 still expires a dismissed Full Access
warning after thirty days. This opt-in feature preserves the current Pro
behavior on Linux: once dismissed, the warning stays dismissed. A warning
that has never been dismissed still appears.

Run `node --test linux-features/persistent-full-access-warning-dismissal/test.js`
and inspect the enabled-feature patch report after building the verified official Linux package.
