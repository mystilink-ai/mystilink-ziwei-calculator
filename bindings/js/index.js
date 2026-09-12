/**
 * Mystilink Zi Wei calculator JS binding.
 *
 * Node: spawns `mystilink-ziwei` (or MYSTILINK_ZIWEI_CLI).
 * Browser: pass a custom `runCli(argv)` that returns a Promise<string> of JSON stdout.
 */

'use strict';

function defaultCliPath() {
  if (typeof process !== 'undefined' && process.env && process.env.MYSTILINK_ZIWEI_CLI) {
    return process.env.MYSTILINK_ZIWEI_CLI;
  }
  return 'mystilink-ziwei';
}

async function defaultRunCli(argv) {
  if (typeof require === 'function') {
    const { spawn } = require('child_process');
    return new Promise((resolve, reject) => {
      const child = spawn(defaultCliPath(), argv, { stdio: ['ignore', 'pipe', 'pipe'] });
      let stdout = '';
      let stderr = '';
      child.stdout.setEncoding('utf8');
      child.stderr.setEncoding('utf8');
      child.stdout.on('data', (d) => { stdout += d; });
      child.stderr.on('data', (d) => { stderr += d; });
      child.on('error', reject);
      child.on('close', (code) => {
        if (code !== 0) {
          reject(new Error(stderr || stdout || `exit ${code}`));
          return;
        }
        resolve(stdout);
      });
    });
  }
  throw new Error('Browser usage requires an injected runCli(argv) function');
}

function createClient(options) {
  const runCli = (options && options.runCli) || defaultRunCli;

  return {
    async chart(params) {
      const argv = [
        'chart',
        '--datetime', String(params.datetime),
        '--timezone', String(params.timezone),
        '--gender', String(params.gender),
        '--midnight-zi', String(params.midnightZi || params.midnight_zi || 'same-day'),
      ];
      if (params.siHua || params.si_hua) argv.push('--si-hua');
      if (params.year != null) {
        argv.push('--year', String(params.year));
      }
      if (params.longitude != null) {
        argv.push('--longitude', String(params.longitude));
      }
      const raw = await runCli(argv);
      return JSON.parse(raw);
    },
    async version() {
      const raw = await runCli(['version']);
      return JSON.parse(raw);
    },
  };
}

module.exports = { createClient, defaultRunCli, defaultCliPath };

// ESM-friendly named exports when supported by bundlers that rewrite CJS
module.exports.createClient = createClient;
