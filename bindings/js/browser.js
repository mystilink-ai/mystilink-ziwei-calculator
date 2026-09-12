/**
 * Browser entry: same API as Node, but requires injected runCli.
 *
 * Example:
 *   const { createClient } = window.MystilinkZiwei;
 *   const client = createClient({ runCli: async (argv) => myBridge(argv) });
 */
'use strict';

function createClient(options) {
  if (!options || typeof options.runCli !== 'function') {
    throw new Error('Browser binding requires options.runCli(argv) returning JSON stdout');
  }
  const runCli = options.runCli;
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
      if (params.year != null) argv.push('--year', String(params.year));
      if (params.longitude != null) argv.push('--longitude', String(params.longitude));
      const raw = await runCli(argv);
      return JSON.parse(raw);
    },
    async version() {
      const raw = await runCli(['version']);
      return JSON.parse(raw);
    },
  };
}

if (typeof module !== 'undefined' && module.exports) {
  module.exports = { createClient };
}
if (typeof window !== 'undefined') {
  window.MystilinkZiwei = { createClient };
}
