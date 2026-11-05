export default function How() {
  return (
    <section>
      <div className="intro"><h2>How HarvestProof works</h2><p>Plain answers to what each part does, and what it does not do.</p></div>
      <div className="col">
        <div className="card"><h3>Ask by voice, answer in Tamil</h3><p>Press the microphone and say what you see, in Tamil or English: “My chilli leaves have white powder.” Your browser turns the speech into text. We read the words, find the crop and the symptoms (including “no rain” or “not sure”), and work out the likely problem. If we are not sure, we ask a simple yes/no question out loud, in Tamil, and you answer “ஆம்” or “இல்லை”. The answer is shown on screen and can be read aloud in Tamil.</p>
          <p className="sm mu">Voice works in Chrome on Android and on computers, over https or localhost. Reading aloud in Tamil needs a Tamil voice on the phone. If your phone has none, the answer is still shown on screen. Tamil terms were written by an AI and should be checked by an agriculture officer.</p></div>
        <div className="card"><h3>The leaf check (not a neural network)</h3><p>The photo is split into leaf, spots, yellow and white areas. We measure how many spots there are and whether they are long and thin or round. A trained model turns those measurements into probabilities. Your answers, spoken or tapped, are added as extra evidence, and we always ask the question that removes the most doubt. If the evidence is not clear we say <b>uncertain</b> instead of guessing.</p><p className="sm mu">Photo analysis exists for <b>tea</b> and <b>chilli</b>, trained on public photos. Rice and grapes use your answers only, because we do not have photos for them yet.</p></div>
        <div className="card"><h3>The pack check</h3><p>Each pack code ends in a signature that only the issuer can create, so forged or mistyped codes fail. We also check the batch is registered and in date, and flag a code that has been scanned in many districts within a short time, which suggests copies.</p></div>
        <div className="card"><h3>The spray options</h3><p>Products and waiting periods come from India's official list of registered pesticide uses. We only show products whose label names your problem on your crop, drop those that would make you harvest too early, and avoid repeating the same mode of action (this slows resistance).</p></div>
        <div className="card"><h3>The passport</h3><p>Safe harvest day = last spray date + the longest label waiting period. It also warns when the EU limit for a product is very strict, because meeting India's waiting period does not guarantee passing an EU residue test.</p></div>
        <div className="card"><h3>Words used here</h3><p><b>Waiting period:</b> days that must pass between the last spray and harvest. <b>Mode of action:</b> how a chemical kills the disease. Using the same one repeatedly makes diseases resistant. <b>Residue limit (MRL):</b> the most chemical allowed on food that is sold.</p></div>
        <div className="card"><h3>What it is not</h3><p>It is advice, not a laboratory certificate, and not a replacement for an agriculture officer. Photo accuracy is measured on public dataset photos and will be lower on your own field photos. Label data was transcribed from official lists and must be checked against the product label.</p></div>
      </div>
    </section>
  )
}
