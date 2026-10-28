export const meta = {
  name: 'qa-verifier',
  description: 'QA verifier: approve a drafted test list, prove it red, or prove each pin caught by a mutation; the verdict is computed from the receipts, not asserted',
  phases: [
    { title: 'Verify', detail: 'one task: approve-tests, prove-red or two-key' },
  ],
}

const a = args

const stop = (verdict, reasons) => ({ unit: a.unit, task: a.task, verdict, reasons, questions: [] })

// The agent model and effort come from the node's row in .sdlc/workflow.md,
// read by `python -m taskcontract node execution --print`; none is pinned here.
if (!a.model || !a.effort) {
  log(`${a.unit}: no model or effort given; pass both from the execution row`)
  return stop('INCOMPLETE', ['model and effort are required arguments'])
}

const TASKS = ['approve-tests', 'prove-red', 'two-key']
if (!TASKS.includes(a.task)) {
  log(`${a.unit}: task must be one of ${TASKS.join(', ')}`)
  return stop('INCOMPLETE', [`task must be one of ${TASKS.join(', ')}`])
}

const REQUIRED = {
  'approve-tests': ['unit', 'contract', 'repo', 'scratch', 'testFile', 'contractPath', 'requestPath', 'draft'],
  'prove-red': ['unit', 'contract', 'repo', 'scratch', 'testFile', 'pluginRoot'],
  'two-key': ['unit', 'contract', 'repo', 'scratch', 'testFile', 'pluginRoot', 'commit', 'contractPath', 'requestPath'],
}
const absent = REQUIRED[a.task].filter(n => a[n] == null || a[n] === '')
if (absent.length) {
  log(`${a.unit}: missing required argument(s): ${absent.join(', ')}`)
  return stop('INCOMPLETE', [`missing required argument(s): ${absent.join(', ')}`])
}

const APPROVE_SCHEMA = {
  type: 'object',
  properties: {
    sketches: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          sketch: { type: 'string', description: 'the acceptance_sketch line, verbatim' },
          pinned: { type: 'boolean', description: 'true only if at least one test fails when this line stops being true' },
          tests: { type: 'array', items: { type: 'string' }, description: 'the names of the tests that pin it' },
          note: { type: 'string' },
        },
        required: ['sketch', 'pinned', 'tests'],
      },
    },
    done_means_held: { type: 'boolean', description: 'true only if every sentence of done_means is pinned by a test' },
    defects: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          severity: { type: 'string', enum: ['blocking', 'advisory'] },
          description: { type: 'string' },
        },
        required: ['severity', 'description'],
      },
    },
    questions: { type: 'array', items: { type: 'string' }, description: 'anything the sources do not decide and you could not settle; empty if none' },
    summary: { type: 'string' },
  },
  required: ['sketches', 'done_means_held', 'defects', 'questions', 'summary'],
}

const PROVE_SCHEMA = {
  type: 'object',
  properties: {
    command: { type: 'string' },
    exit_code: { type: 'integer', description: 'the exit code of the command, as the shell reported it' },
    output: { type: 'string', description: 'the JSON line the command printed, verbatim' },
    red_summary: { type: 'string', description: 'red.summary from that JSON' },
  },
  required: ['command', 'exit_code', 'output', 'red_summary'],
}

const MUTATE_SCHEMA = {
  type: 'object',
  properties: {
    command: { type: 'string' },
    exit_code: { type: 'integer', description: 'the exit code of the command, as the shell reported it' },
    output: { type: 'string', description: 'the JSON line the command printed, verbatim' },
    mutations: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          name: { type: 'string' },
          behavior: { type: 'string', description: 'the behavior this mutation defeats, in words, never the code' },
          applied: { type: 'boolean', description: 'applied from the JSON' },
          caught: { type: 'boolean', description: 'true only if caught_by in the JSON lists at least one test' },
        },
        required: ['name', 'behavior', 'applied', 'caught'],
      },
    },
    questions: { type: 'array', items: { type: 'string' }, description: 'anything you could not settle; empty if none' },
  },
  required: ['command', 'exit_code', 'output', 'mutations', 'questions'],
}

const RULES = [
  `You are the QA verifier for unit "${a.unit}" of contract "${a.contract}", in the repository at ${a.repo}. You never write the tests or the code.`,
  `The repository is read-only for you: create, edit or delete nothing under ${a.repo}, and change no git state. Write only under ${a.scratch}.`,
  'Every shell call is a single command: no pipes, no &&, no ;, no redirects. Run separate commands as separate calls.',
  'Run every test and prove.py call in the foreground and set the Bash tool timeout yourself: 600000 for prove.py. Never use run_in_background, and never read a task\'s output file to wait for it.',
].join('\n')

const prove = a.task === 'approve-tests' ? '' : `python ${a.pluginRoot}/workflows/tools/prove.py --scratch ${a.scratch} --test ${a.testFile}`

const PROMPTS = {
  'approve-tests': () => `${RULES}

Approve one drafted test list. The QA agent returned this draft:
${JSON.stringify(a.draft)}

Read, in this order:
1. ${a.contractPath}: find the unit with id "${a.unit}". Its acceptance_sketch lines and done_means are what the tests must pin.
2. ${a.requestPath}: the feature document; read the checks its sketches point at.${a.designPath ? `\n3. ${a.designPath}: the design document, for the interfaces the tests assume.` : ''}
${a.designPath ? '4' : '3'}. The draft test file at ${a.scratch}/draft/${a.testFile}.

Decide:
- For each acceptance_sketch line, pinned is true only if at least one test fails when that line stops being true. Name the tests.
- done_means_held is true only if every sentence of done_means is pinned.
- defects: a test that cannot fail, a test that asserts only what the code today already does, a pinned behavior the sources do not state. Use blocking for a sketch or sentence left unpinned or a test that pins a wrong behavior; advisory for wording.
Do not run the tests: prove-red is the next task. Be strict: if you are unsure a sketch is pinned, it is not.`,

  'prove-red': () => `${RULES}

Prove the placed draft red. From the repository root run this one command, once:
${prove}
It exports HEAD, places the draft from ${a.scratch}/draft/${a.testFile}, runs the build and the test command, and prints one JSON line. Report the command, its exit code as the shell gave it, the JSON line verbatim as output, and red.summary as red_summary. Do not fix the draft and do not run anything else: the verdict is computed from the exit code.`,

  'two-key': () => `${RULES}

Prove that every pinned behavior is caught, on an export of commit ${a.commit}. Read ${a.contractPath} for unit "${a.unit}" and ${a.requestPath} for the checks its sketches point at, then the unit's files in the commit (git show --stat ${a.commit}, then git show for each file).
Write ${a.scratch}/mutations.json: a JSON list of at least 4 {name, file, old, new}, each one line of the committed code broken to defeat one pinned behavior (file is relative to the repository root; old must match exactly one place in it). Then, from the repository root, run this one command:
${prove} --at ${a.commit} --mutations ${a.scratch}/mutations.json
It prints one JSON line (the full output of each run is under ${a.scratch}/logs/). Report the command, its exit code as the shell gave it, the JSON line verbatim as output, and one entry for each mutation: its name, the behavior it defeats in words (never the code), applied, and caught (true only if caught_by lists a test). Do not fix anything: the verdict is computed from the exit code and the entries.`,
}

const SCHEMAS = { 'approve-tests': APPROVE_SCHEMA, 'prove-red': PROVE_SCHEMA, 'two-key': MUTATE_SCHEMA }

phase('Verify')
const reply = await agent(PROMPTS[a.task](), { label: `${a.task}:${a.unit}`, phase: 'Verify', schema: SCHEMAS[a.task], model: a.model, effort: a.effort })
if (!reply) {
  log(`${a.unit}: the QA verifier returned nothing`)
  return { ...stop('INCOMPLETE', ['the QA verifier returned nothing']), ...(a.task === 'two-key' ? { mutations: { caught: 0, total: 0 } } : {}) }
}

const questions = reply.questions || []
let verdict = 'PASS'
const reasons = []
let extra = {}

if (a.task === 'approve-tests') {
  for (const s of reply.sketches.filter(s => !s.pinned)) reasons.push(`Sketch not pinned: ${s.sketch}`)
  if (!reply.done_means_held) reasons.push('done_means is not pinned in every sentence')
  for (const d of reply.defects.filter(d => d.severity === 'blocking')) reasons.push(`Blocking defect: ${d.description}`)
  if (reasons.length) verdict = 'FAIL'
} else if (a.task === 'prove-red') {
  if (reply.exit_code === 254) {
    verdict = 'INCOMPLETE'
    reasons.push('the test command never started (prove.py exit 254)')
  } else if (reply.exit_code !== 0) {
    verdict = 'FAIL'
    reasons.push(`prove.py exited ${reply.exit_code}: ${reply.red_summary || reply.output}`)
  }
} else {
  const total = reply.mutations.length
  const caught = reply.mutations.filter(m => m.applied && m.caught).length
  extra = { mutations: { caught, total } }
  if (reply.exit_code === 254) {
    verdict = 'INCOMPLETE'
    reasons.push('the test command never started (prove.py exit 254)')
  } else {
    if (reply.exit_code !== 0) reasons.push(`prove.py exited ${reply.exit_code}`)
    if (total < 4) reasons.push(`${total} mutations written; 4 are needed`)
    for (const m of reply.mutations.filter(m => !(m.applied && m.caught))) reasons.push(`Mutation not caught: ${m.behavior}`)
    if (reasons.length) verdict = 'FAIL'
  }
}

log(`${a.unit}: ${a.task}: ${verdict}${reasons.length ? ' - ' + reasons.join('; ') : ''}`)
return { unit: a.unit, task: a.task, verdict, reasons, questions, ...extra }
