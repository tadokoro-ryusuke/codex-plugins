#!/usr/bin/env node

import { existsSync, readFileSync, readdirSync, statSync } from "node:fs";
import { join, relative } from "node:path";

const root = process.cwd();
const errors = [];

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
  if ("hooks" in manifest) {
    errors.push(`${relative(root, manifestPath)}: hooks field is not supported by local validator`);
  }
  for (const required of ["displayName", "shortDescription", "longDescription", "developerName", "category"]) {
    if (!manifest.interface?.[required]) {
      errors.push(`${relative(root, manifestPath)}: missing interface.${required}`);
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
    if (!["name", "description"].includes(key)) {
      errors.push(`${rel}: unsupported frontmatter key ${key}`);
    }
  }

  const name = frontmatter.match(/^name:\s*"?([^"\n]+)"?/m)?.[1]?.trim();
  if (!name) {
    errors.push(`${rel}: missing name`);
  }
  if (!frontmatter.match(/^description:/m)) {
    errors.push(`${rel}: missing description`);
  }

  const folder = skillFile.split("/").slice(-2, -1)[0];
  if (name && name !== folder) {
    errors.push(`${rel}: skill name must match folder name (${folder})`);
  }
  if (content.includes("[TODO:")) {
    errors.push(`${rel}: contains TODO placeholder`);
  }

  const skillDir = skillFile.slice(0, -"/SKILL.md".length);
  const openaiYamlPath = join(skillDir, "agents/openai.yaml");
  if (existsSync(openaiYamlPath)) {
    checkOpenAiYaml(openaiYamlPath, name);
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
    "docs/research/codex-plugin-research.md",
    "plugins/dev-core/skills/codex-collab/SKILL.md",
    "plugins/dev-core/skills/dev-workflow/SKILL.md",
    "scripts/validate-codex-plugins.mjs",
  ]);
  const tokens = [/CLAUDE_[A-Z_]+/, /\.claude\//, /\.claude-plugin/, /allowed-tools:/, /argument-hint:/, /\/dev-core:/, /\/github-tools:/];
  for (const file of walkFiles(root)) {
    const rel = relative(root, file);
    if (rel.startsWith(".git/")) continue;
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
