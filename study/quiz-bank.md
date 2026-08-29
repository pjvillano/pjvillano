# Quiz Bank: Quantum Computing & Photonic Interconnects

Scenario-based questions, grouped by module (see `study/curriculum.md`).
Each question has a short explanation with the answer — read it even if you
got the question right, it usually carries the real lesson.

---

## Module 1 — Quantum Computing Fundamentals

**1.** A vendor claims their new chip has "1000 qubits" and is more
powerful than a 100-qubit competitor. What single additional number would
most change your assessment, and why?
> **Answer:** Two-qubit gate error rate (or equivalently, quantum volume /
> effective circuit depth before noise dominates). Raw qubit count without
> connectivity and gate fidelity tells you almost nothing about what
> circuits the device can actually run — a noisy 1000-qubit device can be
> less useful than a clean 100-qubit one.

**2.** You're deciding between running an algorithm on today's hardware now
(NISQ, variational approach) vs. waiting for fault-tolerant hardware. What
determines which is the right call?
> **Answer:** Whether the algorithm's advantage requires deep circuits
> (many sequential gates) that noise will wash out before completion. Short,
> shallow-circuit, hybrid classical-quantum algorithms (VQE/QAOA-style) can
> extract value now; algorithms needing long coherent circuit depth (e.g.
> full Shor's algorithm at cryptographically relevant sizes) need
> fault tolerance.

**3.** A colleague says "T2 = 100 µs, so we have 100 µs to run our
algorithm." What's wrong with that framing?
> **Answer:** T2 sets an upper bound on how long the qubit's phase
> coherence survives idle, but actual usable circuit time is much shorter
> once you account for gate durations, gate error accumulation (which
> compounds per-gate, not just from idle dephasing), and readout — the
> practical constraint is usually circuit depth × gate error, not raw T2.

---

## Module 2 — Distributed Quantum Computing

**4.** Two quantum processors, A and C, need to become entangled, but
there's no direct physical link between them — only A-B and B-C links
exist. What technique lets you entangle A and C, and what's the key
operation performed at B?
> **Answer:** Entanglement swapping. A Bell-state measurement is performed
> at B on its two halves of the A-B and B-C entangled pairs, which
> (conditioned on classical communication of the result) leaves A and C
> entangled even though they never directly interacted.

**5.** Your two nodes generate entangled pairs at high rate but each pair
has only 70% fidelity, and your application needs ≥95% fidelity to run
correctly. What's the standard technique to fix this, and what do you give
up?
> **Answer:** Entanglement purification (e.g. BBPSSW/DEJMPS): consume
> multiple low-fidelity pairs to distill fewer high-fidelity pairs. The
> cost is throughput — you trade raw entanglement-generation rate for
> usable-entanglement fidelity.

**6.** You're designing a 500 km quantum link. Direct photon transmission
loss makes the success probability of end-to-end entanglement generation
vanishingly small. Why doesn't simply "boosting laser power" fix this the
way it might in classical optical networking, and what's the actual fix?
> **Answer:** Quantum information can't be amplified without violating the
> no-cloning theorem (a classical optical amplifier would have to measure
> and copy the quantum state, destroying it) — you can't just boost signal
> and re-amplify. The fix is quantum repeaters: break the link into shorter
> segments, generate/store entanglement locally per segment, and swap
> segment-by-segment so loss scales with segment length, not total distance.

**7.** A team proposes building a distributed quantum computer by
teleporting qubits between two processing nodes for every two-qubit gate
that spans the nodes. What do they need to have already established before
each teleportation-based remote gate, and why can't it happen faster than
light?
> **Answer:** They need a pre-shared entangled pair between the two nodes
> before each remote operation, plus a classical channel to communicate
> measurement results — teleportation reconstructs state using classical
> bits sent at or below light speed, so the overall protocol is bounded by
> classical communication latency, not instantaneous.

---

## Module 3 — Photonic Interconnects

**8.** You need to link two ion-trap processing nodes 2 km apart over
standard telecom fiber. The ions natively emit photons at 493 nm (visible),
which has fiber loss around 3 dB/km. What two techniques would you combine
to make this link practical, and why?
> **Answer:** (1) Frequency conversion of the 493 nm photon to a telecom
> band (~1550 nm, ~0.2 dB/km) to cut loss by roughly an order of magnitude
> per km; (2) entanglement purification and/or a repeater architecture if
> the resulting rate is still too low for the target fidelity/throughput —
> at just 2 km direct transmission with conversion may suffice, but the
> conversion step is close to mandatory given the native-wavelength loss.

**9.** Between polarization encoding and time-bin encoding, which would you
choose for a qubit traveling tens of km through standard (non-polarization-
maintaining) deployed fiber, and why?
> **Answer:** Time-bin encoding — standard deployed fiber causes
> polarization drift over distance/temperature that requires active,
> continuous compensation for polarization-encoded qubits, while time-bin
> encoding (relative arrival time between two pulses) is inherently robust
> to that drift, at the cost of needing stable interferometers at each end.

**10.** A photon detector reports 40% overall system detection efficiency
in your entanglement-distribution experiment. Your collaborator says "let's
just increase our source brightness to compensate." Is that a full fix?
Why or why not?
> **Answer:** Not fully — low detection efficiency (and channel loss)
> reduces the *rate* of successful heralded events, but the events you do
> detect are still valid (loss is typically a heralded failure, not a
> corrupting error), so brighter sources help throughput. But it doesn't
> fix noise/dark-count-driven fidelity issues, and past some point
> multi-photon emission from a "brighter" source can itself degrade
> fidelity — so source brightness and detector/channel efficiency both need
> addressing, and detector choice (e.g. SNSPDs for low dark counts) matters
> independently.

**11.** You're networking superconducting qubits, which natively operate at
microwave frequencies (~5 GHz) inside a dilution refrigerator. Why can't
you just run a microwave coaxial cable between two separate fridges to
network them, and what's the alternative?
> **Answer:** Microwave photons don't survive transmission through
> room-temperature cable/fiber runs — thermal noise at room temperature
> completely swamps a single microwave photon's energy, and you'd also need
> the link itself cooled, which doesn't scale to real network distances.
> The alternative is microwave-to-optical transduction: convert the qubit's
> state to an optical photon (which survives room-temperature fiber), send
> it, then convert back — an active area of research because efficient,
> low-added-noise conversion is hard.

**12.** Two integrated photonic chips need to be entangled for a
distributed quantum computing demo. What's one advantage integrated
photonics (waveguides, on-chip sources/modulators) has over free-space/
bulk-optics setups for this, and one thing it still doesn't solve?
> **Answer:** Advantage: integration gives stability, reproducibility, and
> a path to scaling channel count and component density (many waveguides/
> modulators on one chip vs. a bulky free-space table) — critical for
> going beyond single-link lab demos. It doesn't solve loss, decoherence,
> or matter-photon transduction physics — those are the same fundamental
> problems whether the photonics is on-chip or on a table; integration is
> an engineering scalability answer, not a physics one.

**13.** A satellite-based quantum link (like the Micius experiments)
distributes entangled photon pairs to two ground stations thousands of km
apart. Why can this beat a ground-fiber link over the same distance despite
satellites seeming like a detour?
> **Answer:** Free-space loss through the atmosphere plus vacuum scales
> much more favorably with distance than fiber attenuation, which is
> exponential per km — a satellite link mostly traverses near-lossless
> vacuum, only incurring atmospheric loss near each ground station, so
> total loss over thousands of km can be far lower than the equivalent
> length of fiber.
