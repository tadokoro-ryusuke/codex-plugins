#!/usr/bin/env node

import { existsSync, readFileSync } from "node:fs";
import { dirname, isAbsolute, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const scriptDir = dirname(fileURLToPath(import.meta.url));
const root = resolve(scriptDir, "..");
const defaultSuite = join(root, "plugins/dev-core/evals/skill-behavior-cases.json");
const suitePath = process.argv[2]
  ? isAbsolute(process.argv[2])
    ? process.argv[2]
    : resolve(process.cwd(), process.argv[2])
  : defaultSuite;
const errors = [];

function nonEmptyStrings(value) {
  return Array.isArray(value) && value.length > 0 && value.every((item) => typeof item === "string" && item.trim().length > 0);
}

let suite;
try {
  suite = JSON.parse(readFileSync(suitePath, "utf8"));
} catch (error) {
  console.error(`${suitePath}: cannot read eval suite (${error.message})`);
  process.exit(1);
}

if (suite.schemaVersion !== 1) errors.push("schemaVersion must be 1");
if (typeof suite.suite !== "string" || suite.suite.trim().length === 0) errors.push("suite must be a non-empty string");
if (!nonEmptyStrings(suite.evaluatorNotes)) errors.push("evaluatorNotes must be a non-empty string array");
if (!Array.isArray(suite.cases) || suite.cases.length === 0) {
  errors.push("cases must be a non-empty array");
} else {
  if (suite.cases.length < 6) errors.push("cases must keep at least 6 autonomy and safety scenarios");
  const ids = new Set();
  for (const [index, testCase] of suite.cases.entries()) {
    const label = `cases[${index}]`;
    if (!testCase || typeof testCase !== "object" || Array.isArray(testCase)) {
      errors.push(`${label} must be an object`);
      continue;
    }
    if (typeof testCase.id !== "string" || !/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(testCase.id)) {
      errors.push(`${label}.id must be unique kebab-case`);
    } else if (ids.has(testCase.id)) {
      errors.push(`${label}.id duplicates ${testCase.id}`);
    } else {
      ids.add(testCase.id);
    }
    if (typeof testCase.skill !== "string" || testCase.skill.trim().length === 0) {
      errors.push(`${label}.skill must be a non-empty string`);
    } else if (!existsSync(join(root, "plugins/dev-core/skills", testCase.skill, "SKILL.md"))) {
      errors.push(`${label}.skill references missing skill ${testCase.skill}`);
    }
    if (typeof testCase.prompt !== "string" || testCase.prompt.trim().length === 0) errors.push(`${label}.prompt must be non-empty`);
    if (typeof testCase.shouldTrigger !== "boolean") errors.push(`${label}.shouldTrigger must be boolean`);
    if (!nonEmptyStrings(testCase.expectedBehaviors)) errors.push(`${label}.expectedBehaviors must be a non-empty string array`);
    if (!nonEmptyStrings(testCase.forbiddenBehaviors)) errors.push(`${label}.forbiddenBehaviors must be a non-empty string array`);
  }

  const grillCases = suite.cases.filter((testCase) => testCase?.skill === "dev-grill");
  if (!grillCases.some((testCase) => testCase.shouldTrigger === true)) errors.push("dev-grill requires a positive trigger case");
  if (!grillCases.some((testCase) => testCase.shouldTrigger === false)) errors.push("dev-grill requires a negative trigger case");
  for (const requiredSkill of ["dev-task", "dev-execute"]) {
    if (!suite.cases.some((testCase) => testCase?.skill === requiredSkill && testCase.shouldTrigger === true)) {
      errors.push(`${requiredSkill} requires a positive behavior case`);
    }
  }
}

if (errors.length > 0) {
  console.error(errors.join("\n"));
  process.exit(1);
}

console.log(`Skill eval validation passed (${suite.cases.length} cases).`);
