export const meta = {
  name: 'test-retirer',
  description: 'Spec channel: retire the tests that pin code a unit deletes, found by deleting the code in an export and reading only the tests that fail',
  phases: [
    { title: 'Retire', detail: 'delete the code in an export, run the suite, classify each failing test' },
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
const absent = ['unit', 'contract', 'repo', 'scratch', 'test.command']
  .filter(n => { const v = read(n); return v == null || v === '' || (n === 'test.command' && !(Array.isArray(v) && v.length)) })
if (absent.length) {
  log(`${a.unit}: missing required argument(s): ${absent.join(', ')}`)
  return { unit: a.unit, error: `missing required argument(s): ${absent.join(', ')}` }
}

const RETIRE_SCHEMA = {
  type: 'object',
  properties: {
    deleted: { type: 'array', items: { type: 'string' }, description: 'each name deleted from the export, as file:name, or each file overlaid on it' },
    suite_with_deletion: { type: 'string', description: 'the last line of the test command\'s output with the code deleted or overlaid and no test amended, verbatim' },
    suite_with_amendments: { type: 'string', description: 'the last line of the test command\'s output with the code deleted or overlaid and the amended modules in place, verbatim' },
    tests: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          module: { type: 'string' },
          test: { type: 'string' },
          fate: { type: 'string', enum: ['retired', 'amended'] },
          pinned: { type: 'string', description: 'one line: the behavior the test pinned' },
          why: { type: 'string', description: 'one line: why it retires, or what the amendment changes' },
        },
        required: ['module', 'test', 'fate', 'pinned', 'why'],
      },
    },
    amended_modules: { type: 'array', items: { type: 'string' }, description: 'absolute paths of the amended module copies under the scratch folder' },
    notes: { type: 'string' },
  },
  required: ['deleted', 'suite_with_deletion', 'suite_with_amendments', 'tests', 'amended_modules'],
}

const list = xs => xs.map((x, i) => `${i + 1}. ${x}`).join('\n')
const command = a.test.command.join(' ')

// An overlay replaces code in place of deleting names: for a unit whose
// retirement flips values on existing fixtures, with no name to delete.
const change = a.overlay
  ? `2. In the export, copy each of these files over its counterpart, and change nothing else:
${list(a.overlay)}
   They carry the unit's new behavior; a test that fails now pinned the behavior they replace.`
  : `2. In the export, delete exactly these names and nothing else, with any import of them inside the same file:
${list(a.deletions)}
   Keep every other name, even one that looks unused: ${a.keep}`

const prompt = `You are the spec channel for one step of unit "${a.unit}" of contract "${a.contract}", in the repository at ${a.repo}: retiring the tests that pin code the unit deletes or replaces. A developer changes the code later; you only prepare the tests.

Rules:
- The repository is read-only for you: create, edit or delete nothing under ${a.repo}, and change no git state (no worktree, stash, checkout or branch). Write only under ${a.scratch}.
- Every shell call is a single command: no pipes, no &&, no ;, no redirects. Run separate commands as separate calls.
- Run the test command in the foreground and set the Bash tool's timeout yourself: 600000. Never use run_in_background, and never read a task's output file to wait for it.
- Keep your reading narrow: never read a test module whole. Read only the test functions that fail, and the module-level lines (imports, helpers) they depend on.

Steps:
1. Export HEAD: git -C ${a.repo} archive --format=tar -o ${a.scratch}/head.tar HEAD, then extract it into ${a.scratch}/kit (tar -xf ${a.scratch}/head.tar -C ${a.scratch}/kit, after creating the folder).
${change}
3. Run the declared test command from the export root ${a.scratch}/kit, in the foreground, with the Bash tool's timeout at 600000: ${command}. It takes one to three minutes. Record the last line of its output verbatim as suite_with_deletion.
4. For each failing or erroring test, read that test only and decide its fate:
   - retired: it pins the deleted or replaced code's own behavior (${a.retiredMeans}). Remove the test.
   - amended: it pins something that still holds, and only touched the deleted or replaced code on the way (an import, a callable() check, one render used to read a line). Change as little as possible to keep what it pins.
   A module that fails at collection because it imports a deleted name: fix the import, then classify each test that used the name.
5. Write each changed module whole, same file name, to ${a.scratch}/amend/, copied from the export and changed only as step 4 says.
6. Copy the amended modules over the export's tests and run the declared test command again the same way; every test must pass. Record the last line of its output as suite_with_amendments.${a.overlay ? '\n   An amended assertion takes the new value the overlaid code gives on the same fixture, and keeps what it pinned otherwise.' : ''}

Context for your decisions:
${list(a.context || [])}

Return the structured result.`

phase('Retire')
const result = await agent(prompt, { label: `retire:${a.unit}`, phase: 'Retire', schema: RETIRE_SCHEMA, model: a.model, effort: a.effort })
if (!result) {
  log(`${a.unit}: the retirer returned nothing`)
  return { unit: a.unit, retire: null, error: 'the retirer returned nothing' }
}
log(`${a.unit}: ${result.tests.length} tests; deleted: ${result.suite_with_deletion}; amended: ${result.suite_with_amendments}`)
return { unit: a.unit, retire: result }
