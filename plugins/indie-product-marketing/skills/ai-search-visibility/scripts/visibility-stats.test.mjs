import assert from "node:assert/strict";
import { execFileSync, spawnSync } from "node:child_process";
import { mkdtempSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join } from "node:path";
import { test } from "node:test";
import { fileURLToPath } from "node:url";

import { compare, parseObservations, summarize } from "./visibility-stats.mjs";

const scriptPath = join(dirname(fileURLToPath(import.meta.url)), "visibility-stats.mjs");

let sequence = 0;

/** Build one row per answered run: `hits` of `runs` runs mention the brand, `cited` of them cite its page. */
function runs({ snapshot = "base", engine = "chatgpt", surface = "product", prompt, question, branded = false, hits, runs: total, cited = 0 }) {
  return Array.from({ length: total }, (_, i) => {
    sequence += 1;
    const row = { snapshot, engine, surface, prompt_id: prompt, run_id: `r${sequence}`, branded, mentioned: i < hits, cited: i < cited };
    if (question) row.question_id = question;
    return row;
  });
}

/** One unanswered run. */
function unanswered({ snapshot = "base", prompt, question, status = "error" }) {
  sequence += 1;
  const row = { snapshot, engine: "chatgpt", surface: "product", prompt_id: prompt, run_id: `r${sequence}`, branded: false, status };
  if (question) row.question_id = question;
  return row;
}

function near(actual, expected, tolerance = 1e-9) {
  assert.ok(Number.isFinite(actual), `expected a finite number, got ${actual}`);
  assert.ok(Math.abs(actual - expected) <= tolerance, `expected ${actual} to be within ${tolerance} of ${expected}`);
}

test("summarize reports counts, a pooled rate, and a rate that weights questions equally", () => {
  const rows = [
    ...runs({ prompt: "p1", hits: 2, runs: 10, cited: 1 }),
    ...runs({ prompt: "p2", hits: 4, runs: 10 }),
    ...runs({ prompt: "p3", hits: 0, runs: 10 }),
    ...runs({ prompt: "p4", hits: 6, runs: 10 }),
    ...runs({ prompt: "p5", hits: 4, runs: 10 }),
  ];
  const [group] = summarize(rows);
  assert.equal(group.snapshot, "base");
  assert.equal(group.engine, "chatgpt");
  assert.equal(group.surface, "product");
  assert.equal(group.branded, false);
  assert.deepEqual(group.questions, { recorded: 5, complete: 5, incomplete: [] });
  assert.deepEqual(group.prompts, { recorded: 5, answered: 5 });
  assert.deepEqual(group.runs, { answered: 50, noAnswer: 0, error: 0 });
  assert.deepEqual(group.answeredRunsPerPrompt, { min: 10, max: 10 });
  assert.equal(group.mention.hits, 16);
  assert.equal(group.mention.runs, 50);
  near(group.mention.pooledRate, 0.32);
  near(group.mention.questionRate, 0.32);
  assert.equal(group.mention.questionsWithHit, 4);
  assert.equal(group.citation.hits, 1);
  near(group.citation.questionRate, 0.02);
  assert.equal(group.citation.questionsWithHit, 1);
  assert.ok(!("low" in group.mention) && !("verdict" in group.mention));
});

test("the two rates differ when answered runs carry unequal weight, and the output says so", () => {
  const [unequalRuns] = summarize([...runs({ prompt: "p1", hits: 1, runs: 1 }), ...runs({ prompt: "p2", hits: 0, runs: 9 })]);
  near(unequalRuns.mention.questionRate, 0.5);
  near(unequalRuns.mention.pooledRate, 0.1);
  assert.equal(unequalRuns.equalWeightPerRun, false);

  const [unequalVariants] = summarize([
    ...runs({ prompt: "a1", question: "qa", hits: 0, runs: 10 }),
    ...runs({ prompt: "a2", question: "qa", hits: 0, runs: 10 }),
    ...runs({ prompt: "b1", question: "qb", hits: 10, runs: 10 }),
  ]);
  near(unequalVariants.mention.questionRate, 0.5);
  near(unequalVariants.mention.pooledRate, 1 / 3);
  assert.equal(unequalVariants.equalWeightPerRun, false);
  assert.ok(unequalVariants.notes.some((note) => /do not all carry the same weight/.test(note)));

  const [balanced] = summarize([...runs({ prompt: "p1", hits: 1, runs: 5 }), ...runs({ prompt: "p2", hits: 0, runs: 5 })]);
  assert.equal(balanced.equalWeightPerRun, true);
  assert.deepEqual(balanced.notes, []);
});

test("summarize weights the variants of one question equally, whatever their run counts", () => {
  const [group] = summarize([
    ...runs({ prompt: "p1a", question: "q1", hits: 8, runs: 8 }),
    ...runs({ prompt: "p1b", question: "q1", hits: 0, runs: 2 }),
    ...runs({ prompt: "p2", question: "q2", hits: 2, runs: 10 }),
  ]);
  assert.deepEqual(group.questions, { recorded: 2, complete: 2, incomplete: [] });
  near(group.mention.questionRate, 0.35); // q1 = mean(1, 0) = 0.5, q2 = 0.2
  near(group.mention.pooledRate, 0.5);
});

test("summarize returns exactly 0 and exactly 1 at the boundaries", () => {
  const all = [];
  const none = [];
  for (let i = 0; i < 6; i += 1) {
    all.push(...runs({ snapshot: "all", prompt: `p${i}`, hits: 2, runs: 2 }));
    none.push(...runs({ snapshot: "none", prompt: `p${i}`, hits: 0, runs: 2 }));
  }
  const groups = summarize([...all, ...none]);
  assert.equal(groups.find((g) => g.snapshot === "all").mention.questionRate, 1);
  assert.equal(groups.find((g) => g.snapshot === "none").mention.questionRate, 0);
});

test("summarize leaves a question out of the equal-weight rate when one of its variants never got an answer", () => {
  const [group] = summarize([
    ...runs({ prompt: "p1a", question: "q1", hits: 5, runs: 5 }),
    unanswered({ prompt: "p1b", question: "q1" }),
    ...runs({ prompt: "p2", question: "q2", hits: 0, runs: 5 }),
    unanswered({ prompt: "p3", status: "no_answer" }),
  ]);
  assert.deepEqual(group.questions, { recorded: 3, complete: 1, incomplete: ["q1", "p3"] });
  assert.deepEqual(group.prompts, { recorded: 4, answered: 2 });
  assert.deepEqual(group.runs, { answered: 10, noAnswer: 1, error: 1 });
  near(group.mention.questionRate, 0); // only q2 is complete
  near(group.mention.pooledRate, 0.5); // every answered run
  assert.equal(group.mention.questionsWithHit, 1);
  assert.ok(group.notes.some((note) => /left out of the by-question rate/.test(note)));
});

test("summarize reports no rate when nothing was answered", () => {
  const [group] = summarize([unanswered({ prompt: "p1" }), unanswered({ prompt: "p2", status: "no_answer" })]);
  assert.equal(group.mention.questionRate, null);
  assert.equal(group.mention.pooledRate, null);
  assert.deepEqual(group.runs, { answered: 0, noAnswer: 1, error: 1 });
});

test("summarize keeps branded prompts, engines, surfaces, and citation separate", () => {
  const groups = summarize([
    ...runs({ prompt: "p1", hits: 1, runs: 4, cited: 0 }),
    ...runs({ prompt: "p2", hits: 3, runs: 4, cited: 2 }),
    ...runs({ prompt: "b1", branded: true, hits: 4, runs: 4, cited: 4 }),
    ...runs({ prompt: "b2", branded: true, hits: 4, runs: 4, cited: 2 }),
    ...runs({ engine: "perplexity", prompt: "p1", hits: 0, runs: 4 }),
    ...runs({ engine: "perplexity", prompt: "p2", hits: 2, runs: 4 }),
    ...runs({ surface: "api", prompt: "p1", hits: 4, runs: 4 }),
    ...runs({ surface: "api", prompt: "p2", hits: 4, runs: 4 }),
  ]);
  assert.equal(groups.length, 4);
  const unbranded = groups.find((g) => g.engine === "chatgpt" && g.surface === "product" && !g.branded);
  const branded = groups.find((g) => g.engine === "chatgpt" && g.branded);
  near(unbranded.mention.questionRate, 0.5);
  near(unbranded.citation.questionRate, 0.25);
  near(branded.mention.questionRate, 1);
  near(branded.citation.questionRate, 0.75);
  near(groups.find((g) => g.engine === "perplexity").mention.questionRate, 0.25);
  near(groups.find((g) => g.surface === "api").mention.questionRate, 1);
});

test("summarize counts runs that cite the product's page without naming the product", () => {
  const base = { snapshot: "base", engine: "chatgpt", surface: "product", branded: false };
  const [group] = summarize([
    { ...base, prompt_id: "p1", run_id: "a", mentioned: false, cited: true },
    { ...base, prompt_id: "p1", run_id: "b", mentioned: true, cited: true },
    { ...base, prompt_id: "p2", run_id: "c", mentioned: false, cited: false },
  ]);
  assert.equal(group.citedWithoutMention, 1);
});

test("summarize and compare handle large inputs", () => {
  const rows = [];
  for (let i = 0; i < 160_000; i += 1) {
    rows.push({ snapshot: "s", engine: "e", surface: "api", prompt_id: `p${i}`, run_id: `r${i}`, branded: false, mentioned: i % 4 === 0, cited: false });
  }
  const [group] = summarize(rows);
  assert.equal(group.questions.complete, 160_000);
  near(group.mention.questionRate, 0.25);

  const variants = [];
  for (const snapshot of ["a", "b"]) {
    for (let i = 0; i < 20_000; i += 1) {
      variants.push({ snapshot, engine: "e", surface: "api", prompt_id: `v${i}`, question_id: "q", run_id: `${snapshot}${i}`, branded: false, mentioned: false, cited: false });
    }
  }
  const started = Date.now();
  const [result] = compare(variants, { from: "a", to: "b" });
  assert.equal(result.pairedQuestions, 1);
  assert.ok(Date.now() - started < 5000);
});

test("compare reports mention and citation changes separately, on the paired questions only", () => {
  const rows = [];
  const before = [[1, 10, 6], [2, 8, 5], [3, 10, 6], [2, 6, 4], [1, 10, 5], [3, 8, 5]];
  const after = [[4, 10, 1], [5, 10, 2], [5, 8, 1], [5, 10, 2], [3, 6, 1], [6, 10, 2]];
  before.forEach(([hits, total, cited], i) => rows.push(...runs({ snapshot: "a", prompt: `p${i}`, hits, runs: total, cited })));
  after.forEach(([hits, total, cited], i) => rows.push(...runs({ snapshot: "b", prompt: `p${i}`, hits, runs: total, cited })));
  const [result] = compare(rows, { from: "a", to: "b" });
  assert.equal(result.comparable, true);
  assert.equal(result.pairedQuestions, 6);
  const meanRate = (list, index) => list.reduce((sum, item) => sum + item[index] / item[1], 0) / list.length;
  near(result.mention.from, meanRate(before, 0));
  near(result.mention.to, meanRate(after, 0));
  near(result.mention.difference, meanRate(after, 0) - meanRate(before, 0));
  assert.deepEqual([result.mention.hitsFrom, result.mention.runsFrom, result.mention.hitsTo, result.mention.runsTo], [12, 52, 28, 54]);
  near(result.citation.from, meanRate(before, 2));
  near(result.citation.to, meanRate(after, 2));
  assert.ok(result.citation.difference < 0 && result.mention.difference > 0);
  assert.deepEqual([result.citation.hitsFrom, result.citation.hitsTo], [31, 9]);
  assert.ok(!("verdict" in result.mention) && !("low" in result.mention));
});

test("compare is not moved by a change in how many times each variant was run", () => {
  const rows = [];
  for (let q = 0; q < 20; q += 1) {
    rows.push(...runs({ snapshot: "a", prompt: `q${q}-hit`, question: `q${q}`, hits: 1, runs: 1 }));
    rows.push(...runs({ snapshot: "a", prompt: `q${q}-miss`, question: `q${q}`, hits: 0, runs: 9 }));
    rows.push(...runs({ snapshot: "b", prompt: `q${q}-hit`, question: `q${q}`, hits: 9, runs: 9 }));
    rows.push(...runs({ snapshot: "b", prompt: `q${q}-miss`, question: `q${q}`, hits: 0, runs: 1 }));
  }
  const [result] = compare(rows, { from: "a", to: "b" });
  near(result.mention.from, 0.5);
  near(result.mention.to, 0.5);
  near(result.mention.difference, 0);
  assert.ok(result.notes.some((note) => /number of answered runs per prompt differs/.test(note)));
});

test("compare leaves out a question whose recorded prompt variants changed, even when the changed variant got no answer", () => {
  const rows = [];
  for (let q = 0; q < 3; q += 1) {
    rows.push(...runs({ snapshot: "a", prompt: `q${q}-old`, question: `q${q}`, hits: 0, runs: 10 }));
    rows.push(...runs({ snapshot: "b", prompt: `q${q}-new`, question: `q${q}`, hits: 5, runs: 10 }));
  }
  rows.push(...runs({ snapshot: "a", prompt: "shared", question: "mixed", hits: 1, runs: 5 }), unanswered({ snapshot: "a", prompt: "old-variant", question: "mixed" }));
  rows.push(...runs({ snapshot: "b", prompt: "shared", question: "mixed", hits: 1, runs: 5 }), unanswered({ snapshot: "b", prompt: "new-variant", question: "mixed" }));
  const [result] = compare(rows, { from: "a", to: "b" });
  assert.equal(result.comparable, false);
  assert.equal(result.pairedQuestions, 0);
  assert.deepEqual(result.excluded.variantsChanged.sort(), ["mixed", "q0", "q1", "q2"]);
  assert.match(result.reason, /no question that can be compared/);
});

test("compare separates missing questions, changed variants, and variants without an answer", () => {
  const rows = [
    ...runs({ snapshot: "a", prompt: "p1", hits: 1, runs: 4 }),
    ...runs({ snapshot: "a", prompt: "p2", hits: 2, runs: 4 }),
    ...runs({ snapshot: "a", prompt: "old", hits: 4, runs: 4 }),
    ...runs({ snapshot: "a", prompt: "flaky", hits: 2, runs: 4 }),
    ...runs({ snapshot: "a", prompt: "va", question: "vq", hits: 2, runs: 4 }),
    ...runs({ snapshot: "a", prompt: "vb", question: "vq", hits: 2, runs: 4 }),
    ...runs({ snapshot: "b", prompt: "p1", hits: 2, runs: 4 }),
    ...runs({ snapshot: "b", prompt: "p2", hits: 2, runs: 4 }),
    ...runs({ snapshot: "b", prompt: "new", hits: 4, runs: 4 }),
    unanswered({ snapshot: "b", prompt: "flaky" }),
    unanswered({ snapshot: "b", prompt: "flaky", status: "no_answer" }),
    ...runs({ snapshot: "b", prompt: "va", question: "vq", hits: 2, runs: 4 }),
    unanswered({ snapshot: "b", prompt: "vb", question: "vq" }),
  ];
  const [result] = compare(rows, { from: "a", to: "b" });
  assert.equal(result.pairedQuestions, 2);
  assert.deepEqual(result.excluded.onlyInFrom, ["old"]);
  assert.deepEqual(result.excluded.onlyInTo, ["new"]);
  assert.deepEqual(result.excluded.variantsChanged, []);
  assert.deepEqual(result.excluded.missingAnswers.sort(), ["flaky", "vq"]);
  assert.deepEqual(result.runsFrom, { answered: 24, noAnswer: 0, error: 0 });
  assert.deepEqual(result.runsTo, { answered: 16, noAnswer: 1, error: 2 });
  near(result.mention.from, 0.375);
  near(result.mention.to, 0.5);
  assert.equal(result.mention.hitsFrom, 3); // only the paired questions
});

test("compare counts questions with hits on one date only and qualifies a zero baseline", () => {
  const rows = [];
  for (let i = 0; i < 8; i += 1) rows.push(...runs({ snapshot: "a", prompt: `p${i}`, hits: 0, runs: 10 }));
  for (let i = 0; i < 8; i += 1) rows.push(...runs({ snapshot: "b", prompt: `p${i}`, hits: i < 2 ? 3 : 0, runs: 10 }));
  rows.push(...runs({ snapshot: "a", prompt: "dropped", hits: 5, runs: 10 }));
  const [result] = compare(rows, { from: "a", to: "b" });
  assert.equal(result.mention.baselineZero, true);
  assert.equal(result.mention.questionsHitOnlyAfter, 2);
  assert.equal(result.mention.questionsHitOnlyBefore, 0);
  assert.deepEqual([result.mention.hitsFrom, result.mention.hitsTo], [0, 6]);
  assert.ok(!("relativeChange" in result.mention));
  assert.match(result.mention.note, /among the paired questions/);
  assert.match(result.mention.note, /counts/);

  const moved = compare(
    [
      ...runs({ snapshot: "c", prompt: "p1", hits: 1, runs: 10 }),
      ...runs({ snapshot: "c", prompt: "p2", hits: 0, runs: 10 }),
      ...runs({ snapshot: "d", prompt: "p1", hits: 0, runs: 10 }),
      ...runs({ snapshot: "d", prompt: "p2", hits: 1, runs: 10 }),
    ],
    { from: "c", to: "d" },
  )[0];
  assert.equal(moved.mention.baselineZero, false);
  assert.equal(moved.mention.questionsHitOnlyAfter, 1);
  assert.equal(moved.mention.questionsHitOnlyBefore, 1);
  near(moved.mention.difference, 0);
});

test("compare keeps the counts of a group that exists in only one snapshot", () => {
  const rows = [
    ...runs({ snapshot: "a", surface: "api", prompt: "p1", hits: 1, runs: 2 }),
    { snapshot: "a", engine: "chatgpt", surface: "api", prompt_id: "p2", run_id: "only-error", branded: false, status: "error" },
    ...runs({ snapshot: "b", surface: "product", prompt: "p1", hits: 2, runs: 2 }),
  ];
  const results = compare(rows, { from: "a", to: "b" });
  assert.equal(results.length, 2);
  assert.ok(results.every((result) => result.comparable === false));
  const api = results.find((r) => r.surface === "api");
  assert.match(api.reason, /only in "a"/);
  assert.deepEqual(api.runsFrom, { answered: 2, noAnswer: 0, error: 1 });
  assert.equal(api.runsTo, null);
  assert.deepEqual(api.excluded.onlyInFrom.sort(), ["p1", "p2"]);
  const product = results.find((r) => r.surface === "product");
  assert.match(product.reason, /only in "b"/);
  assert.deepEqual(product.excluded.onlyInTo, ["p1"]);
});

test("compare rejects an unknown snapshot label and identical labels", () => {
  const rows = runs({ snapshot: "a", prompt: "p1", hits: 1, runs: 4 });
  assert.throws(() => compare(rows, { from: "a", to: "missing" }), /snapshot "missing"/);
  assert.throws(() => compare(rows, { from: "a", to: "a" }), /two different snapshots/);
});

test("parseObservations accepts a JSON array or JSON Lines and applies defaults", () => {
  const row = { snapshot: "a", engine: "chatgpt", surface: "product", prompt_id: "p1", run_id: "1", branded: false, mentioned: true, cited: false };
  const second = { ...row, run_id: "2", note: "extra fields are allowed" };
  assert.equal(parseObservations(JSON.stringify([row, second])).length, 2);
  assert.equal(parseObservations(`${JSON.stringify(row)}\n\n${JSON.stringify(second)}\n`).length, 2);
  const [first] = parseObservations(JSON.stringify([row]));
  assert.equal(first.question_id, "p1");
  assert.equal(first.status, "answered");
  assert.throws(() => parseObservations("[]"), /no observations/);
  assert.throws(() => parseObservations("{not json"), /could not parse/);
});

test("summarize and compare validate raw rows themselves", () => {
  const raw = [
    { snapshot: "a", engine: "e", surface: "api", prompt_id: "p1", run_id: "1", branded: false, mentioned: true, cited: false },
    { snapshot: "a", engine: "e", surface: "api", prompt_id: "p2", run_id: "2", branded: false, mentioned: false, cited: false },
  ];
  assert.equal(summarize(raw)[0].questions.recorded, 2);
  assert.throws(() => summarize([{ ...raw[0], branded: undefined }]), /row 1: branded/);
  assert.throws(() => compare([raw[0], { ...raw[0] }], { from: "a", to: "b" }), /row 2: duplicate run_id/);
});

test("validation fails closed on rows that would skew a rate", () => {
  const row = { snapshot: "a", engine: "chatgpt", surface: "product", prompt_id: "p1", run_id: "1", branded: false, mentioned: true, cited: false };
  const check = (rows, pattern) => assert.throws(() => summarize(rows), pattern);
  const { branded, ...withoutFlag } = row;
  check([withoutFlag], /row 1: branded must be true or false/);
  check([{ ...row, mentioned: "yes" }], /row 1: mentioned must be true or false/);
  check([{ ...row, prompt_id: "" }], /row 1: prompt_id/);
  check([{ ...row, surface: undefined }], /row 1: surface/);
  check([{ ...row, status: "maybe" }], /row 1: status/);
  check([{ ...row, status: null }], /row 1: status/);
  check([{ ...row, run_id: "1 " }], /row 1: run_id must not start or end with whitespace/);
  check([{ ...row, surface: "web\n" }], /row 1: surface/);
  check([{ ...row, snapshot: "a\nb" }], /row 1: snapshot must be a single line/);
  check([{ ...row, surface: "web\u2028app" }], /row 1: surface must be a single line/);
  check([{ ...row, status: "error", mentioned: false, cited: true }], /row 1: cited must be false or absent when status is error/);
  check([{ ...row, status: "no_answer", mentioned: "yes" }], /row 1: mentioned must be false or absent when status is no_answer/);
  check([{ ...row, questionId: "q1" }], /row 1: unknown field "questionId"; did you mean "question_id"/);
  check([{ ...row, Status: "error" }], /row 1: unknown field "Status"; did you mean "status"/);
  check([row, row], /row 2: duplicate run_id "1"/);
  check([row, { ...row, run_id: "2", branded: true }], /row 2: prompt "p1" is branded in one row and unbranded in another/);
  check([row, { ...row, run_id: "2", question_id: "other" }], /row 2: prompt "p1" belongs to more than one question_id/);
});

test("the CLI labels its tables, lists every exclusion, and rejects bad usage", () => {
  const dir = mkdtempSync(join(tmpdir(), "visibility-stats-"));
  try {
    const file = join(dir, "runs.json");
    const rows = [];
    [2, 4, 4, 6, 4].forEach((hits, i) => rows.push(...runs({ snapshot: "a|1", prompt: `p${i}`, hits, runs: 10 })));
    [4, 6, 5, 8, 6].forEach((hits, i) => rows.push(...runs({ snapshot: "--b", prompt: `p${i}`, hits, runs: 10 })));
    for (let i = 0; i < 12; i += 1) rows.push(...runs({ snapshot: "a|1", prompt: `gone${i}`, hits: 0, runs: 10 }));
    writeFileSync(file, JSON.stringify(rows));
    const run = (...args) => execFileSync("node", [scriptPath, ...args], { encoding: "utf8" });

    const table = run("summarize", file);
    assert.match(table, /observed counts and rates/);
    assert.match(table, /\| --b \| chatgpt \| product \| no \| 5 \| 50 \|/);
    assert.match(table, /\| a\\\|1 \| chatgpt \| product \| no \| 17 \| 170 \|/);
    assert.match(table, /58\.0% by question, 29\/50 runs \(58\.0%\), 5 of 5 questions with a hit/);
    assert.doesNotMatch(table, /95%|interval/);

    const comparison = run("compare", file, "--from", "a|1", "--to=--b");
    assert.match(comparison, /Comparing "a\\\|1" \(before\) with "--b" \(after\)/);
    assert.match(comparison, /40\.0% → 58\.0% by question \(\+18\.0 pt\), hits 20\/50 → 29\/50/);
    assert.match(comparison, /left out 12 questions recorded only in "a\\\|1": gone0, gone1, .*gone11\./);
    assert.match(comparison, /do not show whether a difference is larger than run-to-run noise/);
    assert.doesNotMatch(comparison, /95%|interval excludes|increase \(|decrease \(/);

    const json = JSON.parse(run("compare", file, "--from", "a|1", "--to=--b", "--json"));
    assert.equal(json[0].pairedQuestions, 5);
    assert.equal(json[0].excluded.onlyInFrom.length, 12);

    const usage = (...args) => spawnSync("node", [scriptPath, ...args], { encoding: "utf8" });
    assert.equal(usage("compare", file, "--from", "a|1").status, 2);
    assert.equal(usage("compare", file, "--from", "--b", "--to", "--b").status, 2);
    assert.equal(usage("compare", file, "--from=a|1", "--to=a|1").status, 2);
    assert.equal(usage("compare", file, "--from", "a|1", "--from", "x", "--to", "y").status, 2);
    assert.equal(usage("summarize", file, "--from", "x").status, 2);
    assert.equal(usage("summarize", "--json").status, 2);
    assert.equal(usage("summarize").status, 2);
    assert.match(usage("compare", file, "--from", "a|1").stderr, /--to/);

    const bad = join(dir, "bad.json");
    writeFileSync(bad, "{not json");
    const failed = usage("summarize", bad);
    assert.equal(failed.status, 1);
    assert.match(failed.stderr, /could not parse/);
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});
