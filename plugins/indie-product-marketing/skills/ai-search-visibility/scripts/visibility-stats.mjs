#!/usr/bin/env node
// Counts and rates for a fixed AI-visibility prompt set.
//
// Each observation is one run of one prompt on one engine and surface:
//   { "snapshot": "2026-11-baseline", "engine": "chatgpt", "surface": "product",
//     "prompt_id": "P-07", "run_id": "2026-11-baseline/chatgpt/P-07/03",
//     "branded": false, "mentioned": true, "cited": false }
// Optional fields: "question_id" (defaults to prompt_id; put the same value on
// every prompt variant of one buyer question), "status" ("answered" by default,
// "no_answer" when the engine showed no AI answer, "error" for a failed run),
// and "notes" (any other detail; ignored). Other fields are rejected.
//
// The script validates the records, keeps engines, surfaces, and branded prompts
// apart, and reports what was observed: hits and answered runs, the pooled rate,
// a rate that weights every question equally, and, for two snapshots, the
// difference on the questions whose prompts are the same in both.
//
// It reports no confidence interval and no verdict on whether a difference is
// real; it has no validated model of the uncertainty in these runs. It knows
// only the prompts that appear in the file, and it groups by snapshot, engine,
// and surface, so keep one locale and one model or mode per series.
//
// Usage:
//   node visibility-stats.mjs summarize <file> [--json]
//   node visibility-stats.mjs compare <file> --from <snapshot> --to <snapshot> [--json]
//   (a label that starts with "--" can be given as --from=<label>)
//
// In JSON output, rates are fractions between 0 and 1.
// <file> holds a JSON array or JSON Lines. Exit codes: 0 ok, 1 bad data, 2 bad usage.

import { readFileSync, realpathSync } from "node:fs";
import { fileURLToPath } from "node:url";

const STATUSES = ["answered", "no_answer", "error"];
const TEXT_FIELDS = ["snapshot", "engine", "surface", "prompt_id", "run_id"];
const KNOWN_FIELDS = [...TEXT_FIELDS, "question_id", "branded", "status", "mentioned", "cited", "notes"];
const squash = (name) => name.toLowerCase().replace(/[^a-z0-9]/g, "");

function editDistance(a, b) {
  let previous = Array.from({ length: b.length + 1 }, (_, i) => i);
  for (let i = 1; i <= a.length; i += 1) {
    const current = [i];
    for (let j = 1; j <= b.length; j += 1) {
      current[j] = Math.min(previous[j] + 1, current[j - 1] + 1, previous[j - 1] + (a[i - 1] === b[j - 1] ? 0 : 1));
    }
    previous = current;
  }
  return previous[b.length];
}

/** The known field a misspelled key most likely stands for, if any. */
function closestField(key) {
  const squashed = squash(key);
  let best = null;
  let bestDistance = 3;
  for (const field of KNOWN_FIELDS) {
    const distance = editDistance(squashed, squash(field));
    if (distance < bestDistance) {
      best = field;
      bestDistance = distance;
    }
  }
  return best;
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
  return normalizeObservations(rows);
}

/** Validate rows and fill defaults. Safe to call on rows that are already normalized. */
export function normalizeObservations(rows) {
  if (!Array.isArray(rows) || rows.length === 0) throw new Error("no observations found");
  const runIds = new Set();
  const promptStratum = new Map();
  const promptQuestion = new Map();
  const questionPrompts = new Map();
  const implicitQuestions = new Set();
  const normalized = rows.map((raw, index) => {
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
    if (!questionPrompts.has(row.question_id)) questionPrompts.set(row.question_id, new Set());
    questionPrompts.get(row.question_id).add(row.prompt_id);
    if (raw.question_id === undefined) implicitQuestions.add(row.question_id);
    return row;
  });
  for (const question of implicitQuestions) {
    const prompts = questionPrompts.get(question);
    if (prompts.size > 1) {
      throw new Error(`question "${question}" groups several prompts (${[...prompts].sort().join(", ")}), so each of their rows needs an explicit question_id`);
    }
  }
  return normalized;
}

function checkText(row, field, number) {
  const value = row[field];
  if (typeof value !== "string" || value.trim() === "") throw new Error(`row ${number}: ${field} must be a non-empty string`);
  if (/[\u0000-\u001f\u007f\u0085\u2028\u2029]/.test(value.trim())) throw new Error(`row ${number}: ${field} must be a single line`);
  if (value !== value.trim()) throw new Error(`row ${number}: ${field} must not start or end with whitespace`);
}

function normalizeRow(row, number) {
  if (row === null || typeof row !== "object" || Array.isArray(row)) throw new Error(`row ${number}: must be an object`);
  for (const key of Object.keys(row)) {
    if (KNOWN_FIELDS.includes(key)) continue;
    const suggestion = closestField(key);
    throw new Error(`row ${number}: unknown field "${key}"${suggestion ? `; did you mean "${suggestion}"?` : "."} Put other details under "notes".`);
  }
  for (const field of TEXT_FIELDS) checkText(row, field, number);
  if (row.question_id !== undefined) checkText(row, "question_id", number);
  if (typeof row.branded !== "boolean") throw new Error(`row ${number}: branded must be true or false`);
  const status = row.status === undefined ? "answered" : row.status;
  if (!STATUSES.includes(status)) throw new Error(`row ${number}: status must be one of ${STATUSES.join(", ")}`);
  for (const field of ["mentioned", "cited"]) {
    if (status === "answered") {
      if (typeof row[field] !== "boolean") throw new Error(`row ${number}: ${field} must be true or false`);
    } else if (row[field] !== undefined && row[field] !== false) {
      throw new Error(`row ${number}: ${field} must be false or absent when status is ${status}`);
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

/** Group rows into snapshot + engine + surface + branded; within a group, question -> prompt -> counts. */
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
        noAnswer: 0,
        error: 0,
        citedWithoutMention: 0,
      });
    }
    const group = groups.get(key);
    if (!group.questions.has(row.question_id)) group.questions.set(row.question_id, new Map());
    const prompts = group.questions.get(row.question_id);
    if (!prompts.has(row.prompt_id)) prompts.set(row.prompt_id, { runs: 0, mentioned: 0, cited: 0 });
    if (row.status === "no_answer") group.noAnswer += 1;
    else if (row.status === "error") group.error += 1;
    else {
      const counts = prompts.get(row.prompt_id);
      counts.runs += 1;
      if (row.mentioned) counts.mentioned += 1;
      if (row.cited) counts.cited += 1;
      if (row.cited && !row.mentioned) group.citedWithoutMention += 1;
    }
  }
  return [...groups.values()];
}

/** A question is complete when every recorded variant has at least one answered run. */
function isComplete(prompts) {
  for (const counts of prompts.values()) if (counts.runs === 0) return false;
  return true;
}

function runTotals(group) {
  let answered = 0;
  for (const prompts of group.questions.values()) for (const counts of prompts.values()) answered += counts.runs;
  return { answered, noAnswer: group.noAnswer, error: group.error };
}

/** Variants in a fixed order, so the same records always add up the same way. */
function orderedVariants(prompts) {
  return [...prompts.keys()].sort().map((id) => prompts.get(id));
}

/** Rate with equal weight per question and equal weight per variant within it, over `questionIds`. */
function questionRate(group, questionIds, field) {
  if (questionIds.length === 0) return { rate: null, hits: 0, runs: 0 };
  let sum = 0;
  let hits = 0;
  let runs = 0;
  for (const id of questionIds) {
    const variants = orderedVariants(group.questions.get(id));
    let variantSum = 0;
    for (const counts of variants) {
      variantSum += counts[field] / counts.runs;
      hits += counts[field];
      runs += counts.runs;
    }
    sum += variantSum / variants.length;
  }
  const rate = hits === 0 ? 0 : hits === runs ? 1 : sum / questionIds.length;
  return { rate, hits, runs };
}

function metric(group, completeIds, field) {
  let hits = 0;
  let runs = 0;
  let questionsWithHit = 0;
  for (const prompts of group.questions.values()) {
    let questionHits = 0;
    for (const counts of prompts.values()) {
      questionHits += counts[field];
      runs += counts.runs;
    }
    hits += questionHits;
    if (questionHits > 0) questionsWithHit += 1;
  }
  return { hits, runs, pooledRate: runs === 0 ? null : hits / runs, questionRate: questionRate(group, completeIds, field).rate, questionsWithHit };
}

export function summarize(rows) {
  return tally(normalizeObservations(rows)).map((group) => {
    const recorded = [...group.questions.keys()];
    const completeIds = [];
    const incomplete = [];
    let recordedPrompts = 0;
    let answeredPrompts = 0;
    let min = Infinity;
    let max = 0;
    let weightUnit = null;
    let equalWeightPerRun = true;
    for (const id of recorded) {
      const prompts = group.questions.get(id);
      const complete = isComplete(prompts);
      (complete ? completeIds : incomplete).push(id);
      for (const counts of prompts.values()) {
        recordedPrompts += 1;
        if (counts.runs > 0) answeredPrompts += 1;
        if (counts.runs < min) min = counts.runs;
        if (counts.runs > max) max = counts.runs;
        if (complete) {
          // Each answered run of this prompt weighs 1 / (variants * runs) of its question.
          const unit = prompts.size * counts.runs;
          if (weightUnit === null) weightUnit = unit;
          else if (unit !== weightUnit) equalWeightPerRun = false;
        } else if (counts.runs > 0) {
          // The pooled rate counts these runs; the by-question rate does not.
          equalWeightPerRun = false;
        }
      }
    }
    if (completeIds.length === 0) equalWeightPerRun = null;
    const notes = [];
    if (incomplete.length > 0) {
      notes.push(`${plural(incomplete.length, "question")} left out of the by-question rate because a prompt got no answer: ${incomplete.join(", ")}. The pooled counts still include every answered run.`);
    }
    if (equalWeightPerRun === false) {
      notes.push("Answered runs do not all carry the same weight in the by-question rate, so it can differ from the pooled rate. Say which one is quoted.");
    }
    return {
      snapshot: group.snapshot,
      engine: group.engine,
      surface: group.surface,
      branded: group.branded,
      questions: { recorded: recorded.length, complete: completeIds.length, incomplete },
      prompts: { recorded: recordedPrompts, answered: answeredPrompts },
      runs: runTotals(group),
      answeredRunsPerRecordedPrompt: { min, max },
      equalWeightPerRun,
      mention: metric(group, completeIds, "mentioned"),
      citation: metric(group, completeIds, "cited"),
      citedWithoutMention: group.citedWithoutMention,
      notes,
    };
  });
}

function sameKeys(left, right) {
  if (left.size !== right.size) return false;
  for (const key of left.keys()) if (!right.has(key)) return false;
  return true;
}

function change(before, after, paired, field) {
  const from = questionRate(before, paired, field);
  const to = questionRate(after, paired, field);
  const hitsOf = (group, id) => {
    let hits = 0;
    for (const counts of group.questions.get(id).values()) hits += counts[field];
    return hits;
  };
  const hitOnlyAfterIds = [];
  const hitOnlyBeforeIds = [];
  for (const id of paired) {
    const was = hitsOf(before, id) > 0;
    const is = hitsOf(after, id) > 0;
    if (!was && is) hitOnlyAfterIds.push(id);
    if (was && !is) hitOnlyBeforeIds.push(id);
  }
  const result = {
    questionRateFrom: from.rate,
    questionRateTo: to.rate,
    questionRateDifference: to.rate - from.rate,
    pairedHitsFrom: from.hits,
    pairedRunsFrom: from.runs,
    pairedHitsTo: to.hits,
    pairedRunsTo: to.runs,
    questionsHitOnlyAfter: hitOnlyAfterIds.length,
    questionsHitOnlyBefore: hitOnlyBeforeIds.length,
    hitOnlyAfterIds,
    hitOnlyBeforeIds,
    baselineZero: from.hits === 0,
  };
  if (from.hits === 0 && to.hits === 0) {
    result.note = "No hits among the paired questions in either snapshot.";
  } else if (from.hits === 0) {
    result.note = "No baseline hits among the paired questions, so a percentage change is undefined. Report counts and the number of questions with a first observed hit between these two snapshots.";
  }
  return result;
}

export function compare(rows, { from, to }) {
  if (from === to) throw new Error("compare needs two different snapshots");
  const groups = tally(normalizeObservations(rows));
  for (const label of [from, to]) {
    if (!groups.some((group) => group.snapshot === label)) throw new Error(`snapshot "${label}" has no observations`);
  }
  const strata = new Map();
  for (const group of groups) {
    if (group.snapshot !== from && group.snapshot !== to) continue;
    const key = JSON.stringify([group.engine, group.surface, group.branded]);
    if (!strata.has(key)) strata.set(key, {});
    strata.get(key)[group.snapshot === from ? "before" : "after"] = group;
  }

  const results = [];
  for (const { before, after } of strata.values()) {
    const present = before ?? after;
    const excluded = { onlyInFrom: [], onlyInTo: [], variantsChanged: [], missingAnswers: [] };
    const entry = {
      engine: present.engine,
      surface: present.surface,
      branded: present.branded,
      from,
      to,
      comparable: false,
      pairedQuestions: 0,
      excluded,
      groupRunsFrom: before ? runTotals(before) : null,
      groupRunsTo: after ? runTotals(after) : null,
      notes: [],
    };
    if (!before || !after) {
      const target = excluded[before ? "onlyInFrom" : "onlyInTo"];
      for (const id of present.questions.keys()) target.push(id);
      entry.reason = `This engine, surface, and prompt type appears only in "${before ? from : to}".`;
      results.push(entry);
      continue;
    }
    const paired = [];
    for (const id of new Set([...before.questions.keys(), ...after.questions.keys()])) {
      const was = before.questions.get(id);
      const is = after.questions.get(id);
      if (!is) excluded.onlyInFrom.push(id);
      else if (!was) excluded.onlyInTo.push(id);
      else if (!sameKeys(was, is)) excluded.variantsChanged.push(id);
      else if (!isComplete(was) || !isComplete(is)) excluded.missingAnswers.push(id);
      else paired.push(id);
    }
    entry.pairedQuestions = paired.length;
    if (paired.length === 0) {
      entry.reason = "The two snapshots share no question that can be compared.";
    } else {
      entry.comparable = true;
      entry.mention = change(before, after, paired, "mentioned");
      entry.citation = change(before, after, paired, "cited");
      let sameEffort = true;
      for (const id of paired) {
        for (const [promptId, counts] of before.questions.get(id)) {
          if (after.questions.get(id).get(promptId).runs !== counts.runs) sameEffort = false;
        }
      }
      entry.sameRunsPerPrompt = sameEffort;
      if (!sameEffort) {
        entry.notes.push("The number of answered runs per prompt differs between the snapshots. More runs make a hit more likely to be observed, so counts of questions with a hit on one date only are not like-for-like.");
      }
    }
    results.push(entry);
  }
  return results;
}

function cell(value) {
  return String(value).replaceAll("|", "\\|");
}

/** One decimal, without rounding an observed hit or miss away. */
function percent(value) {
  const text = (value * 100).toFixed(1);
  if (value > 0 && text === "0.0") return "<0.1%";
  if (value < 1 && text === "100.0") return ">99.9%";
  return `${text}%`;
}

function points(value) {
  if (value === 0) return "0.0 pt";
  const sign = value > 0 ? "+" : "-";
  const text = (Math.abs(value) * 100).toFixed(1);
  return text === "0.0" ? `${sign}<0.1 pt` : `${sign}${text} pt`;
}

function plural(count, noun) {
  return `${count} ${noun}${count === 1 ? "" : "s"}`;
}

function formatMetric(value, group) {
  if (value.runs === 0) return "no answered runs";
  const byQuestion = value.questionRate === null ? "no by-question rate (no complete question)" : `${percent(value.questionRate)} by question (${plural(group.questions.complete, "complete question")})`;
  return `${byQuestion}, ${value.hits}/${value.runs} answered runs (${percent(value.pooledRate)}), ${value.questionsWithHit} of ${group.questions.recorded} recorded questions with a hit`;
}

function formatChange(changed) {
  return `${percent(changed.questionRateFrom)} → ${percent(changed.questionRateTo)} by question (${points(changed.questionRateDifference)}), hits ${changed.pairedHitsFrom}/${changed.pairedRunsFrom} → ${changed.pairedHitsTo}/${changed.pairedRunsTo} answered runs, questions with a hit only before: ${changed.questionsHitOnlyBefore}, only after: ${changed.questionsHitOnlyAfter}`;
}

function formatRuns(name, runs) {
  return `"${name}" had ${plural(runs.answered, "answered run")}, ${plural(runs.noAnswer, "run")} with no AI answer, and ${plural(runs.error, "failed run")}`;
}

function endSentence(text) {
  return /[.!?]$/.test(text) ? text : `${text}.`;
}

function summaryTable(groups) {
  const lines = [
    "These are observed counts and rates, not estimates with a margin of error. \"By question\" weights every complete question equally; the answered-runs figure pools every answered run.",
    "",
    "| Snapshot | Engine | Surface | Branded prompts | Questions (complete / recorded) | Answered runs | Mention | Citation |",
    "|---|---|---|---|---:|---:|---|---|",
  ];
  for (const group of groups) {
    lines.push(
      `| ${cell(group.snapshot)} | ${cell(group.engine)} | ${cell(group.surface)} | ${group.branded ? "yes" : "no"} | ${group.questions.complete} / ${group.questions.recorded} | ${group.runs.answered} | ${cell(formatMetric(group.mention, group))} | ${cell(formatMetric(group.citation, group))} |`,
    );
  }
  for (const group of groups) {
    const label = `${group.snapshot} / ${group.engine} / ${group.surface} / ${group.branded ? "branded" : "unbranded"}`;
    const notes = [...group.notes];
    const outside = [];
    if (group.runs.noAnswer > 0) outside.push(`${plural(group.runs.noAnswer, "run")} with no AI answer`);
    if (group.runs.error > 0) outside.push(plural(group.runs.error, "failed run"));
    if (outside.length > 0) notes.push(`Outside the rates: ${outside.join("; ")}`);
    if (group.citedWithoutMention > 0) notes.push(`${plural(group.citedWithoutMention, "answered run")} recorded as citing the product's page without naming the product`);
    for (const note of notes) lines.push("", `Note (${label}): ${endSentence(note)}`);
  }
  return lines.join("\n");
}

function comparisonTable(results, { from, to }) {
  const lines = [
    `Comparing "${from}" (before) with "${to}" (after) on the questions whose prompts are the same and answered in both. Each cell shows the by-question rate before → after and the difference in percentage points, then the observed counts on those questions.`,
    "",
    "| Engine | Surface | Branded prompts | Paired questions | Mention | Citation |",
    "|---|---|---|---:|---|---|",
  ];
  for (const result of results) {
    const start = `| ${cell(result.engine)} | ${cell(result.surface)} | ${result.branded ? "yes" : "no"} | ${result.pairedQuestions} |`;
    if (!result.comparable) lines.push(`${start} not comparable | not comparable |`);
    else lines.push(`${start} ${cell(formatChange(result.mention))} | ${cell(formatChange(result.citation))} |`);
  }
  for (const result of results) {
    const label = `${result.engine} / ${result.surface} / ${result.branded ? "branded" : "unbranded"}`;
    const notes = [];
    if (result.reason) notes.push(result.reason);
    const { onlyInFrom, onlyInTo, variantsChanged, missingAnswers } = result.excluded;
    if (onlyInFrom.length > 0) notes.push(`left out ${plural(onlyInFrom.length, "question")} recorded only in "${from}": ${onlyInFrom.join(", ")}`);
    if (onlyInTo.length > 0) notes.push(`left out ${plural(onlyInTo.length, "question")} recorded only in "${to}": ${onlyInTo.join(", ")}`);
    if (variantsChanged.length > 0) notes.push(`left out ${plural(variantsChanged.length, "question")} whose recorded prompts differ between the snapshots: ${variantsChanged.join(", ")}`);
    if (missingAnswers.length > 0) notes.push(`left out ${plural(missingAnswers.length, "question")} with a prompt that had zero answered runs in at least one snapshot: ${missingAnswers.join(", ")}`);
    const totals = [];
    if (result.groupRunsFrom) totals.push(formatRuns(from, result.groupRunsFrom));
    if (result.groupRunsTo) totals.push(formatRuns(to, result.groupRunsTo));
    notes.push(`whole-group counts: ${totals.join("; ")}`);
    notes.push(...result.notes);
    if (result.mention?.note) notes.push(`Mention: ${result.mention.note}`);
    if (result.citation?.note) notes.push(`Citation: ${result.citation.note}`);
    for (const note of notes) lines.push("", `Note (${label}): ${endSentence(note)}`);
  }
  lines.push(
    "",
    "These are observed differences. They do not show whether a difference is larger than run-to-run noise: compare it with the differences between same-day repeats of the same set, and confirm it in a further snapshot.",
  );
  return lines.join("\n");
}

function usage(message) {
  if (message) console.error(message);
  console.error("Usage: visibility-stats.mjs summarize <file> [--json]");
  console.error("       visibility-stats.mjs compare <file> --from <snapshot> --to <snapshot> [--json]");
  console.error("       A label that starts with -- can be given as --from=<label> or --to=<label>.");
  process.exit(2);
}

function main(argv) {
  const [command, file, ...rest] = argv;
  if (!["summarize", "compare"].includes(command)) usage();
  if (!file || file.startsWith("--")) usage("Give the observations file before any option.");
  const options = { json: false };
  for (let i = 0; i < rest.length; i += 1) {
    const argument = rest[i];
    const match = /^--(from|to)(?:=(.*))?$/s.exec(argument);
    if (argument === "--json" && !options.json) options.json = true;
    else if (match && command === "compare") {
      const [, name, inline] = match;
      if (options[name] !== undefined) usage(`--${name} was given more than once`);
      let value = inline;
      if (value === undefined) {
        value = rest[i + 1];
        i += 1;
        if (value === undefined || value.startsWith("--")) usage(`--${name} needs a snapshot label; use --${name}=<label> for a label that starts with --`);
      }
      if (value === "") usage(`--${name} needs a snapshot label`);
      options[name] = value;
    } else usage(`Unknown or misplaced argument: ${argument}`);
  }
  if (command === "compare") {
    if (options.from === undefined || options.to === undefined) usage("compare needs --from <snapshot> and --to <snapshot>");
    if (options.from === options.to) usage("compare needs two different snapshots");
  }

  try {
    const rows = parseObservations(readFileSync(file, "utf8"));
    const result = command === "summarize" ? summarize(rows) : compare(rows, options);
    console.log(options.json ? JSON.stringify(result, null, 2) : command === "summarize" ? summaryTable(result) : comparisonTable(result, options));
  } catch (error) {
    console.error(error.message);
    process.exit(1);
  }
}

if (process.argv[1] && realpathSync(process.argv[1]) === fileURLToPath(import.meta.url)) {
  main(process.argv.slice(2));
}
