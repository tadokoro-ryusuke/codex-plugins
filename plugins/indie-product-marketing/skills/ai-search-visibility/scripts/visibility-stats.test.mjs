import assert from "node:assert/strict";
import { execFileSync, spawnSync } from "node:child_process";
import { mkdtempSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join } from "node:path";
import { test } from "node:test";
import { fileURLToPath } from "node:url";

import { compare, parseObservations, summarize, tCritical, wilsonInterval } from "./visibility-stats.mjs";

const scriptPath = join(dirname(fileURLToPath(import.meta.url)), "visibility-stats.mjs");

let sequence = 0;

/** Build one row per answered run: `hits` of `runs` runs mention the brand. */
function runs({ snapshot = "base", engine = "chatgpt", surface = "product", prompt, question, branded = false, hits, runs: total, cited = 0 }) {
  return Array.from({ length: total }, (_, i) => {
    sequence += 1;
    const row = {
      snapshot,
      engine,
      surface,
      prompt_id: prompt,
      run_id: `r${sequence}`,
      branded,
      mentioned: i < hits,
      cited: i < cited,
    };
    if (question) row.question_id = question;
    return row;
  });
}

/** Round-trip through the parser so tests exercise validation and defaults. */
function parsed(rows) {
  return parseObservations(JSON.stringify(rows));
}

function near(actual, expected, tolerance = 1e-3) {
  assert.ok(Math.abs(actual - expected) <= tolerance, `expected ${actual} to be within ${tolerance} of ${expected}`);
}

test("tCritical returns two-sided 95% Student t quantiles", () => {
  near(tCritical(1), 12.706);
  near(tCritical(4), 2.776);
  near(tCritical(9), 2.262);
  near(tCritical(29), 2.045);
  near(tCritical(60), 2.0, 5e-3);
  near(tCritical(1000), 1.962, 2e-3);
  assert.throws(() => tCritical(0), /degrees of freedom/);
});

test("wilsonInterval bounds a zero count away from a zero-width interval", () => {
  const zero = wilsonInterval(0, 20);
  assert.equal(zero.low, 0);
  near(zero.high, 0.1611);
  const all = wilsonInterval(20, 20);
  near(all.low, 0.8389);
  assert.equal(all.high, 1);
  const half = wilsonInterval(10, 20);
  near(half.low, 0.2993);
  near(half.high, 0.7007);
});

test("summarize weights questions equally and uses the spread between them", () => {
  const rows = parsed([
    ...runs({ prompt: "p1", hits: 2, runs: 10 }),
    ...runs({ prompt: "p2", hits: 4, runs: 10 }),
    ...runs({ prompt: "p3", hits: 4, runs: 10 }),
    ...runs({ prompt: "p4", hits: 6, runs: 10 }),
    ...runs({ prompt: "p5", hits: 4, runs: 10 }),
  ]);
  const [group] = summarize(rows);
  assert.equal(group.snapshot, "base");
  assert.equal(group.engine, "chatgpt");
  assert.equal(group.surface, "product");
  assert.equal(group.branded, false);
  assert.equal(group.questions, 5);
  assert.equal(group.prompts, 5);
  assert.deepEqual(group.runs, { answered: 50, noAnswer: 0, error: 0 });
  assert.deepEqual(group.answeredRunsPerQuestion, { min: 10, max: 10 });
  near(group.mention.rate, 0.4);
  near(group.mention.pooledRate, 0.4);
  assert.equal(group.mention.method, "t-across-questions");
  near(group.mention.low, 0.2244);
  near(group.mention.high, 0.5756);
  assert.equal(group.mention.hits, 20);
  assert.equal(group.mention.runs, 50);
});

test("summarize reports the per-question mean and the pooled rate when run counts differ", () => {
  const rows = parsed([...runs({ prompt: "p1", hits: 1, runs: 1 }), ...runs({ prompt: "p2", hits: 0, runs: 9 })]);
  const [group] = summarize(rows);
  near(group.mention.rate, 0.5);
  near(group.mention.pooledRate, 0.1);
  assert.equal(group.mention.hits, 1);
  assert.equal(group.mention.runs, 10);
  assert.deepEqual(group.answeredRunsPerQuestion, { min: 1, max: 9 });
});

test("summarize treats prompt variants of one question as a single unit", () => {
  const rows = parsed([
    ...runs({ prompt: "p1a", question: "q1", hits: 4, runs: 5 }),
    ...runs({ prompt: "p1b", question: "q1", hits: 2, runs: 5 }),
    ...runs({ prompt: "p2", question: "q2", hits: 2, runs: 10 }),
  ]);
  const [group] = summarize(rows);
  assert.equal(group.questions, 2);
  assert.equal(group.prompts, 3);
  near(group.mention.rate, 0.4); // q1 6/10, q2 2/10
});

test("summarize clamps the interval to the 0..1 range", () => {
  const rows = parsed([
    ...runs({ prompt: "p1", hits: 0, runs: 4 }),
    ...runs({ prompt: "p2", hits: 2, runs: 4 }),
    ...runs({ prompt: "p3", hits: 2, runs: 4 }),
    ...runs({ prompt: "p4", hits: 4, runs: 4 }),
  ]);
  const [group] = summarize(rows);
  near(group.mention.rate, 0.5);
  assert.equal(group.mention.low, 0);
  assert.equal(group.mention.high, 1);
});

test("summarize does not report a zero-width interval when nothing was mentioned", () => {
  const rows = [];
  for (let i = 0; i < 20; i += 1) rows.push(...runs({ prompt: `p${i}`, hits: 0, runs: 10 }));
  const [group] = summarize(parsed(rows));
  assert.equal(group.mention.rate, 0);
  assert.equal(group.mention.hits, 0);
  assert.equal(group.mention.method, "bound-from-question-count");
  assert.equal(group.mention.low, 0);
  near(group.mention.high, 0.1611);
  assert.match(group.mention.note, /counts/);
  assert.match(group.mention.note, /not how many runs/);
  assert.equal(group.mention.questionsWithHit, 0);
});

test("summarize gives no interval when every question has the same fractional rate", () => {
  const rows = ["p1", "p2", "p3"].flatMap((prompt) => runs({ prompt, hits: 1, runs: 10 }));
  const [group] = summarize(parsed(rows));
  near(group.mention.rate, 0.1);
  assert.equal(group.mention.method, "none");
  assert.equal(group.mention.low, null);
  assert.match(group.mention.note, /Add questions or runs/);
});

test("summarize reports no interval for a single question", () => {
  const [group] = summarize(parsed(runs({ prompt: "only", hits: 3, runs: 10 })));
  near(group.mention.rate, 0.3);
  assert.equal(group.mention.low, null);
  assert.equal(group.mention.high, null);
  assert.equal(group.mention.method, "none");
  assert.match(group.mention.note, /at least 2 questions/);
});

test("summarize keeps branded prompts, engines, surfaces, and citation separate", () => {
  const rows = parsed([
    ...runs({ prompt: "p1", hits: 1, runs: 4, cited: 0 }),
    ...runs({ prompt: "p2", hits: 3, runs: 4, cited: 2 }),
    ...runs({ prompt: "b1", branded: true, hits: 4, runs: 4, cited: 4 }),
    ...runs({ prompt: "b2", branded: true, hits: 4, runs: 4, cited: 2 }),
    ...runs({ engine: "perplexity", prompt: "p1", hits: 0, runs: 4 }),
    ...runs({ engine: "perplexity", prompt: "p2", hits: 2, runs: 4 }),
    ...runs({ surface: "api", prompt: "p1", hits: 4, runs: 4 }),
    ...runs({ surface: "api", prompt: "p2", hits: 4, runs: 4 }),
  ]);
  const groups = summarize(rows);
  assert.equal(groups.length, 4);
  const unbranded = groups.find((g) => g.engine === "chatgpt" && g.surface === "product" && !g.branded);
  const branded = groups.find((g) => g.engine === "chatgpt" && g.branded);
  const perplexity = groups.find((g) => g.engine === "perplexity");
  const api = groups.find((g) => g.surface === "api");
  near(unbranded.mention.rate, 0.5);
  near(unbranded.citation.rate, 0.25);
  near(branded.mention.rate, 1);
  assert.equal(branded.mention.method, "bound-from-question-count");
  near(branded.citation.rate, 0.75);
  near(perplexity.mention.rate, 0.25);
  near(api.mention.rate, 1);
});

test("summarize keeps failed and answerless runs out of the rate and counts them", () => {
  const rows = parsed([
    ...runs({ prompt: "p1", hits: 1, runs: 2 }),
    ...runs({ prompt: "p2", hits: 0, runs: 2 }),
    { snapshot: "base", engine: "chatgpt", surface: "product", prompt_id: "p1", run_id: "x1", branded: false, status: "no_answer" },
    { snapshot: "base", engine: "chatgpt", surface: "product", prompt_id: "p2", run_id: "x2", branded: false, status: "error" },
    { snapshot: "base", engine: "chatgpt", surface: "product", prompt_id: "p3", run_id: "x3", branded: false, status: "no_answer" },
  ]);
  const [group] = summarize(rows);
  assert.deepEqual(group.runs, { answered: 4, noAnswer: 2, error: 1 });
  assert.equal(group.questions, 2);
  assert.equal(group.questionsWithoutAnswer, 1);
  near(group.mention.rate, 0.25);
});

test("summarize counts runs that cite the product's page without naming the product", () => {
  const base = { snapshot: "base", engine: "chatgpt", surface: "product", branded: false };
  const rows = parsed([
    { ...base, prompt_id: "p1", run_id: "a", mentioned: false, cited: true },
    { ...base, prompt_id: "p1", run_id: "b", mentioned: true, cited: true },
    { ...base, prompt_id: "p2", run_id: "c", mentioned: false, cited: false },
  ]);
  const [group] = summarize(rows);
  assert.equal(group.citedWithoutMention, 1);
});

test("compare reports a change whose interval excludes zero", () => {
  const before = [1, 2, 3, 2, 1, 3];
  const after = [3, 5, 5, 5, 3, 6];
  const rows = [];
  before.forEach((hits, i) => rows.push(...runs({ snapshot: "a", prompt: `p${i}`, hits, runs: 10 })));
  after.forEach((hits, i) => rows.push(...runs({ snapshot: "b", prompt: `p${i}`, hits, runs: 10 })));
  const [result] = compare(parsed(rows), { from: "a", to: "b" });
  assert.equal(result.comparable, true);
  assert.equal(result.pairedQuestions, 6);
  near(result.mention.from, 0.2);
  near(result.mention.to, 0.45);
  near(result.mention.difference, 0.25);
  // differences: .2 .3 .2 .3 .2 .3 -> sd 0.05477, se 0.02236, t(5) 2.571
  near(result.mention.low, 0.1925);
  near(result.mention.high, 0.3075);
  assert.equal(result.mention.verdict, "increase (interval excludes zero)");
  assert.equal(result.mention.baselineZero, false);
  assert.equal(result.mention.hitsFrom, 12);
  assert.equal(result.mention.runsFrom, 60);
  assert.equal(result.mention.hitsTo, 27);
  assert.equal(result.mention.runsTo, 60);
});

test("compare calls a move the interval does not separate from zero inconclusive", () => {
  const before = [2, 5, 3, 6, 4];
  const after = [4, 4, 5, 5, 3];
  const rows = [];
  before.forEach((hits, i) => rows.push(...runs({ snapshot: "a", prompt: `p${i}`, hits, runs: 10 })));
  after.forEach((hits, i) => rows.push(...runs({ snapshot: "b", prompt: `p${i}`, hits, runs: 10 })));
  const [result] = compare(parsed(rows), { from: "a", to: "b" });
  near(result.mention.difference, 0.02);
  assert.ok(result.mention.low < 0 && result.mention.high > 0);
  assert.equal(result.mention.verdict, "inconclusive");
});

test("compare gives no directional verdict when every question moved by the same amount", () => {
  const rows = parsed([
    ...runs({ snapshot: "a", prompt: "p1", hits: 0, runs: 1 }),
    ...runs({ snapshot: "a", prompt: "p2", hits: 0, runs: 1 }),
    ...runs({ snapshot: "b", prompt: "p1", hits: 1, runs: 1 }),
    ...runs({ snapshot: "b", prompt: "p2", hits: 1, runs: 1 }),
  ]);
  const [result] = compare(rows, { from: "a", to: "b" });
  near(result.mention.difference, 1);
  assert.equal(result.mention.low, null);
  assert.equal(result.mention.verdict, "no interval");
  assert.match(result.mention.note, /same amount/);
});

test("compare keeps the difference interval inside the possible range", () => {
  const rows = parsed([
    ...runs({ snapshot: "a", prompt: "p1", hits: 0, runs: 1 }),
    ...runs({ snapshot: "a", prompt: "p2", hits: 1, runs: 1 }),
    ...runs({ snapshot: "b", prompt: "p1", hits: 1, runs: 1 }),
    ...runs({ snapshot: "b", prompt: "p2", hits: 0, runs: 1 }),
  ]);
  const [result] = compare(rows, { from: "a", to: "b" });
  assert.equal(result.mention.low, -1);
  assert.equal(result.mention.high, 1);
  assert.equal(result.mention.verdict, "inconclusive");
  assert.match(result.mention.note, /whole possible range/);
});

test("compare reports first appearances instead of a ratio when the baseline is zero", () => {
  const rows = [];
  for (let i = 0; i < 8; i += 1) rows.push(...runs({ snapshot: "a", prompt: `p${i}`, hits: 0, runs: 10 }));
  for (let i = 0; i < 8; i += 1) rows.push(...runs({ snapshot: "b", prompt: `p${i}`, hits: i < 2 ? 3 : 0, runs: 10 }));
  const [result] = compare(parsed(rows), { from: "a", to: "b" });
  assert.equal(result.mention.baselineZero, true);
  assert.equal(result.mention.newlyAppearing, 2);
  assert.equal(result.mention.disappeared, 0);
  assert.equal(result.mention.hitsFrom, 0);
  assert.equal(result.mention.hitsTo, 6);
  assert.ok(!("relativeChange" in result.mention));
  assert.match(result.mention.note, /counts/);
});

test("compare reports no change when every question is identical in both snapshots", () => {
  const rows = [];
  for (let i = 0; i < 5; i += 1) {
    rows.push(...runs({ snapshot: "a", prompt: `p${i}`, hits: 0, runs: 5 }));
    rows.push(...runs({ snapshot: "b", prompt: `p${i}`, hits: 0, runs: 5 }));
  }
  const [result] = compare(parsed(rows), { from: "a", to: "b" });
  assert.equal(result.mention.difference, 0);
  assert.equal(result.mention.verdict, "no change observed");
  assert.equal(result.mention.low, null);
});

test("compare pairs only questions present in both snapshots and lists the rest", () => {
  const rows = parsed([
    ...runs({ snapshot: "a", prompt: "p1", hits: 1, runs: 4 }),
    ...runs({ snapshot: "a", prompt: "p2", hits: 2, runs: 4 }),
    ...runs({ snapshot: "a", prompt: "old", hits: 4, runs: 4 }),
    ...runs({ snapshot: "b", prompt: "p1", hits: 2, runs: 4 }),
    ...runs({ snapshot: "b", prompt: "p2", hits: 2, runs: 4 }),
    ...runs({ snapshot: "b", prompt: "new", hits: 4, runs: 4 }),
  ]);
  const [result] = compare(rows, { from: "a", to: "b" });
  assert.equal(result.pairedQuestions, 2);
  assert.deepEqual(result.onlyInFrom, ["old"]);
  assert.deepEqual(result.onlyInTo, ["new"]);
  near(result.mention.from, 0.375);
  near(result.mention.to, 0.5);
});

test("compare reports groups that exist in only one snapshot instead of dropping them", () => {
  const rows = parsed([
    ...runs({ snapshot: "a", engine: "chatgpt", surface: "api", prompt: "p1", hits: 1, runs: 2 }),
    ...runs({ snapshot: "a", engine: "chatgpt", surface: "api", prompt: "p2", hits: 1, runs: 2 }),
    ...runs({ snapshot: "b", engine: "chatgpt", surface: "product", prompt: "p1", hits: 2, runs: 2 }),
    ...runs({ snapshot: "b", engine: "chatgpt", surface: "product", prompt: "p2", hits: 2, runs: 2 }),
  ]);
  const results = compare(rows, { from: "a", to: "b" });
  assert.equal(results.length, 2);
  assert.ok(results.every((result) => result.comparable === false));
  assert.match(results.find((r) => r.surface === "api").reason, /only in "a"/);
  assert.match(results.find((r) => r.surface === "product").reason, /only in "b"/);
});

test("compare rejects an unknown snapshot label", () => {
  const rows = parsed(runs({ snapshot: "a", prompt: "p1", hits: 1, runs: 4 }));
  assert.throws(() => compare(rows, { from: "a", to: "missing" }), /snapshot "missing"/);
});

test("parseObservations accepts a JSON array or JSON Lines and validates rows", () => {
  const row = { snapshot: "a", engine: "chatgpt", surface: "product", prompt_id: "p1", run_id: "1", branded: false, mentioned: true, cited: false };
  const second = { ...row, run_id: "2" };
  assert.equal(parseObservations(JSON.stringify([row, second])).length, 2);
  assert.equal(parseObservations(`${JSON.stringify(row)}\n\n${JSON.stringify(second)}\n`).length, 2);
  const [first] = parseObservations(JSON.stringify([row]));
  assert.equal(first.question_id, "p1");
  assert.equal(first.status, "answered");
  assert.throws(() => parseObservations(JSON.stringify([{ ...row, mentioned: "yes" }])), /row 1: mentioned must be true or false/);
  assert.throws(() => parseObservations(JSON.stringify([{ ...row, prompt_id: "" }])), /row 1: prompt_id/);
  assert.throws(() => parseObservations(JSON.stringify([{ ...row, surface: undefined }])), /row 1: surface/);
  assert.throws(() => parseObservations(JSON.stringify([{ ...row, status: "maybe" }])), /row 1: status/);
  assert.throws(() => parseObservations("[]"), /no observations/);
});

test("parseObservations fails closed on a missing branded flag, a duplicate run, or a prompt that changes stratum", () => {
  const row = { snapshot: "a", engine: "chatgpt", surface: "product", prompt_id: "p1", run_id: "1", branded: false, mentioned: true, cited: false };
  const { branded, ...withoutFlag } = row;
  assert.throws(() => parseObservations(JSON.stringify([withoutFlag])), /row 1: branded must be true or false/);
  assert.throws(() => parseObservations(JSON.stringify([row, row])), /row 2: duplicate run_id "1"/);
  assert.throws(
    () => parseObservations(JSON.stringify([row, { ...row, run_id: "2", branded: true }])),
    /row 2: prompt "p1" is branded in one row and unbranded in another/,
  );
  assert.throws(
    () => parseObservations(JSON.stringify([row, { ...row, run_id: "2", question_id: "other" }])),
    /row 2: prompt "p1" belongs to more than one question_id/,
  );
});

test("the CLI prints tables with counts and JSON, and exits non-zero on bad input", () => {
  const dir = mkdtempSync(join(tmpdir(), "visibility-stats-"));
  try {
    const file = join(dir, "runs.json");
    const rows = [];
    [2, 4, 4, 6, 4].forEach((hits, i) => rows.push(...runs({ snapshot: "a", prompt: `p${i}`, hits, runs: 10 })));
    [4, 6, 5, 8, 6].forEach((hits, i) => rows.push(...runs({ snapshot: "b", prompt: `p${i}`, hits, runs: 10 })));
    writeFileSync(file, JSON.stringify(rows));

    const table = execFileSync("node", [scriptPath, "summarize", file], { encoding: "utf8" });
    assert.match(table, /\| a \| chatgpt \| product \| no \| 5 \| 50 \|/);
    assert.match(table, /40\.0% \(22\.4%–57\.6%\); 20\/50 runs, 5 questions with a hit/);

    const comparison = execFileSync("node", [scriptPath, "compare", file, "--from", "a", "--to", "b"], { encoding: "utf8" });
    assert.match(comparison, /hits 20\/50 → 29\/50/);
    assert.match(comparison, /single comparison is not a decision/);

    const json = JSON.parse(execFileSync("node", [scriptPath, "compare", file, "--from", "a", "--to", "b", "--json"], { encoding: "utf8" }));
    assert.equal(json[0].mention.verdict, "increase (interval excludes zero)");

    const missing = spawnSync("node", [scriptPath, "compare", file, "--from", "a"], { encoding: "utf8" });
    assert.equal(missing.status, 2);
    assert.match(missing.stderr, /--to/);

    const bad = join(dir, "bad.json");
    writeFileSync(bad, "{not json");
    const failed = spawnSync("node", [scriptPath, "summarize", bad], { encoding: "utf8" });
    assert.equal(failed.status, 1);
    assert.match(failed.stderr, /could not parse/);
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});
