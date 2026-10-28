export const meta = {
  name: 'qa',
  description: 'QA: draft one unit test list and prove it red from the scratch folder, reading no implementation body',
  phases: [
    { title: 'Draft', detail: 'test list, interface note, red proof' },
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
const absent = ['unit', 'contract', 'repo', 'scratch', 'pluginRoot', 'sources', 'test.command']
  .filter(n => { const v = read(n); return v == null || v === '' || (n === 'test.command' && !(Array.isArray(v) && v.length)) })
if (absent.length) {
  log(`${a.unit}: missing required argument(s): ${absent.join(', ')}`)
  return { unit: a.unit, error: `missing required argument(s): ${absent.join(', ')}` }
}

const DRAFT_SCHEMA = {
  type: 'object',
  properties: {
    test_file: { type: 'string', description: 'repo-relative path of the drafted test file, forward slashes: where the Orchestrator will place it' },
    interface: { type: 'string', description: 'the interface the tests assume, complete enough for a developer who never reads the tests: commands, options, record keys, every printed line verbatim, exit codes, and what the tree prints' },
    tests: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          name: { type: 'string' },
          proves: { type: 'string', description: 'the check id, done_means, a ruling number, or an advisory letter' },
          intent: { type: 'string', description: 'one line: the behavior the test pins' },
        },
        required: ['name', 'proves', 'intent'],
      },
    },
    red_proof: {
      type: 'object',
      properties: {
        command: { type: 'string' },
        summary: { type: 'string', description: 'the summary line of the red run, verbatim' },
        every_failure_on_the_missing_behavior: { type: 'boolean', description: 'true only if every test fails, each on an assertion about the missing behavior, never on a fixture, import, build or collection error' },
        notes: { type: 'string' },
      },
      required: ['command', 'summary', 'every_failure_on_the_missing_behavior'],
    },
    details_fixed: { type: 'array', items: { type: 'string' }, description: 'each detail the sources left open that this list fixes, one line each, with the choice made' },
    questions: { type: 'array', items: { type: 'string' }, description: 'anything the sources and rulings do not decide and you could not settle; empty if none' },
  },
  required: ['test_file', 'interface', 'tests', 'red_proof', 'details_fixed', 'questions'],
}

const list = xs => (xs || []).map((x, i) => `${i + 1}. ${x}`).join('\n')
const wall = a.wall || {}
const paths = key => (wall[key] || []).join(' ') || 'none declared'
const oneFile = a.test.file ? a.test.file.join(' ') : 'none declared'
const build = a.test.build ? a.test.build.join(' ') : 'none declared'

const prompt = `You are the spec channel (G2.5) for unit "${a.unit}" of contract "${a.contract}", in the repository at ${a.repo}. You write the unit's tests. A separate developer agent writes the code later from your interface note alone, and never reads your tests, so the note must carry every name, option, printed line and exit code the tests depend on.

Rules:
- The repository is read-only for you: create, edit or delete nothing under ${a.repo}, and change no git state. Write only under ${a.scratch}.
- Every shell call is a single command: no pipes, no &&, no ;, no redirects. Run separate commands as separate calls.
- Run Python as python -m from the repository root, except prove.py, which runs by its path.
- Run every test and prove.py call in the foreground and set the Bash tool's timeout yourself: 600000 for prove.py, for several files or for the whole suite; 120000 for one test file. Never use run_in_background, and never read a task's output file to wait for it.
- The wall: read no file of these paths other than as said here. Never open the unit tests: ${paths('unit')}. Read only the interface of the code, never its body: the interface of a Python file comes from python -m taskcontract interface FILE; read whole only these interface files: ${paths('interface')}. The functional tests, which you write, stand at: ${paths('functional')}.

The repository's declared test commands, each an argv joined by single spaces:
- the whole suite: ${a.test.command.join(' ')}
- one test file ({file} stands for its repo-relative path): ${oneFile}
- the build, which runs before the one-file command: ${build}

Read first, in this order:
${list(a.sources)}

The list must pin:
- each acceptance_sketch line of unit ${a.unit}, and each sentence of its done_means;
- these rulings and readings, and these advisories carried from earlier rounds:
${list(a.pins)}

How to write it:
${list(a.notes)}
- Choose the test file's path, repo-relative with forward slashes, inside the wall's functional paths. Write the draft at ${a.scratch}/draft/ followed by that path. It will be placed at that path unchanged, so write it for that location. prove.py writes the conftest.py it runs the draft with; only the test file gets placed.
- Name each test for what it proves, with the check id first when it proves a sketch (for example test_sc3_2_...), so one check's tests can be selected by name.
- A test that passes before the code exists is a failed red. Assert the behavior itself, never only an exit code that the code today already returns.

Settle each of these open details and record the choice in details_fixed (these are suggestions; the sources win where they speak):
${list(a.open)}

Prove the list red with one command, from the repository root: python ${a.pluginRoot}/workflows/tools/prove.py --scratch ${a.scratch} --test PATH, where PATH is the path you chose. It exports HEAD, places the draft, runs the build and the test command, and prints one JSON line (the full output of each run is under ${a.scratch}/logs/, to read only for a failure the JSON does not explain). Red holds when red.red_ok reads true: every test fails, each on an assertion about the missing behavior. Fix the draft until that holds. Write no code of the unit: the QA verifier proves each pin later, by mutating the committed code.

Return the structured result. In interface, write the note the developer will get: the commands and their options, what each writes (keys and their values), every line printed verbatim with where it goes (stdout or stderr), the exit codes, and what the tree prints for each new state and piece of evidence. Run python -m taskcontract interface on each Python file you describe, so the signatures you give are the real ones.`

phase('Draft')
const draft = await agent(prompt, { label: `draft:${a.unit}`, phase: 'Draft', schema: DRAFT_SCHEMA, model: a.model, effort: a.effort })
if (!draft) {
  log(`${a.unit}: the QA agent returned nothing`)
  return { unit: a.unit, draft: null, error: 'the QA agent returned nothing', questions: [] }
}
log(`${a.unit}: ${draft.tests.length} tests; red: ${draft.red_proof.summary}`)
return { unit: a.unit, draft, questions: draft.questions || [] }
