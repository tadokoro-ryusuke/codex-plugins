#!/usr/bin/env node

import { existsSync, readFileSync, readdirSync, statSync } from "node:fs";
import { join, relative, dirname, resolve } from "node:path";

const root = process.cwd();
const errors = [];

const HOOK_EVENTS = new Set([
  "SessionStart",
  "SubagentStart",
  "PreToolUse",
  "PermissionRequest",
  "PostToolUse",
  "PreCompact",
  "PostCompact",
  "UserPromptSubmit",
  "SubagentStop",
  "Stop",
]);

// agentskills.io spec: name and description are required; license,
// compatibility, and metadata are optional. allowed-tools is experimental
// and intentionally not accepted here.
const ALLOWED_FRONTMATTER_KEYS = new Set(["name", "description", "license", "compatibility", "metadata"]);

function readJson(path) {
  try {
    return JSON.parse(readFileSync(path, "utf8"));
  } catch (error) {
    errors.push(`${path}: invalid JSON (${error.message})`);
    return null;
  }
}

function walkFiles(dir, out = []) {
  for (const entry of readdirSync(dir)) {
    const path = join(dir, entry);
    const stat = statSync(path);
    if (stat.isDirectory()) {
      walkFiles(path, out);
    } else {
      out.push(path);
    }
  }
  return out;
}

function checkMarketplace() {
  const path = join(root, ".agents/plugins/marketplace.json");
  const marketplace = readJson(path);
  if (!marketplace) return;

  if (marketplace.name !== "codex-plugins") {
    errors.push(`${relative(root, path)}: name must be codex-plugins`);
  }
  if (!Array.isArray(marketplace.plugins)) {
    errors.push(`${relative(root, path)}: plugins must be an array`);
    return;
  }

  for (const plugin of marketplace.plugins) {
    const pluginName = plugin.name;
    const sourcePath = plugin.source?.path;
    if (sourcePath !== `./plugins/${pluginName}`) {
      errors.push(`${relative(root, path)}: ${pluginName} source.path must be ./plugins/${pluginName}`);
    }
    const pluginRoot = join(root, sourcePath.replace(/^\.\//, ""));
    if (!existsSync(pluginRoot)) {
      errors.push(`${relative(root, path)}: ${pluginName} source path does not exist`);
    }
    if (!plugin.policy?.installation || !plugin.policy?.authentication || !plugin.category) {
      errors.push(`${relative(root, path)}: ${pluginName} must include policy.installation, policy.authentication, and category`);
    }
  }

  const listed = new Set(marketplace.plugins.map((plugin) => plugin.name));
  for (const pluginName of readdirSync(join(root, "plugins"))) {
    if (statSync(join(root, "plugins", pluginName)).isDirectory() && !listed.has(pluginName)) {
      errors.push(`${relative(root, path)}: plugins/${pluginName} exists but is not listed in the marketplace`);
    }
  }
}

function checkPlugin(pluginDir) {
  const manifestPath = join(pluginDir, ".codex-plugin/plugin.json");
  const manifest = readJson(manifestPath);
  if (!manifest) return;

  const pluginName = pluginDir.split("/").pop();
  if (manifest.name !== pluginName) {
    errors.push(`${relative(root, manifestPath)}: manifest name must match folder name`);
  }
  if (!/^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$/.test(manifest.version ?? "")) {
    errors.push(`${relative(root, manifestPath)}: version must be strict semver`);
  }
  if (manifest.skills !== "./skills/") {
    errors.push(`${relative(root, manifestPath)}: skills must be ./skills/`);
  }
  // Codex discovers hooks/hooks.json at the plugin root automatically.
  // The bundled plugin-creator validator rejects a hooks manifest field,
  // so rely on default-path discovery instead of declaring it.
  if ("hooks" in manifest) {
    errors.push(`${relative(root, manifestPath)}: do not declare hooks in plugin.json; place hooks at hooks/hooks.json (auto-discovered)`);
  }
  for (const required of ["displayName", "shortDescription", "longDescription", "developerName", "category"]) {
    if (!manifest.interface?.[required]) {
      errors.push(`${relative(root, manifestPath)}: missing interface.${required}`);
    }
  }

  const hooksPath = join(pluginDir, "hooks/hooks.json");
  if (existsSync(hooksPath)) {
    checkHooks(hooksPath, pluginDir);
  }
}

function checkHooks(hooksPath, pluginDir) {
  const rel = relative(root, hooksPath);
  const config = readJson(hooksPath);
  if (!config) return;

  if (typeof config.hooks !== "object" || config.hooks === null) {
    errors.push(`${rel}: top-level hooks object is required`);
    return;
  }

  for (const [event, groups] of Object.entries(config.hooks)) {
    if (!HOOK_EVENTS.has(event)) {
      errors.push(`${rel}: unknown hook event ${event}`);
      continue;
    }
    if (!Array.isArray(groups)) {
      errors.push(`${rel}: ${event} must be an array of matcher groups`);
      continue;
    }
    for (const group of groups) {
      for (const hook of group.hooks ?? []) {
        // Codex executes command handlers only; prompt/agent handlers are
        // parsed but skipped, so shipping them is a silent no-op.
        if (hook.type !== "command") {
          errors.push(`${rel}: ${event} handler type must be "command" (got ${JSON.stringify(hook.type)})`);
        }
        if (!hook.command || typeof hook.command !== "string") {
          errors.push(`${rel}: ${event} handler is missing a command`);
          continue;
        }
        const scriptMatch = hook.command.match(/\$\{PLUGIN_ROOT\}\/(\S+)/);
        if (scriptMatch && !existsSync(join(pluginDir, scriptMatch[1]))) {
          errors.push(`${rel}: ${event} references missing script ${scriptMatch[1]}`);
        }
      }
    }
  }
}

function checkSkill(skillFile) {
  const content = readFileSync(skillFile, "utf8");
  const rel = relative(root, skillFile);
  const match = content.match(/^---\n([\s\S]*?)\n---\n/);
  if (!match) {
    errors.push(`${rel}: missing YAML frontmatter`);
    return;
  }

  const frontmatter = match[1];
  const topLevelKeys = [...frontmatter.matchAll(/^([A-Za-z0-9_-]+):/gm)].map((m) => m[1]);
  for (const key of topLevelKeys) {
    if (!ALLOWED_FRONTMATTER_KEYS.has(key)) {
      errors.push(`${rel}: unsupported frontmatter key ${key}`);
    }
  }

  const name = frontmatter.match(/^name:\s*"?([^"\n]+)"?/m)?.[1]?.trim();
  if (!name) {
    errors.push(`${rel}: missing name`);
  }
  const description = frontmatter.match(/^description:\s*"?(.+?)"?\s*$/m)?.[1] ?? "";
  if (!description) {
    errors.push(`${rel}: missing description`);
  } else if (description.length > 1024) {
    errors.push(`${rel}: description exceeds the 1024 character limit`);
  }

  const folder = skillFile.split("/").slice(-2, -1)[0];
  if (name && name !== folder) {
    errors.push(`${rel}: skill name must match folder name (${folder})`);
  }
  if (content.includes("[TODO:")) {
    errors.push(`${rel}: contains TODO placeholder`);
  }

  const bodyLines = content.slice(match[0].length).split("\n").length;
  if (bodyLines > 500) {
    errors.push(`${rel}: body exceeds 500 lines (${bodyLines}); move detail into references/`);
  }

  const skillDir = dirname(skillFile);
  checkBundledPaths(content, skillDir, rel);

  const openaiYamlPath = join(skillDir, "agents/openai.yaml");
  if (!existsSync(openaiYamlPath)) {
    errors.push(`${rel}: missing agents/openai.yaml`);
  } else {
    checkOpenAiYaml(openaiYamlPath, name);
  }
}

function checkBundledPaths(content, skillDir, rel) {
  // Verify that references/scripts/assets paths mentioned in SKILL.md exist.
  const pathPattern = /(?:\.\.\/[A-Za-z0-9-]+\/)?(?:references|scripts|assets)\/[A-Za-z0-9_./-]+\.[A-Za-z0-9]+/g;
  for (const token of new Set(content.match(pathPattern) ?? [])) {
    const target = resolve(skillDir, token);
    if (!target.startsWith(resolve(root, "plugins"))) continue;
    if (!existsSync(target)) {
      errors.push(`${rel}: references missing bundled file ${token}`);
    }
  }
}

function checkOpenAiYaml(path, skillName) {
  const content = readFileSync(path, "utf8");
  const rel = relative(root, path);
  for (const required of ["display_name", "short_description", "default_prompt"]) {
    if (!new RegExp(`^\\s*${required}:`, "m").test(content)) {
      errors.push(`${rel}: missing interface.${required}`);
    }
  }
  if (skillName && !content.includes(`$${skillName}`)) {
    errors.push(`${rel}: default_prompt must mention $${skillName}`);
  }
  if (/Use\s+-[A-Za-z0-9-]+/.test(content)) {
    errors.push(`${rel}: default_prompt looks like shell-expanded skill name`);
  }
}

function checkNoClaudeOnlyTokens() {
  const allowed = new Set([
    "README.md",
    "AGENTS.md",
    "CLAUDE.md", // Claude Code 向けラッパ（@AGENTS.md import）。Claude 構文への言及が本文の目的
    "docs/research/codex-plugin-research.md",
    "scripts/validate-codex-plugins.mjs",
  ]);
  const tokens = [/CLAUDE_[A-Z_]+/, /\.claude\//, /\.claude-plugin/, /allowed-tools:/, /argument-hint:/, /\/dev-core:/, /\/github-tools:/];
  for (const file of walkFiles(root)) {
    const rel = relative(root, file);
    if (rel.startsWith(".git/") || rel.startsWith("node_modules/")) continue;
    if (allowed.has(rel)) continue;
    const content = readFileSync(file, "utf8");
    for (const token of tokens) {
      if (token.test(content)) {
        errors.push(`${rel}: contains Claude-only token ${token}`);
      }
    }
  }
}

checkMarketplace();

for (const pluginName of readdirSync(join(root, "plugins"))) {
  const pluginDir = join(root, "plugins", pluginName);
  if (statSync(pluginDir).isDirectory()) {
    checkPlugin(pluginDir);
  }
}

for (const skillFile of walkFiles(join(root, "plugins")).filter((file) => file.endsWith("/SKILL.md"))) {
  checkSkill(skillFile);
}

checkNoClaudeOnlyTokens();

if (errors.length > 0) {
  console.error(errors.join("\n"));
  process.exit(1);
}

console.log("Codex plugin validation passed.");
