// Throwaway interaction check for the cc composition prototype.
// Loads the prototype's inline script under a minimal DOM shim and drives
// every guided walkthrough and free-play operation.
//
// Run with: node prototype/cc-composition-cli.check.js
// Requires Node. Checks the model's behaviour, not its appearance.
const fs = require('node:fs');
const path = require('node:path');

const html = fs.readFileSync(
  path.join(__dirname, 'cc-composition-cli.html'),
  'utf8',
);
const script = html.split('<script>')[1].split('</script>')[0];

function el() {
  return {
    innerHTML: '',
    textContent: '',
    hidden: false,
    handlers: {},
    addEventListener(type, handler) {
      this.handlers[type] = handler;
    },
  };
}

const nodes = {};
for (const id of ['tabs', 'walkthrough', 'play', 'playTerminal', 'playLog', 'playState', 'playArtifacts']) {
  nodes[id] = el();
}

const document = {
  getElementById: (id) => nodes[id] || null,
  querySelectorAll: () => [],
};

const driver = `
const results = [];
function check(name, ok, detail) {
  results.push({ name, ok: Boolean(ok), detail: detail === undefined ? '' : String(detail) });
}

// Guided walkthroughs.
const snapshots = {};
for (const id of Object.keys(scenarios)) {
  resetScenario();
  selectScenario(id);
  const scenario = scenarios[id];
  const walked = [];
  let guard = 0;
  while (indexes[id] < scenario.steps.length - 1 && guard++ < 25) {
    nextStep();
    walked.push(indexes[id]);
  }
  scenario.steps[indexes[id]].apply();
  snapshots[id] = JSON.parse(JSON.stringify(state));
  check('scenario ' + id + ' has at least two steps', scenario.steps.length >= 2, scenario.steps.length);
  check('scenario ' + id + ' advances through every step', walked.length === scenario.steps.length - 1, walked.join(','));
  check('scenario ' + id + ' rendered a transcript', document.getElementById('walkthrough').innerHTML.includes('Proposed terminal'), document.getElementById('walkthrough').innerHTML.length);
}

check('compose: base adopted', snapshots.compose.base && snapshots.compose.base.name === 'agnostic-base', JSON.stringify(snapshots.compose.base));
check('compose: two overlays', snapshots.compose.overlays.length === 2, snapshots.compose.overlays.map((o) => o.name).join(','));
check('compose: named stack recorded', snapshots.compose.stack && snapshots.compose.stack.name === 'python-agentic', JSON.stringify(snapshots.compose.stack));
check('compose: task store preserved', snapshots.compose.tasks.length === 1, snapshots.compose.tasks.join(','));
check('compose: knowledge preserved', snapshots.compose.knowledge.length === 1, snapshots.compose.knowledge.join(','));

check('migrate: task imported', snapshots.migrate.importedTasks.length >= 1, snapshots.migrate.importedTasks.join(','));
check('migrate: backup created', Boolean(snapshots.migrate.backup), snapshots.migrate.backup);
check('migrate: existing task retained', snapshots.migrate.tasks.includes('TASK-1 Ship CLI'), snapshots.migrate.tasks.join(','));

check('reset: backup created', Boolean(snapshots.reset.backup), snapshots.reset.backup);
check('reset: workflow replaced', Boolean(snapshots.reset.workflow), snapshots.reset.workflow);
check('reset: code preserved', snapshots.reset.code.length === 1, snapshots.reset.code.join(','));
check('reset: knowledge preserved', snapshots.reset.knowledge.length === 1, snapshots.reset.knowledge.join(','));
check('reset: task history preserved', snapshots.reset.tasks.length === 1, snapshots.reset.tasks.join(','));

check('phone: three proposals', snapshots.phone.proposals.length === 3, snapshots.phone.proposals.length);
check('phone: one project-specific', snapshots.phone.proposals.filter((p) => p.kind === 'project-specific').length === 1);
check('phone: project-specific routed nowhere', snapshots.phone.proposals.find((p) => p.kind === 'project-specific').dest === 'none');
check('phone: only approved proposal published', snapshots.phone.proposals.filter((p) => p.status).length === 1, JSON.stringify(snapshots.phone.proposals.map((p) => p.status || 'unpublished')));

// Free play.
resetScenario();
showPlay();
check('play: starts uncomposed', state.base === null && state.overlays.length === 0);
op('python');
check('play: overlay refused without base', state.overlays.length === 0, document.getElementById('playTerminal').textContent.slice(0, 48));
op('base');
check('play: base adopted', state.base && state.base.name === 'agnostic-base');
op('python');
check('play: python overlay added', hasOverlay('python'));
op('agentic');
check('play: agentic overlay added', hasOverlay('agentic'));
op('phone');
check('play: phone explains nothing to send', document.getElementById('playTerminal').textContent.includes('no local improvements'), document.getElementById('playTerminal').textContent.slice(0, 48));
op('change');
op('phone');
check('play: phone splits proposals', state.proposals.length === 3, state.proposals.length);
op('migrate');
check('play: migrate quarantines', state.importedTasks.length === 1 && state.importedTasks[0].includes('quarantined'), state.importedTasks.join(','));
op('reset');
check('play: reset backs up', Boolean(state.backup));
check('play: state view rendered', document.getElementById('playState').textContent.includes('"project"'), document.getElementById('playState').textContent.slice(0, 32));
check('play: artifacts rendered', document.getElementById('playArtifacts').innerHTML.includes('Preserved'));
op('restart');
check('play: restart clears state', state.base === null && state.proposals.length === 0 && state.overlays.length === 0);

globalThis.__results = results;
`;

new Function('document', 'nodes_playTerminal_proxy', script + driver)(document, null);

const results = globalThis.__results;
const failed = results.filter((r) => !r.ok);
for (const r of results) {
  console.log(`${r.ok ? 'ok  ' : 'FAIL'}  ${r.name}${r.detail ? '  [' + r.detail + ']' : ''}`);
}
console.log(`\n${results.length - failed.length}/${results.length} checks passed`);
process.exit(failed.length === 0 ? 0 : 1);
