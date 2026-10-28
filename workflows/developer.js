export const meta = {
  name: 'developer',
  description: 'Developer: make one unit placed tests green from its interface note, without opening the functional tests',
  phases: [
    { title: 'Green', detail: 'implement to the interface note; the suite green' },
  ],
}

const a = args

// The agent model and effort come from the node's row in .sdlc/workflow.md,
// read by `python -m taskcontract node execution --print`; none is pinned here.
if (!a.model || !a.effort) {
  log(`${a.unit}: no model or effort given; pass both from the execution row`)
  return { unit: a.unit, error: 'model and effort are required arguments' }
}

// A required argument is absent when it is null or empty; test.command is a
// list, and an empty one declares nothing.
const read = name => name.split('.').reduce((o, k) => (o == null ? o : o[k]), a)
const absent = ['unit', 'contract', 'repo', 'branch', 'testFile', 'scratchRoot', 'files', 'sources', 'interface', 'test.command']
  .filter(n => { const v = read(n); return v == null || v === '' || (n === 'test.command' && !(Array.isArray(v) && v.length)) })
if (absent.length) {
  log(`${a.unit}: missing required argument(s): ${absent.join(', ')}`)
  return { unit: a.unit, error: `missing required argument(s): ${absent.join(', ')}` }
}

const DEV_SCHEMA = {
  type: 'object',
  properties: {
    files_changed: { type: 'array', items: { type: 'string' } },
    summary: { type: 'string', description: 'what changed, file by file, in a few lines' },
    suite: { type: 'string', description: 'the last line of the whole command\'s run, verbatim' },
    deviations: { type: 'array', items: { type: 'string' }, description: 'each place the code departs from the interface note, and why; empty if none' },
    questions: { type: 'array', items: { type: 'string' }, description: 'anything the note and the sources left undecided; empty if none' },
  },
  required: ['files_changed', 'summary', 'suite', 'deviations', 'questions'],
}

const list = xs => xs.map((x, i) => `${i + 1}. ${x}`).join('\n')

const functional = (a.wall && a.wall.functional && a.wall.functional.length ? a.wall.functional : []).join(' ') || 'none declared'
const whole = a.test.command.join(' ')
const build = a.test.build ? a.test.build.join(' ') : 'none declared'

const prompt = `You are the developer (G3) for unit "${a.unit}" of contract "${a.contract}", in the repository at ${a.repo}, on branch ${a.branch}. The spec channel has placed the unit's tests at ${a.testFile}, and they fail today. Make them pass by changing the code, working from the interface note below.

Rules:
- Never open, read, search or edit any of these files: ${functional}. Never read anything under ${a.scratchRoot}. You may run the tests and read the test output.
- Change only these files: ${a.files.join(', ')}. Create a file only when it is on that list; create no other.
- Change no git state: no add, commit, stash, checkout, reset, or branch.
- Every shell call is a single command: no pipes, no &&, no ;, no redirects. Run separate commands as separate calls.
- Run every test call in the foreground and set the Bash tool's timeout yourself: 600000. Never use run_in_background, and never read a task's output file to wait for it.
- Never run one test file alone: the wall hook refuses any command that names a path behind the functional wall. Run the build, when declared, then the whole command.
- No new dependency. Match the surrounding code: its comment density, naming and idiom, and its docstrings' register.

The repository's declared test commands, each an argv joined by single spaces:
- the whole command: ${whole}
- the build, which runs before the whole command: ${build}

Read first:
${list(a.sources)}

The interface note (the tests assume exactly this):
${a.interface}

Done means: ${whole} passes whole. Run it from the repository root, then return the structured result.`

phase('Green')
const dev = await agent(prompt, { label: `green:${a.unit}`, phase: 'Green', schema: DEV_SCHEMA, model: a.model, effort: a.effort })
if (!dev) {
  log(`${a.unit}: the developer returned nothing`)
  return { unit: a.unit, dev: null, error: 'the developer returned nothing', questions: [] }
}
log(`${a.unit}: suite: ${dev.suite}; ${dev.deviations.length} deviation(s)`)
return { unit: a.unit, dev, questions: dev.questions || [] }
