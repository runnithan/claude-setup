#!/usr/bin/env node
// Check for GSD updates in background, write result to cache
// Called by SessionStart hook - runs once per session

const fs = require('fs');
const path = require('path');
const os = require('os');
const { spawn } = require('child_process');

const homeDir = os.homedir();
const cwd = process.cwd();

// Detect runtime config directory (supports Claude, OpenCode, Gemini)
// Respects CLAUDE_CONFIG_DIR for custom config directory setups
function detectConfigDir(baseDir) {
  // Check env override first (supports multi-account setups)
  const envDir = process.env.CLAUDE_CONFIG_DIR;
  if (envDir && fs.existsSync(path.join(envDir, 'get-shit-done', 'VERSION'))) {
    return envDir;
  }
  for (const dir of ['.config/opencode', '.opencode', '.gemini', '.claude']) {
    if (fs.existsSync(path.join(baseDir, dir, 'get-shit-done', 'VERSION'))) {
      return path.join(baseDir, dir);
    }
  }
  return envDir || path.join(baseDir, '.claude');
}

const globalConfigDir = detectConfigDir(homeDir);
const projectConfigDir = detectConfigDir(cwd);
const cacheDir = path.join(globalConfigDir, 'cache');
const cacheFile = path.join(cacheDir, 'gsd-update-check.json');

// VERSION file locations (check project first, then global)
const projectVersionFile = path.join(projectConfigDir, 'get-shit-done', 'VERSION');
const globalVersionFile = path.join(globalConfigDir, 'get-shit-done', 'VERSION');

// Ensure cache directory exists
if (!fs.existsSync(cacheDir)) {
  fs.mkdirSync(cacheDir, { recursive: true });
}

// Run check in background (spawn background process, windowsHide prevents console flash)
const child = spawn(process.execPath, ['-e', `
  const fs = require('fs');
  const { execSync } = require('child_process');

  const cacheFile = ${JSON.stringify(cacheFile)};
  const projectVersionFile = ${JSON.stringify(projectVersionFile)};
  const globalVersionFile = ${JSON.stringify(globalVersionFile)};

  // Check project directory first (local install), then global
  let installed = '0.0.0';
  try {
    if (fs.existsSync(projectVersionFile)) {
      installed = fs.readFileSync(projectVersionFile, 'utf8').trim();
    } else if (fs.existsSync(globalVersionFile)) {
      installed = fs.readFileSync(globalVersionFile, 'utf8').trim();
    }
  } catch (e) {}

  let latest = null;
  try {
    latest = execSync('npm view get-shit-done-cc version', { encoding: 'utf8', timeout: 10000, windowsHide: true }).trim();
  } catch (e) {}

  // Normalize before comparing so a leading 'v', stray whitespace, or a
  // prerelease/build suffix doesn't trigger a false "update available". Compare
  // numeric major.minor.patch components when both parse as semver; otherwise
  // fall back to a trimmed string compare.
  function normVer(v) {
    return String(v == null ? '' : v).trim().replace(/^v/i, '');
  }
  function semverParts(v) {
    const core = normVer(v).split(/[-+]/)[0]; // drop prerelease/build metadata
    const m = core.match(/^(\\d+)\\.(\\d+)\\.(\\d+)$/);
    return m ? [Number(m[1]), Number(m[2]), Number(m[3])] : null;
  }
  function isNewer(latestV, installedV) {
    const a = semverParts(latestV);
    const b = semverParts(installedV);
    if (a && b) {
      for (let i = 0; i < 3; i++) {
        if (a[i] !== b[i]) return a[i] > b[i];
      }
      return false; // equal core versions -> not an update
    }
    return normVer(latestV) !== normVer(installedV);
  }

  const result = {
    update_available: !!latest && isNewer(latest, installed),
    installed,
    latest: latest || 'unknown',
    checked: Math.floor(Date.now() / 1000)
  };

  fs.writeFileSync(cacheFile, JSON.stringify(result));
`], {
  stdio: 'ignore',
  windowsHide: true,
  detached: true  // Required on Windows for proper process detachment
});

child.unref();
