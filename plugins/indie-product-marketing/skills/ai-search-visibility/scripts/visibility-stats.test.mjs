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
function unanswered({ snapshot = "base", surface = "product", prompt, question, status = "error" }) {
  sequence += 1;
  const row = { snapshot, engine: "chatgpt", surface, prompt_id: prompt, run_id: `r${sequence}`, branded: false, status };
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
  assert.deepEqual(group.answeredRunsPerRecordedPrompt, { min: 10, max: 10 });
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

  // One variant answered twice and two variants answered once each: every run has the same weight.
  const [alsoBalanced] = summarize([
    ...runs({ prompt: "s1", question: "single", hits: 1, runs: 2 }),
    ...runs({ prompt: "d1", question: "double", hits: 0, runs: 1 }),
    ...runs({ prompt: "d2", question: "double", hits: 1, runs: 1 }),
  ]);
  assert.equal(alsoBalanced.equalWeightPerRun, true);
  near(alsoBalanced.mention.questionRate, alsoBalanced.mention.pooledRate);
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

test("summarize leaves a question out of the by-question rate when one of its variants never got an answer", () => {
  const [group] = summarize([
    ...runs({ prompt: "p1a", question: "q1", hits: 5, runs: 5 }),
    unanswered({ prompt: "p1b", question: "q1" }),
    ...runs({ prompt: "p2", hits: 0, runs: 5 }),
    unanswered({ prompt: "p3", status: "no_answer" }),
  ]);
  assert.deepEqual(group.questions, { recorded: 3, complete: 1, incomplete: ["q1", "p3"] });
  assert.deepEqual(group.prompts, { recorded: 4, answered: 2 });
  assert.deepEqual(group.runs, { answered: 10, noAnswer: 1, error: 1 });
  assert.deepEqual(group.answeredRunsPerRecordedPrompt, { min: 0, max: 5 });
  near(group.mention.questionRate, 0); // only p2 is complete
  near(group.mention.pooledRate, 0.5); // every answered run
  assert.equal(group.mention.questionsWithHit, 1);
  assert.equal(group.equalWeightPerRun, false); // the pooled rate covers runs the by-question rate leaves out
  assert.ok(group.notes.some((note) => /left out of the by-question rate/.test(note) && /q1, p3/.test(note)));
});

test("summarize reports no rate when nothing was answered", () => {
  const [group] = summarize([unanswered({ prompt: "p1" }), unanswered({ prompt: "p2", status: "no_answer" })]);
  assert.equal(group.mention.questionRate, null);
  assert.equal(group.mention.pooledRate, null);
  assert.equal(group.equalWeightPerRun, null);
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

test("summarize counts runs recorded as citing the product's page without naming the product", () => {
  const base = { snapshot: "base", engine: "chatgpt", surface: "product", branded: false };
  const [group] = summarize([
    { ...base, prompt_id: "p1", run_id: "a", mentioned: false, cited: true },
    { ...base, prompt_id: "p1", run_id: "b", mentioned: true, cited: true },
    { ...base, prompt_id: "p2", run_id: "c", mentioned: false, cited: false },
  ]);
  assert.equal(group.citedWithoutMention, 1);
});

test("summarize keeps raw identifiers in its JSON notes", () => {
  const [group] = summarize([...runs({ prompt: "ok", hits: 0, runs: 2 }), unanswered({ prompt: "a|1" })]);
  assert.deepEqual(group.questions.incomplete, ["a|1"]);
  assert.ok(group.notes.some((note) => note.includes("a|1") && !note.includes("a\\|1")));
});

test("summarize and compare handle large inputs", () => {
  const rows = [];
  for (let i = 0; i < 160_000; i += 1) {
    rows.push({ snapshot: "s", engine: "e", surface: "api", prompt_id: `p${i}`, run_id: `r${i}`, branded: false, mentioned: i % 4 === 0, cited: false });
  }
  const [group] = summarize(rows);
  assert.equal(group.questions.complete, 160_000);
  near(group.mention.questionRate, 0.25);

  rows.push({ snapshot: "t", engine: "e", surface: "product", prompt_id: "other", run_id: "t1", branded: false, mentioned: false, cited: false });
  const oneSided = compare(rows, { from: "s", to: "t" });
  assert.equal(oneSided.find((r) => r.surface === "api").excluded.onlyInFrom.length, 160_000);

  const variants = [];
  for (const [snapshot, hitEvery] of [["a", 4], ["b", 2]]) {
    for (let i = 0; i < 20_000; i += 1) {
      variants.push({ snapshot, engine: "e", surface: "api", prompt_id: `v${i}`, question_id: "q", run_id: `${snapshot}${i}`, branded: false, mentioned: i % hitEvery === 0, cited: false });
    }
  }
  const [result] = compare(variants, { from: "a", to: "b" });
  assert.equal(result.pairedQuestions, 1);
  near(result.mention.questionRateFrom, 0.25);
  near(result.mention.questionRateTo, 0.5);
  assert.deepEqual([result.mention.pairedHitsFrom, result.mention.pairedRunsFrom, result.mention.pairedHitsTo, result.mention.pairedRunsTo], [5000, 20_000, 10_000, 20_000]);
});

test("compare reports mention and citation changes separately, on the paired questions only", () => {
  const rows = [];
  const before = [[1, 10, 6], [2, 8, 5], [3, 10, 6], [2, 6, 4], [1, 10, 5], [3, 8, 5]];
  const after = [[4, 10, 1], [5, 10, 2], [5, 8, 1], [5, 10, 2], [3, 6, 1], [6, 10, 2]];
  before.forEach(([hits, total, cited], i) => rows.push(...runs({ snapshot: "a", prompt: `p${i}`, hits, runs: total, cited })));
  after.forEach(([hits, total, cited], i) => rows.push(...runs({ snapshot: "b", prompt: `p${i}`, hits, runs: total, cited })));
  // A third snapshot must not leak into the comparison.
  for (let i = 0; i < 6; i += 1) rows.push(...runs({ snapshot: "c", prompt: `p${i}`, hits: 10, runs: 10, cited: 10 }));
  const [result] = compare(rows, { from: "a", to: "b" });
  assert.equal(result.comparable, true);
  assert.equal(result.pairedQuestions, 6);
  const meanRate = (list, index) => list.reduce((sum, item) => sum + item[index] / item[1], 0) / list.length;
  near(result.mention.questionRateFrom, meanRate(before, 0));
  near(result.mention.questionRateTo, meanRate(after, 0));
  near(result.mention.questionRateDifference, meanRate(after, 0) - meanRate(before, 0));
  assert.deepEqual([result.mention.pairedHitsFrom, result.mention.pairedRunsFrom, result.mention.pairedHitsTo, result.mention.pairedRunsTo], [12, 52, 28, 54]);
  near(result.citation.questionRateFrom, meanRate(before, 2));
  near(result.citation.questionRateTo, meanRate(after, 2));
  assert.ok(result.citation.questionRateDifference < 0 && result.mention.questionRateDifference > 0);
  assert.deepEqual([result.citation.pairedHitsFrom, result.citation.pairedHitsTo], [31, 9]);
  assert.ok(!("verdict" in result.mention) && !("low" in result.mention) && !("difference" in result.mention));
  assert.deepEqual(result.groupRunsFrom, { answered: 52, noAnswer: 0, error: 0 });
  assert.deepEqual(result.groupRunsTo, { answered: 54, noAnswer: 0, error: 0 });
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
  near(result.mention.questionRateFrom, 0.5);
  near(result.mention.questionRateTo, 0.5);
  assert.equal(result.mention.questionRateDifference, 0);
  assert.equal(result.sameRunsPerPrompt, false);
  assert.ok(result.notes.some((note) => /number of answered runs per prompt differs/.test(note)));
});

test("compare gives an exact zero difference for identical records in a different order", () => {
  const variants = [["v1", 1], ["v2", 2], ["v3", 3]];
  const rows = [];
  for (const [prompt, hits] of variants) rows.push(...runs({ snapshot: "a", prompt, question: "q", hits, runs: 10 }));
  for (const [prompt, hits] of [...variants].reverse()) rows.push(...runs({ snapshot: "b", prompt, question: "q", hits, runs: 10 }));
  const [result] = compare(rows, { from: "a", to: "b" });
  assert.equal(result.mention.questionRateDifference, 0);
  assert.equal(result.sameRunsPerPrompt, true);
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
  assert.deepEqual(result.groupRunsFrom, { answered: 24, noAnswer: 0, error: 0 });
  assert.deepEqual(result.groupRunsTo, { answered: 16, noAnswer: 1, error: 2 });
  near(result.mention.questionRateFrom, 0.375);
  near(result.mention.questionRateTo, 0.5);
  assert.equal(result.mention.pairedHitsFrom, 3); // only the paired questions
});

test("compare lists the questions with hits on one date only, for each metric", () => {
  const rows = [];
  // mention: gained on g1, g2, g3; lost on l1. citation: gained on l1; lost on g1 and g2.
  const plan = { g1: [[0, 2], [3, 0]], g2: [[0, 1], [1, 0]], g3: [[0, 0], [2, 0]], l1: [[4, 0], [0, 1]], steady: [[1, 1], [1, 1]] };
  for (const [prompt, [[beforeHits, beforeCited], [afterHits, afterCited]]] of Object.entries(plan)) {
    rows.push(...runs({ snapshot: "a", prompt, hits: beforeHits, runs: 10, cited: beforeCited }));
    rows.push(...runs({ snapshot: "b", prompt, hits: afterHits, runs: 10, cited: afterCited }));
    rows.push(...runs({ snapshot: "c", prompt, hits: 10, runs: 10, cited: 10 }));
  }
  const [result] = compare(rows, { from: "a", to: "b" });
  assert.equal(result.mention.questionsHitOnlyAfter, 3);
  assert.deepEqual(result.mention.hitOnlyAfterIds.sort(), ["g1", "g2", "g3"]);
  assert.equal(result.mention.questionsHitOnlyBefore, 1);
  assert.deepEqual(result.mention.hitOnlyBeforeIds, ["l1"]);
  assert.equal(result.citation.questionsHitOnlyAfter, 1);
  assert.deepEqual(result.citation.hitOnlyAfterIds, ["l1"]);
  assert.equal(result.citation.questionsHitOnlyBefore, 2);
  assert.deepEqual(result.citation.hitOnlyBeforeIds.sort(), ["g1", "g2"]);
  assert.equal(result.mention.baselineZero, false);
});

test("compare qualifies a zero baseline and does not invent a change when both dates are empty", () => {
  const rows = [];
  for (let i = 0; i < 8; i += 1) rows.push(...runs({ snapshot: "a", prompt: `p${i}`, hits: 0, runs: 10 }));
  for (let i = 0; i < 8; i += 1) rows.push(...runs({ snapshot: "b", prompt: `p${i}`, hits: i < 2 ? 3 : 0, runs: 10 }));
  rows.push(...runs({ snapshot: "a", prompt: "dropped", hits: 5, runs: 10 }));
  const [result] = compare(rows, { from: "a", to: "b" });
  assert.equal(result.mention.baselineZero, true);
  assert.equal(result.mention.questionsHitOnlyAfter, 2);
  assert.deepEqual([result.mention.pairedHitsFrom, result.mention.pairedHitsTo], [0, 6]);
  assert.ok(!("relativeChange" in result.mention));
  assert.match(result.mention.note, /among the paired questions/);
  assert.match(result.mention.note, /counts/);
  assert.match(result.mention.note, /between these two snapshots/);
  assert.match(result.citation.note, /No hits among the paired questions in either snapshot/);
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
  assert.deepEqual(api.groupRunsFrom, { answered: 2, noAnswer: 0, error: 1 });
  assert.equal(api.groupRunsTo, null);
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
  const second = { ...row, run_id: "2", notes: { locale: "ja-JP", cited_urls: ["https://example.com/"] } };
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
  assert.equal(summarize(parseObservations(JSON.stringify(raw)))[0].questions.recorded, 2);
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
  check([row, row], /row 2: duplicate run_id "1"/);
  check([row, { ...row, run_id: "2", branded: true }], /row 2: prompt "p1" is branded in one row and unbranded in another/);
  check([row, { ...row, run_id: "2", question_id: "other" }], /row 2: prompt "p1" belongs to more than one question_id/);
});

test("validation rejects unknown fields and suggests the intended one", () => {
  const row = { snapshot: "a", engine: "chatgpt", surface: "product", prompt_id: "p1", run_id: "1", branded: false, mentioned: true, cited: false };
  const check = (extra, pattern) => assert.throws(() => summarize([{ ...row, ...extra }]), pattern);
  check({ questionId: "q1" }, /row 1: unknown field "questionId"; did you mean "question_id"\?/);
  check({ Status: "error" }, /row 1: unknown field "Status"; did you mean "status"\?/);
  check({ queston_id: "q1" }, /row 1: unknown field "queston_id"; did you mean "question_id"\?/);
  check({ staus: "error" }, /row 1: unknown field "staus"; did you mean "status"\?/);
  check({ locale: "ja-JP" }, /row 1: unknown field "locale"\. Put other details under "notes"/);
  assert.equal(summarize([{ ...row, notes: "anything" }]).length, 1);
});

test("a question with several prompts needs an explicit question_id on each of them", () => {
  const base = { snapshot: "a", engine: "chatgpt", surface: "product", branded: false, mentioned: false, cited: false };
  const standalone = { ...base, prompt_id: "q1", run_id: "1" };
  const variant = { ...base, prompt_id: "other", run_id: "2", question_id: "q1" };
  assert.throws(() => summarize([standalone, variant]), /question "q1" groups several prompts \(other, q1\).*explicit question_id/);
  assert.throws(() => summarize([variant, standalone]), /question "q1" groups several prompts/);
  const [group] = summarize([{ ...standalone, question_id: "q1" }, variant]);
  assert.deepEqual(group.questions, { recorded: 1, complete: 1, incomplete: [] });
});

test("the default tables state their populations, list every exclusion, and do not round a hit away", () => {
  const dir = mkdtempSync(join(tmpdir(), "visibility-stats-"));
  try {
    const file = join(dir, "runs.json");
    const rows = [];
    [2, 4, 4, 6, 4].forEach((hits, i) => rows.push(...runs({ snapshot: "a|1", prompt: `p${i}`, hits, runs: 10 })));
    [4, 6, 5, 8, 6].forEach((hits, i) => rows.push(...runs({ snapshot: "--b", prompt: `p${i}`, hits, runs: 10 })));
    const gone = Array.from({ length: 12 }, (_, i) => `gone${i}`);
    for (const prompt of gone) rows.push(...runs({ snapshot: "a|1", prompt, hits: 0, runs: 10 }));
    rows.push(...runs({ snapshot: "--b", prompt: "added", hits: 0, runs: 10 }));
    rows.push(...runs({ snapshot: "a|1", prompt: "swap-old", question: "swapped", hits: 0, runs: 10 }), ...runs({ snapshot: "--b", prompt: "swap-new", question: "swapped", hits: 0, runs: 10 }));
    rows.push(...runs({ snapshot: "a|1", prompt: "flaky", hits: 0, runs: 10 }), unanswered({ snapshot: "--b", prompt: "flaky" }));
    rows.push(...runs({ snapshot: "a|1", surface: "api", prompt: "p0", hits: 1, runs: 3 }));
    writeFileSync(file, JSON.stringify(rows));
    const run = (...args) => execFileSync("node", [scriptPath, ...args], { encoding: "utf8" });

    const table = run("summarize", file);
    assert.match(table, /observed counts and rates/);
    assert.match(table, /\| --b \| chatgpt \| product \| no \| 7 \/ 8 \| 70 \|/);
    assert.match(table, /\| a\\\|1 \| chatgpt \| product \| no \| 19 \/ 19 \| 190 \|/);
    assert.match(table, /41\.4% by question \(7 complete questions\), 29\/70 answered runs \(41\.4%\), 5 of 8 recorded questions with a hit/);
    assert.match(table, /Note \(--b \/ chatgpt \/ product \/ unbranded\): 1 question left out of the by-question rate.*: flaky\./);
    assert.doesNotMatch(table, /95%|interval/);

    const comparison = run("compare", file, "--from", "a|1", "--to=--b");
    assert.ok(comparison.includes('Comparing "a|1" (before) with "--b" (after)'));
    assert.match(comparison, /\| chatgpt \| product \| no \| 5 \| 40\.0% → 58\.0% by question \(\+18\.0 pt\), hits 20\/50 → 29\/50 answered runs, questions with a hit only before: 0, only after: 0 \|/);
    assert.ok(comparison.includes(`left out 12 questions recorded only in "a|1": ${gone.join(", ")}.`));
    assert.ok(comparison.includes('left out 1 question recorded only in "--b": added.'));
    assert.ok(comparison.includes("left out 1 question whose recorded prompts differ between the snapshots: swapped."));
    assert.ok(comparison.includes("left out 1 question with a prompt that had zero answered runs in at least one snapshot: flaky."));
    assert.match(comparison, /Note \(chatgpt \/ api \/ unbranded\): whole-group counts: "a\|1" had 3 answered runs, 0 runs with no AI answer, and 0 failed runs\./);
    assert.match(comparison, /whole-group counts: "a\|1" had 190 answered runs, 0 runs with no AI answer, and 0 failed runs; "--b" had 70 answered runs, 0 runs with no AI answer, and 1 failed run\./);
    assert.match(comparison, /do not show whether a difference is larger than run-to-run noise/);
    assert.doesNotMatch(comparison, /95%|interval excludes|increase \(|decrease \(/);

    const json = JSON.parse(run("compare", file, "--from", "a|1", "--to=--b", "--json"));
    const product = json.find((entry) => entry.surface === "product");
    assert.equal(product.pairedQuestions, 5);
    assert.deepEqual(product.excluded.onlyInFrom, gone);

    const sparse = join(dir, "sparse.json");
    const sparseRows = [];
    for (let q = 0; q < 50; q += 1) {
      for (let v = 0; v < 5; v += 1) {
        const hit = q === 0 && v === 0 ? 1 : 0;
        sparseRows.push(...runs({ snapshot: "s1", prompt: `q${q}v${v}`, question: `q${q}`, hits: 0, runs: 10, cited: 10 }));
        sparseRows.push(...runs({ snapshot: "s2", prompt: `q${q}v${v}`, question: `q${q}`, hits: hit, runs: 10, cited: 10 - hit }));
      }
    }
    writeFileSync(sparse, JSON.stringify(sparseRows));
    const sparseComparison = run("compare", sparse, "--from", "s1", "--to", "s2");
    assert.match(sparseComparison, /0\.0% → <0\.1% by question \(\+<0\.1 pt\), hits 0\/2500 → 1\/2500 answered runs/);
    assert.match(sparseComparison, /100\.0% → >99\.9% by question \(-<0\.1 pt\), hits 2500\/2500 → 2499\/2500 answered runs/);
    assert.match(run("summarize", sparse), /<0\.1% by question \(50 complete questions\), 1\/2500 answered runs \(<0\.1%\)/);
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});

test("the CLI rejects bad usage with exit code 2 and bad data with exit code 1", () => {
  const dir = mkdtempSync(join(tmpdir(), "visibility-stats-"));
  try {
    const file = join(dir, "runs.json");
    writeFileSync(file, JSON.stringify([...runs({ snapshot: "a|1", prompt: "p1", hits: 1, runs: 2 }), ...runs({ snapshot: "--b", prompt: "p1", hits: 1, runs: 2 })]));
    const usage = (...args) => spawnSync("node", [scriptPath, ...args], { encoding: "utf8" });
    assert.equal(usage("compare", file, "--from", "a|1", "--to=--b").status, 0);
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
