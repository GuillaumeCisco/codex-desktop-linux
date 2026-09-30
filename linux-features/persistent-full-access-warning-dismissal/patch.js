"use strict";

const MARKER = "codexLinuxPersistentFullAccessWarningDismissal";
const warningPredicate =
  /function ([A-Za-z_$][\w$]*)\(([A-Za-z_$][\w$]*),([A-Za-z_$][\w$]*),([A-Za-z_$][\w$]*)\)\{return \2\|\|\3!=null&&\4-\3<=([A-Za-z_$][\w$]*)\}/gu;

function applyPersistentFullAccessWarningDismissal(source) {
  if (source.includes(MARKER)) return source;
  if (!source.includes("full-access-warning-dismissed-at-v2")) return source;
  const matches = [...source.matchAll(warningPredicate)];
  if (matches.length !== 1) {
    console.warn("WARN: Could not uniquely match the Full access warning timer");
    return source;
  }
  const [needle, name, session, dismissedAt, now, duration] = matches[0];
  const replacement =
    `function ${name}(${session},${dismissedAt},${now}){return ${session}||` +
    `${dismissedAt}!=null&&(typeof navigator!=\`undefined\`&&` +
    `navigator.userAgent.includes(\`Linux\`)/*${MARKER}*/||` +
    `${now}-${dismissedAt}<=${duration})}`;
  return source.replace(needle, replacement);
}

module.exports = {
  applyPersistentFullAccessWarningDismissal,
  descriptors: [{
    id: "linux-persistent-full-access-warning-dismissal",
    phase: "webview-asset",
    order: 20_950,
    ciPolicy: "optional",
    pattern: /^app-primary-[^.]+\.js$/u,
    missingDescription: "Full access warning state bundle",
    skipDescription: "persistent Full access warning dismissal patch",
    apply: applyPersistentFullAccessWarningDismissal,
  }],
};
