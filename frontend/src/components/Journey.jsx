const LABELS = [['Check the leaf', 'What is wrong?'], ['Check the pack', 'Is it genuine?'], ['Choose the spray', 'What fits?'], ['Passport', 'When is it safe?']]

export default function Journey({ step, setStep, done }) {
  return (
    <nav className="journey" aria-label="Steps">
      {LABELS.map(([t, s], i) => (
        <button type="button" key={t} className={`${step === i + 1 ? 'on' : ''} ${done[i] ? 'done' : ''}`} aria-current={step === i + 1 ? 'step' : undefined} onClick={() => setStep(i + 1)}>
          <span className="n">{done[i] ? '✓' : i + 1}</span><span><b>{t}</b><small>{s}</small></span>
        </button>
      ))}
    </nav>
  )
}
