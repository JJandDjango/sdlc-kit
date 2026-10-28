export const meta = {
  name: 'dev-verifier',
  description: 'Dev verifier: a zero-trust grade for one contract unit on the receipts receipts.py ran; the verdict is computed, not asserted',
  phases: [
    { title: 'Grade', detail: 'zero-trust reading of the unit commit against its sketches' },
  ],
}

const a = args

const GRADE_SCHEMA = {
  type: 'object',
  properties: {
    commit_checked: { type: 'string' },
    files_in_commit: { type: 'array', items: { type: 'string' } },
    trailers: {
      type: 'object',
      properties: {
        contract_trailer: { type: 'string' },
        theory_trailer_present: { type: 'boolean' },
        contract_trailer_in_final_paragraph: { type: 'boolean' },
      },
      required: ['contract_trailer', 'theory_trailer_present'],
    },
    every_path_inside_scope_or_free: { type: 'boolean' },
    sketches: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          sketch: { type: 'string' },
          verdict: { type: 'string', enum: ['PASS', 'FAIL'] },
          evidence: { type: 'string', description: 'file:line and the words or behavior that decide it' },
        },
        required: ['sketch', 'verdict', 'evidence'],
      },
    },
    done_means_held: { type: 'boolean' },
    defects: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          severity: { type: 'string', enum: ['blocking', 'advisory'] },
          file: { type: 'string' },
          line: { type: 'integer' },
          description: { type: 'string' },
        },
        required: ['severity', 'file', 'description'],
      },
    },
    questions: { type: 'array', items: { type: 'string' }, description: 'anything the sources do not decide and you could not settle; empty if none' },
    summary: { type: 'string' },
  },
  required: ['commit_checked', 'files_in_commit', 'trailers', 'every_path_inside_scope_or_free', 'sketches', 'done_means_held', 'defects', 'summary'],
}

// The agent model and effort come from the node's row in .sdlc/workflow.md,
// read by `python -m taskcontract node execution --print`; none is pinned here.
if (!a.model || !a.effort) {
  log(`${a.unit}: no model or effort given; pass both from the execution row`)
  return { unit: a.unit, verdict: 'INCOMPLETE', reasons: ['model and effort are required arguments'], questions: [] }
}

const absent = ['unit', 'contract', 'repo', 'branch', 'commit', 'contractPath', 'requestPath', 'receiptsResult']
  .filter(n => a[n] == null || a[n] === '')
if (absent.length) {
  log(`${a.unit}: missing required argument(s): ${absent.join(', ')}`)
  return { unit: a.unit, verdict: 'INCOMPLETE', reasons: [`missing required argument(s): ${absent.join(', ')}`], questions: [] }
}

const focus = a.focus || []
const freePaths = a.freePaths || 'none'
const plural = (n, one, many) => `${n} ${n === 1 ? one : many}`

const RULES = [
  'You are read-only. Do not edit, create, stage, commit, push, or delete anything. Do not switch branches.',
  'Every shell call is a single command: no pipes, no &&, no ;, no redirects. Run separate commands as separate calls.',
  `Work in the repository at ${a.repo} (it is on branch ${a.branch}). Use python -m from the repository root so the checkout, not an installed copy, is what runs.`,
].join('\n')

// The blocking bar: the wrap files are session scratch, rewritten at every
// wrap, so a defect in one never gates a unit; and the repo-wide stale-claim
// sweep runs once, in the unit called with sweep: true, not in every unit.
const WRAP_FILES = ['plan.md', 'plan.workflow.json', 'STATE.md']
const wrapList = `${WRAP_FILES.slice(0, -1).join(', ')} and ${WRAP_FILES[WRAP_FILES.length - 1]}`
const sweepRule = a.sweep === true
  ? 'This unit owns the one repo-wide sweep: search every tracked file (git grep, one call per pattern) for a statement of a rule this contract retired or changed, and file each one on a shipped surface as a blocking defect.'
  : 'Do not search files this commit does not touch for statements the change made stale: that sweep runs once, in the release unit. A stale statement you meet in a file outside this commit is advisory.'

const reads = [
  `${a.contractPath}: find the unit with id "${a.unit}". Its done_means and its acceptance_sketch lines are what you grade. Read the contract's scope and non_goals too.`,
  `${a.requestPath}: the feature document. The check ids in parentheses at the end of a sketch (for example SC5.3) point at the checks under "Acceptance criteria"; read those checks, the "Error messages, verbatim" section, and the "Constraints" section.`,
  ...(a.designPath ? [`${a.designPath}: the design document, for the interfaces and rulings this work implements.`] : []),
  'Each commit listed above, by its own sha: git show --stat <sha> ; git show <sha> ; git show -s --format=%B <sha> (three separate calls per commit).',
]

const gradePrompt = `${RULES}

You are the zero-trust grader of a Two-Key verification. Grade ONE unit of work: unit "${a.unit}" of contract "${a.contract}", delivered by commit(s) ${a.commit}. When more than one commit is listed, the later ones are fixes from an earlier verification round: read every one, and grade the tree as it stands at HEAD. Do not trust the commit message, the author, or any claim of correctness: decide everything from the files and from git.

Read, in this order:
${reads.map((r, i) => `${i + 1}. ${r}`).join('\n')}

Grade:
- One verdict per acceptance_sketch line, PASS or FAIL, with file:line evidence from the tree at HEAD. A sketch passes only if what it says is true in the files now.
- done_means_held: true only if every sentence of the unit's done_means is true now.
- every_path_inside_scope_or_free: every path the commit touches must match an entry of the contract's scope, or be a free path (${freePaths}). Paths under specs/ are governed separately; report them but do not fail on them.
- trailers: the commit must carry "Contract: ${a.contract}" and a "Theory:" trailer in the final paragraph. Git only parses trailers from the final paragraph, so check that both lines sit in it.
- defects: anything wrong that the sketches do not cover. Use "blocking" only for a false statement on a shipped surface, a broken promise of the contract, a constraint violated, or a change outside the unit's purpose; use "advisory" for wording or polish. A shipped surface is any tracked file except ${wrapList}, so it covers the code, the schema, docs/, USAGE.md and CHANGELOG.md. ${wrapList} are session scratch, rewritten at every wrap: a defect in one of them is advisory, never blocking. For every factual claim the commit adds about how the kit behaves, verify the claim against the code and cite file:line; a claim you cannot verify is a defect.
- ${sweepRule}
- questions: anything the sources and the contract do not decide and you could not settle; empty if none.

Where the evidence for the sketches lives (pointers only: they add no requirement beyond the sketches, done_means, scope and trailers):
${focus.map((f, i) => `${i + 1}. ${f}`).join('\n')}

Be strict. If you are unsure whether something holds, it does not pass.`

// receiptsResult is the JSON object receipts.py printed in the session (a script
// cannot read files, so it arrives inline in args). The verdict below reads the
// script's own exit codes: its `ok` field is never trusted. A result that is
// not receipts.py's shape reads as no receipts.
const given = a.receiptsResult
const receipts = !!given && Array.isArray(given.commands) && given.commands.length > 0
  && given.commands.every(c => Number.isInteger(c.exit_code)) ? given : null
phase('Grade')
const grade = await agent(gradePrompt, { label: `grade:${a.unit}`, phase: 'Grade', schema: GRADE_SCHEMA, model: a.model, effort: a.effort })

const failedCommands = receipts ? receipts.commands.filter(c => c.exit_code !== 0) : []
const failedSketches = grade ? grade.sketches.filter(s => s.verdict !== 'PASS') : []
// The grader names a file in its own form (relative, ./-prefixed, absolute,
// with a :line suffix), so normalize it before matching against WRAP_FILES.
const repoPrefix = `${a.repo.replace(/\\/g, '/').replace(/\/+$/, '')}/`.toLowerCase()
const isWrapFile = file => {
  let f = (file || '').trim().replace(/\\/g, '/').replace(/:\d+(-\d+)?$/, '').toLowerCase()
  if (f.startsWith(repoPrefix)) f = f.slice(repoPrefix.length)
  f = f.replace(/^\.\//, '')
  return WRAP_FILES.some(w => w.toLowerCase() === f)
}
const defects = grade ? grade.defects : []
const demoted = defects.filter(d => d.severity === 'blocking' && isWrapFile(d.file))
const blocking = defects.filter(d => d.severity === 'blocking' && !isWrapFile(d.file))
const advisories = defects.filter(d => d.severity === 'advisory').concat(demoted)

let verdict = 'PASS'
const reasons = []
if (!receipts) { verdict = 'INCOMPLETE'; reasons.push('receiptsResult is not a receipts.py result') }
if (!grade) { verdict = 'INCOMPLETE'; reasons.push('the grader returned nothing') }
if (failedCommands.length) { verdict = 'FAIL'; reasons.push(`${plural(failedCommands.length, 'receipt command', 'receipt commands')} exited non-zero`) }
if (failedSketches.length) { verdict = 'FAIL'; reasons.push(`${plural(failedSketches.length, 'sketch', 'sketches')} failed`) }
if (blocking.length) { verdict = 'FAIL'; reasons.push(plural(blocking.length, 'blocking defect', 'blocking defects')) }
if (grade && !grade.done_means_held) { verdict = 'FAIL'; reasons.push('done_means does not hold') }
if (grade && !grade.every_path_inside_scope_or_free) { verdict = 'FAIL'; reasons.push('a path outside scope') }
// The grader answers this field in its own words (the bare id, the whole
// "Contract: <id>" line, or that line with a remark after it), so extract the
// first contract-id-shaped token after an optional "Contract:" prefix.
const trailerText = grade ? grade.trailers.contract_trailer : ''
const explicitId = trailerText.match(/Contract:\s*([a-z][a-z0-9-]{2,63})/i)
const bareId = trailerText.trim().match(/^([a-z][a-z0-9-]{2,63})$/)
const trailerId = explicitId ? explicitId[1] : (bareId ? bareId[1] : '')
if (grade && trailerId !== a.contract) { verdict = 'FAIL'; reasons.push(`Contract trailer missing or wrong (got "${grade.trailers.contract_trailer}")`) }
if (grade && !grade.trailers.theory_trailer_present) { verdict = 'FAIL'; reasons.push('Theory trailer missing') }

if (demoted.length) log(`${a.unit}: ${plural(demoted.length, 'blocking defect', 'blocking defects')} in the wrap files counted as advisory`)
log(`${a.unit}: ${verdict}${reasons.length ? ' - ' + reasons.join('; ') : ''}`)

const questions = grade ? (grade.questions || []) : []
return { unit: a.unit, commit: a.commit, verdict, reasons, questions, failedCommands, failedSketches, blocking, advisories, demoted, receipts, grade }
