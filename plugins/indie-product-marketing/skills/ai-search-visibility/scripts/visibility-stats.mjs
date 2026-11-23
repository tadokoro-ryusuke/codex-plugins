#!/usr/bin/env node
// Mention-rate and citation-rate summaries for an AI-visibility prompt set.
//
// Each observation is one run of one prompt on one engine and surface:
//   { "snapshot": "2026-11-baseline", "engine": "chatgpt", "surface": "product",
//     "prompt_id": "P-07", "run_id": "2026-11-baseline/chatgpt/P-07/03",
//     "branded": false, "mentioned": true, "cited": false }
// Optional fields: "question_id" (defaults to prompt_id; give prompt variants of
// one buyer question the same value) and "status" ("answered" by default,
// "no_answer" when the engine showed no AI answer, "error" for a failed run).
//
// The buyer question is the unit of analysis: each question's rate over its
// answered runs counts once, and the interval comes from the spread between
// questions. Two snapshots are compared through question-level paired
// differences. This follows Miller, "Adding Error Bars to Evals"
// (arXiv:2411.00640): standard errors of the mean over questions, related
// questions treated as one cluster, repeated runs to reduce within-question
// noise, and paired differences when the same questions are measured twice.
//
// The interval is approximate and describes buyers' questions in general only
// if the questions are an independent, representative sample of them. For a
// hand-picked set it describes that set.
//
// Usage:
//   node visibility-stats.mjs summarize <file> [--json]
//   node visibility-stats.mjs compare <file> --from <snapshot> --to <snapshot> [--json]
//
// <file> holds a JSON array or JSON Lines. Exit codes: 0 ok, 1 bad data, 2 bad usage.

import { readFileSync, realpathSync } from "node:fs";
import { fileURLToPath } from "node:url";

const Z_95 = 1.959964;
// Rates are ratios of small integers; treat a spread below this as "every question agrees".
const NO_SPREAD = 1e-12;
const STATUSES = ["answered", "no_answer", "error"];

// Two-sided 95% Student t critical values for 1..30 degrees of freedom.
const T_TABLE = [
  12.706, 4.303, 3.182, 2.776, 2.571, 2.447, 2.365, 2.306, 2.262, 2.228,
  2.201, 2.179, 2.16, 2.145, 2.131, 2.12, 2.11, 2.101, 2.093, 2.086,
  2.08, 2.074, 2.069, 2.064, 2.06, 2.056, 2.052, 2.048, 2.045, 2.042,
];

export function tCritical(degreesOfFreedom) {
  if (!Number.isInteger(degreesOfFreedom) || degreesOfFreedom < 1) {
    throw new Error("degrees of freedom must be a positive integer");
  }
  if (degreesOfFreedom <= T_TABLE.length) return T_TABLE[degreesOfFreedom - 1];
  // Cornish-Fisher expansion around the normal quantile; accurate to 3 decimals above 30.
  const z = Z_95;
  const v = degreesOfFreedom;
  return z + (z ** 3 + z) / (4 * v) + (5 * z ** 5 + 16 * z ** 3 + 3 * z) / (96 * v ** 2);
}

export function wilsonInterval(successes, trials) {
  if (trials <= 0) throw new Error("trials must be positive");
  const p = successes / trials;
  const z2 = Z_95 ** 2;
  const denominator = 1 + z2 / trials;
  const center = (p + z2 / (2 * trials)) / denominator;
  const half = (Z_95 * Math.sqrt((p * (1 - p)) / trials + z2 / (4 * trials ** 2))) / denominator;
  return {
    low: successes === 0 ? 0 : Math.max(0, center - half),
    high: successes === trials ? 1 : Math.min(1, center + half),
  };
}

export function parseObservations(text) {
  let rows;
  const trimmed = text.trim();
  try {
    rows = trimmed.startsWith("[")
      ? JSON.parse(trimmed)
      : trimmed.split("\n").filter((line) => line.trim() !== "").map((line) => JSON.parse(line));
  } catch (error) {
    throw new Error(`could not parse observations as a JSON array or JSON Lines (${error.message})`);
  }
  if (!Array.isArray(rows) || rows.length === 0) throw new Error("no observations found");

  const runIds = new Set();
  const promptStratum = new Map();
  const promptQuestion = new Map();
  return rows.map((raw, index) => {
    const number = index + 1;
    const row = normalizeRow(raw, number);
    if (runIds.has(row.run_id)) throw new Error(`row ${number}: duplicate run_id "${row.run_id}"`);
    runIds.add(row.run_id);
    if (promptStratum.has(row.prompt_id) && promptStratum.get(row.prompt_id) !== row.branded) {
      throw new Error(`row ${number}: prompt "${row.prompt_id}" is branded in one row and unbranded in another`);
    }
    promptStratum.set(row.prompt_id, row.branded);
    if (promptQuestion.has(row.prompt_id) && promptQuestion.get(row.prompt_id) !== row.question_id) {
      throw new Error(`row ${number}: prompt "${row.prompt_id}" belongs to more than one question_id`);
    }
    promptQuestion.set(row.prompt_id, row.question_id);
    return row;
  });
}

function normalizeRow(row, number) {
  if (row === null || typeof row !== "object" || Array.isArray(row)) {
    throw new Error(`row ${number}: must be an object`);
  }
  for (const field of ["snapshot", "engine", "surface", "prompt_id", "run_id"]) {
    if (typeof row[field] !== "string" || row[field].trim() === "") {
      throw new Error(`row ${number}: ${field} must be a non-empty string`);
    }
  }
  if (typeof row.branded !== "boolean") throw new Error(`row ${number}: branded must be true or false`);
  if (row.question_id !== undefined && (typeof row.question_id !== "string" || row.question_id.trim() === "")) {
    throw new Error(`row ${number}: question_id must be a non-empty string when present`);
  }
  const status = row.status ?? "answered";
  if (!STATUSES.includes(status)) throw new Error(`row ${number}: status must be one of ${STATUSES.join(", ")}`);
  if (status === "answered") {
    for (const field of ["mentioned", "cited"]) {
      if (typeof row[field] !== "boolean") throw new Error(`row ${number}: ${field} must be true or false`);
    }
  }
  return {
    snapshot: row.snapshot,
    engine: row.engine,
    surface: row.surface,
    prompt_id: row.prompt_id,
    question_id: row.question_id ?? row.prompt_id,
    run_id: row.run_id,
    branded: row.branded,
    status,
    mentioned: status === "answered" && row.mentioned,
    cited: status === "answered" && row.cited,
  };
}

function mean(values) {
  return values.reduce((sum, value) => sum + value, 0) / values.length;
}

function sampleVariance(values) {
  const center = mean(values);
  return values.reduce((sum, value) => sum + (value - center) ** 2, 0) / (values.length - 1);
}

/** Group rows into snapshot + engine + surface + branded, then by question. */
function tally(rows) {
  const groups = new Map();
  for (const row of rows) {
    const key = JSON.stringify([row.snapshot, row.engine, row.surface, row.branded]);
    if (!groups.has(key)) {
      groups.set(key, {
        snapshot: row.snapshot,
        engine: row.engine,
        surface: row.surface,
        branded: row.branded,
        questions: new Map(),
        prompts: new Set(),
        noAnswer: 0,
        error: 0,
        citedWithoutMention: 0,
      });
    }
    const group = groups.get(key);
    group.prompts.add(row.prompt_id);
    if (!group.questions.has(row.question_id)) group.questions.set(row.question_id, { runs: 0, mentioned: 0, cited: 0 });
    if (row.status === "no_answer") group.noAnswer += 1;
    else if (row.status === "error") group.error += 1;
    else {
      const counts = group.questions.get(row.question_id);
      counts.runs += 1;
      if (row.mentioned) counts.mentioned += 1;
      if (row.cited) counts.cited += 1;
      if (row.cited && !row.mentioned) group.citedWithoutMention += 1;
    }
  }
  return [...groups.values()];
}

/** Questions that have at least one answered run. */
function answeredQuestions(group) {
  return new Map([...group.questions].filter(([, counts]) => counts.runs > 0));
}

function rateEstimate(questionCounts, field) {
  const hits = questionCounts.reduce((sum, counts) => sum + counts[field], 0);
  const runs = questionCounts.reduce((sum, counts) => sum + counts.runs, 0);
  const questionsWithHit = questionCounts.filter((counts) => counts[field] > 0).length;
  if (questionCounts.length === 0) {
    return { rate: null, pooledRate: null, hits, runs, questionsWithHit, low: null, high: null, method: "none", note: "No answered runs." };
  }
  const rates = questionCounts.map((counts) => counts[field] / counts.runs);
  const rate = mean(rates);
  const base = { rate, pooledRate: hits / runs, hits, runs, questionsWithHit };

  if (rates.length < 2) {
    return { ...base, low: null, high: null, method: "none", note: "An interval needs at least 2 questions." };
  }
  const variance = sampleVariance(rates);
  if (variance < NO_SPREAD) {
    if (rate === 0 || rate === 1) {
      // Every question agrees. A spread-based interval would have zero width and read as
      // certainty, so bound the rate with the number of questions as the sample size.
      const bound = wilsonInterval(rate === 0 ? 0 : rates.length, rates.length);
      return {
        ...base,
        low: bound.low,
        high: bound.high,
        method: "bound-from-question-count",
        note: "Every question gave the same result. Report counts. The bound reflects how many questions were asked, not how many runs.",
      };
    }
    return {
      ...base,
      low: null,
      high: null,
      method: "none",
      note: "Every question has the same rate, so the spread between questions gives no interval. Add questions or runs.",
    };
  }
  const half = tCritical(rates.length - 1) * Math.sqrt(variance / rates.length);
  return {
    ...base,
    low: Math.max(0, rate - half),
    high: Math.min(1, rate + half),
    method: "t-across-questions",
  };
}

export function summarize(rows) {
  return tally(rows).map((group) => {
    const questionCounts = [...answeredQuestions(group).values()];
    const runCounts = questionCounts.map((counts) => counts.runs);
    const answered = runCounts.reduce((sum, value) => sum + value, 0);
    return {
      snapshot: group.snapshot,
      engine: group.engine,
      surface: group.surface,
      branded: group.branded,
      questions: questionCounts.length,
      questionsWithoutAnswer: group.questions.size - questionCounts.length,
      prompts: group.prompts.size,
      runs: { answered, noAnswer: group.noAnswer, error: group.error },
      answeredRunsPerQuestion: runCounts.length > 0 ? { min: Math.min(...runCounts), max: Math.max(...runCounts) } : { min: 0, max: 0 },
      mention: rateEstimate(questionCounts, "mentioned"),
      citation: rateEstimate(questionCounts, "cited"),
      citedWithoutMention: group.citedWithoutMention,
    };
  });
}

function pairedChange(pairs, field) {
  const fromRates = pairs.map(([before]) => before[field] / before.runs);
  const toRates = pairs.map(([, after]) => after[field] / after.runs);
  const differences = toRates.map((rate, index) => rate - fromRates[index]);
  const difference = mean(differences);
  const hitsFrom = pairs.reduce((sum, [before]) => sum + before[field], 0);
  const result = {
    from: mean(fromRates),
    to: mean(toRates),
    difference,
    low: null,
    high: null,
    verdict: "not enough questions",
    baselineZero: hitsFrom === 0,
    hitsFrom,
    runsFrom: pairs.reduce((sum, [before]) => sum + before.runs, 0),
    hitsTo: pairs.reduce((sum, [, after]) => sum + after[field], 0),
    runsTo: pairs.reduce((sum, [, after]) => sum + after.runs, 0),
    newlyAppearing: pairs.filter(([before, after]) => before[field] === 0 && after[field] > 0).length,
    disappeared: pairs.filter(([before, after]) => before[field] > 0 && after[field] === 0).length,
  };
  const notes = [];

  if (differences.length >= 2) {
    const variance = sampleVariance(differences);
    if (variance < NO_SPREAD) {
      if (Math.abs(difference) < NO_SPREAD) result.verdict = "no change observed";
      else {
        result.verdict = "no interval";
        notes.push("Every question moved by the same amount, so the data give no interval and no basis for calling the change real.");
      }
    } else {
      const half = tCritical(differences.length - 1) * Math.sqrt(variance / differences.length);
      result.low = Math.max(-1, difference - half);
      result.high = Math.min(1, difference + half);
      if (result.low === -1 && result.high === 1) {
        notes.push("The interval covers the whole possible range; there are too few questions or runs to say anything.");
      }
      result.verdict = result.low > 0 ? "increase (interval excludes zero)" : result.high < 0 ? "decrease (interval excludes zero)" : "inconclusive";
    }
  }
  if (result.baselineZero) {
    notes.unshift("The baseline had no hits, so a percentage change is undefined. Report counts and first appearances.");
  }
  if (notes.length > 0) result.note = notes.join(" ");
  return result;
}

export function compare(rows, { from, to }) {
  const groups = tally(rows);
  for (const label of [from, to]) {
    if (!groups.some((group) => group.snapshot === label)) throw new Error(`snapshot "${label}" has no observations`);
  }
  const strata = new Map();
  for (const group of groups.filter((candidate) => candidate.snapshot === from || candidate.snapshot === to)) {
    const key = JSON.stringify([group.engine, group.surface, group.branded]);
    if (!strata.has(key)) strata.set(key, {});
    strata.get(key)[group.snapshot === from ? "before" : "after"] = group;
  }

  const results = [];
  for (const { before, after } of strata.values()) {
    const present = before ?? after;
    const entry = { engine: present.engine, surface: present.surface, branded: present.branded, from, to, comparable: false };
    if (!before || !after) {
      entry.reason = `This engine, surface, and prompt type appears only in "${before ? from : to}".`;
      results.push(entry);
      continue;
    }
    const beforeQuestions = answeredQuestions(before);
    const afterQuestions = answeredQuestions(after);
    const shared = [...beforeQuestions.keys()].filter((question) => afterQuestions.has(question));
    entry.pairedQuestions = shared.length;
    entry.onlyInFrom = [...beforeQuestions.keys()].filter((question) => !afterQuestions.has(question));
    entry.onlyInTo = [...afterQuestions.keys()].filter((question) => !beforeQuestions.has(question));
    if (shared.length === 0) {
      entry.reason = "The two snapshots share no answered question.";
    } else {
      const pairs = shared.map((question) => [beforeQuestions.get(question), afterQuestions.get(question)]);
      entry.comparable = true;
      entry.mention = pairedChange(pairs, "mentioned");
      entry.citation = pairedChange(pairs, "cited");
    }
    results.push(entry);
  }
  return results;
}

function percent(value) {
  return `${(value * 100).toFixed(1)}%`;
}

function formatRate(estimate) {
  if (estimate.rate === null) return "no answered runs";
  const interval = estimate.low === null ? "no interval" : `${percent(estimate.low)}–${percent(estimate.high)}`;
  const withHit = `${estimate.questionsWithHit} question${estimate.questionsWithHit === 1 ? "" : "s"} with a hit`;
  return `${percent(estimate.rate)} (${interval}); ${estimate.hits}/${estimate.runs} runs, ${withHit}`;
}

function formatChange(change) {
  const points = (value) => `${value >= 0 ? "+" : ""}${(value * 100).toFixed(1)} pt`;
  const interval = change.low === null ? "no interval" : `${points(change.low)} to ${points(change.high)}`;
  const counts = `hits ${change.hitsFrom}/${change.runsFrom} → ${change.hitsTo}/${change.runsTo}`;
  const firsts = change.baselineZero ? `, first appearances ${change.newlyAppearing}` : "";
  return `${percent(change.from)} → ${percent(change.to)}, ${points(change.difference)} (${interval}); ${counts}${firsts}: ${change.verdict}`;
}

function summaryTable(groups) {
  const lines = [
    "Rates are means of per-question rates over answered runs; intervals are approximate 95% intervals from the spread between questions.",
    "",
    "| Snapshot | Engine | Surface | Branded prompts | Questions | Answered runs | Mention rate | Citation rate |",
    "|---|---|---|---|---:|---:|---|---|",
  ];
  for (const group of groups) {
    lines.push(
      `| ${group.snapshot} | ${group.engine} | ${group.surface} | ${group.branded ? "yes" : "no"} | ${group.questions} | ${group.runs.answered} | ${formatRate(group.mention)} | ${formatRate(group.citation)} |`,
    );
  }
  for (const group of groups) {
    const label = `${group.snapshot} / ${group.engine} / ${group.surface} / ${group.branded ? "branded" : "unbranded"}`;
    const excluded = [];
    if (group.runs.noAnswer > 0) excluded.push(`${group.runs.noAnswer} run(s) with no AI answer`);
    if (group.runs.error > 0) excluded.push(`${group.runs.error} failed run(s)`);
    if (group.questionsWithoutAnswer > 0) excluded.push(`${group.questionsWithoutAnswer} question(s) never answered`);
    if (excluded.length > 0) lines.push("", `Note: ${label}: ${excluded.join("; ")}. These are outside the rates.`);
    if (group.citedWithoutMention > 0) {
      lines.push("", `Note: ${label}: ${group.citedWithoutMention} answered run(s) cited the product's page without naming the product.`);
    }
  }
  const notes = new Set(groups.flatMap((group) => [group.mention.note, group.citation.note]).filter(Boolean));
  for (const note of notes) lines.push("", `Note: ${note}`);
  return lines.join("\n");
}

function comparisonTable(results) {
  const lines = [
    "Changes are means of per-question differences on the questions both snapshots answered.",
    "",
    "| Engine | Surface | Branded prompts | Paired questions | Mention rate | Citation rate |",
    "|---|---|---|---:|---|---|",
  ];
  for (const result of results) {
    const start = `| ${result.engine} | ${result.surface} | ${result.branded ? "yes" : "no"} |`;
    if (!result.comparable) lines.push(`${start} ${result.pairedQuestions ?? 0} | not comparable | not comparable |`);
    else lines.push(`${start} ${result.pairedQuestions} | ${formatChange(result.mention)} | ${formatChange(result.citation)} |`);
  }
  for (const result of results) {
    const label = `${result.engine} / ${result.surface} / ${result.branded ? "branded" : "unbranded"}`;
    if (result.reason) lines.push("", `Note: ${label}: ${result.reason}`);
    else if (result.onlyInFrom.length + result.onlyInTo.length > 0) {
      lines.push(
        "",
        `Note: ${label}: left out ${result.onlyInFrom.length} question(s) only in "${result.from}" and ${result.onlyInTo.length} only in "${result.to}".`,
      );
    }
  }
  const notes = new Set(results.flatMap((result) => [result.mention?.note, result.citation?.note]).filter(Boolean));
  for (const note of notes) lines.push("", `Note: ${note}`);
  lines.push(
    "",
    "A single comparison is not a decision. Check the difference against same-day variability and confirm it with another snapshot before acting on it.",
  );
  return lines.join("\n");
}

function usage(message) {
  if (message) console.error(message);
  console.error("Usage: visibility-stats.mjs summarize <file> [--json]");
  console.error("       visibility-stats.mjs compare <file> --from <snapshot> --to <snapshot> [--json]");
  process.exit(2);
}

function main(argv) {
  const [command, file, ...rest] = argv;
  if (!["summarize", "compare"].includes(command) || !file) usage();
  const options = { json: false };
  for (let i = 0; i < rest.length; i += 1) {
    if (rest[i] === "--json") options.json = true;
    else if (rest[i] === "--from" || rest[i] === "--to") {
      options[rest[i].slice(2)] = rest[i + 1];
      i += 1;
    } else usage(`Unknown argument: ${rest[i]}`);
  }
  if (command === "compare" && (!options.from || !options.to)) usage("compare needs --from <snapshot> and --to <snapshot>");

  try {
    const rows = parseObservations(readFileSync(file, "utf8"));
    const result = command === "summarize" ? summarize(rows) : compare(rows, options);
    console.log(options.json ? JSON.stringify(result, null, 2) : command === "summarize" ? summaryTable(result) : comparisonTable(result));
  } catch (error) {
    console.error(error.message);
    process.exit(1);
  }
}

if (process.argv[1] && realpathSync(process.argv[1]) === fileURLToPath(import.meta.url)) {
  main(process.argv.slice(2));
}
