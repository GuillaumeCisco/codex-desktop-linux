"use strict";

const assert = require("node:assert/strict");
const test = require("node:test");
const { applyPersistentFullAccessWarningDismissal } = require("./patch.js");

test("keeps a previously dismissed Full access warning dismissed on Linux", () => {
  const source = "function oBe(e,t,n){return e||t!=null&&n-t<=sBe}const key=`full-access-warning-dismissed-at-v2`";
  const patched = applyPersistentFullAccessWarningDismissal(source);
  assert.match(patched, /navigator\.userAgent\.includes\(`Linux`\)/u);
  assert.equal(applyPersistentFullAccessWarningDismissal(patched), patched);
  assert.equal(patched.includes("t!=null&&(typeof navigator"), true);
});
