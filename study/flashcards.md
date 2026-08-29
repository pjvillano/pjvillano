# Flashcards: Quantum Computing & Photonic Interconnects

Grouped by curriculum module (see `study/curriculum.md`). Also loaded into
the interactive flipper in `study/companion.html`. Format: `Q:` / `A:` pairs;
keep answers short (a few sentences or a short list).

---

## Module 1 — Quantum Computing Fundamentals

**Q1.** What does superposition let a qubit do that a classical bit can't?
**A1.** Exist in a weighted combination of |0⟩ and |1⟩ simultaneously
(α|0⟩ + β|1⟩), rather than being fixed at exactly one value — measurement
then collapses it to 0 or 1 with probability |α|² / |β|².

**Q2.** Why does an N-qubit system require 2^N complex amplitudes to
describe, and why does that matter?
**A2.** Each qubit's basis states combine multiplicatively (tensor product),
so N qubits span a 2^N-dimensional space. It's why classical computers can't
efficiently simulate general quantum states past ~50 qubits, and it's the
source of quantum computing's potential speedup.

**Q3.** What is the no-cloning theorem and why does it matter for
networking?
**A3.** It's impossible to create an identical copy of an arbitrary unknown
quantum state. It means you can't "just copy" quantum information across a
network the way you copy classical packets — entanglement/teleportation
schemes exist precisely because of this constraint.

**Q4.** What's the practical difference between T1 and T2 coherence times?
**A4.** T1 is energy relaxation time (how long before the qubit decays to
|0⟩); T2 is dephasing time (how long relative phase information survives).
T2 ≤ 2×T1, and T2 is usually the tighter constraint on algorithm runtime.

**Q5.** What's a "logical qubit" vs. a "physical qubit"?
**A5.** A physical qubit is one real hardware qubit; a logical qubit is an
error-corrected qubit built from many physical qubits (e.g. dozens to
thousands, depending on the code and target error rate) that behaves as one
much-lower-error qubit.

**Q6.** Why does two-qubit gate fidelity dominate system error budgets more
than single-qubit gate fidelity?
**A6.** Two-qubit gates are harder to implement precisely (they require
controlled interaction between qubits) and typically have error rates
5–10× worse than single-qubit gates, and circuits use many more of them as
width/depth grow — so they set the practical ceiling on circuit size.

**Q7.** What defines the "NISQ era" and what's its main workaround for
lack of error correction?
**A7.** Noisy Intermediate-Scale Quantum devices: tens to a few thousand
qubits, no full error correction, limited circuit depth before noise
dominates. The main workaround is variational/hybrid algorithms (e.g. VQE,
QAOA) that use short circuits plus classical optimization loops.

**Q8.** Name the four major hardware modalities and one key tradeoff each.
**A8.** Superconducting (fast gates, but short coherence, needs dilution
fridge); trapped ion (very high fidelity, all-to-all connectivity, but
slower gates); photonic (room temp possible, natural for networking, but
hard to do deterministic two-qubit gates and to store photons); neutral
atom (scalable qubit counts via optical tweezers, flexible connectivity,
still maturing on gate fidelity).

---

## Module 2 — Distributed Quantum Computing

**Q9.** Why pursue distributed/modular quantum computing instead of one
large monolithic processor?
**A9.** Chip-scale wiring, crosstalk, cooling, and control-electronics
density all get harder as qubit count grows on a single chip; linking
smaller, well-characterized modules via quantum interconnects is a more
scalable path than indefinitely scaling one module.

**Q10.** What is the fundamental "networking primitive" in quantum
networks, and how is it different from classical networking?
**A10.** Distributed entanglement between nodes. Classical networks move
copies of bits; quantum networks generate and distribute entangled pairs,
then use them (with classical communication) to move or operate on quantum
information — you can't just "send the qubit" losslessly at scale.

**Q11.** Walk through quantum teleportation in one sentence, and name what
it requires.
**A11.** Using a pre-shared entangled pair plus a Bell-state measurement on
the sender's side and two classical bits sent to the receiver, an unknown
qubit's state is reconstructed at the receiver (destroying the original) —
it requires pre-existing entanglement and a classical channel, and does not
transmit information faster than light.

**Q12.** What does entanglement swapping accomplish?
**A12.** It extends entanglement across a hop that was never directly
entangled: if A-B and B-C are entangled, a Bell measurement at B "swaps" the
entanglement so A-C become entangled, without A and C ever directly
interacting.

**Q13.** What problem does entanglement purification solve, and at what
cost?
**A13.** It takes multiple copies of noisy/low-fidelity entangled pairs and
distills fewer, higher-fidelity pairs (e.g. BBPSSW, DEJMPS protocols) — the
cost is consuming more raw entangled pairs (and time) per usable high-
fidelity pair.

**Q14.** Why can't you just send entangled photons directly over
arbitrarily long fiber without repeaters?
**A14.** Fiber loss is exponential in distance (~0.2 dB/km at telecom
wavelength), so direct transmission success probability collapses over
hundreds of km — repeaters break the link into shorter segments where
entanglement is generated locally then swapped/purified, avoiding
end-to-end exponential loss.

**Q15.** What is the core idea of the DLCZ quantum repeater protocol?
**A15.** Use atomic ensembles (or similar quantum memories) at repeater
nodes to heraldedly store entanglement generated with photons over each
segment, then perform entanglement swapping between adjacent segments once
both succeed — trading a memory requirement for beating direct-transmission
loss scaling.

**Q16.** How does the proposed "quantum internet stack" parallel the
classical OSI/TCP-IP stack, at a high level?
**A16.** It's similarly layered (physical link generation → entanglement
distribution/link layer → network-wide entanglement routing → transport →
application), but the physical layer's job is generating and swapping
entanglement rather than moving classical bits, and "packets" don't survive
copying the way classical ones do.

---

## Module 3 — Photonic Interconnects

**Q17.** Why are photons the natural choice for carrying quantum
information between nodes?
**A17.** They interact weakly with their environment (long coherence while
in flight) and travel near the speed of light, making them ideal "flying
qubits" for transmission — the tradeoff is they're hard to store and easy
to lose (absorption/scattering).

**Q18.** Name three ways to encode a qubit in a photon and one tradeoff for
each.
**A18.** Polarization (simple, but polarization drifts in standard fiber
and needs active compensation); time-bin (robust to fiber polarization
drift, but requires stable interferometric timing); path/dual-rail (natural
for integrated photonics, but harder over long fiber distances than
time-bin).

**Q19.** What is "matter–photon transduction" and why is it needed?
**A19.** Converting information between a stationary matter qubit (ion,
atom, superconducting circuit) and a flying photonic qubit, so a
memory/processing qubit can be entangled with a photon for transmission —
needed because matter qubits can't travel through fiber and photons can't
be stored/processed the way matter qubits can.

**Q20.** How do trapped-ion systems typically generate ion-photon
entanglement?
**A20.** An ion is excited such that its spontaneous emission photon's
properties (e.g. polarization or frequency) are entangled with the ion's
internal state — collecting and interfering these photons from two distant
ions (with a successful joint measurement) heralds ion-ion entanglement.

**Q21.** What is microwave-to-optical transduction and which modality
needs it most?
**A21.** Converting a superconducting qubit's native microwave-frequency
signal into an optical photon (and back), since microwave photons don't
survive room-temperature fiber transport — needed for networking
superconducting quantum processors, and still an active research problem
because efficient, low-noise conversion is hard.

**Q22.** Why is loss usually the dominant error mechanism in photonic
links, more than decoherence?
**A22.** A lost photon simply fails to arrive (a heralded, detectable
failure you retry), but the loss probability compounds exponentially with
distance/interfaces — at practical link lengths, the sheer rate of failed
attempts (not phase/amplitude corruption of surviving photons) is what
limits throughput.

**Q23.** Roughly what is fiber attenuation at telecom wavelength (~1550nm)
and why does that number matter?
**A23.** About 0.2 dB/km — it's the reference number for link-budget and
repeater-spacing calculations; native emission wavelengths of many qubit
modalities are much lossier in fiber, which is why frequency conversion to
telecom bands matters.

**Q24.** What is an SNSPD and why does it matter for photonic
interconnects?
**A24.** A Superconducting Nanowire Single-Photon Detector — an extremely
low-noise, high-efficiency single-photon detector (cryogenic) that's become
the workhorse detector for quantum-photonic experiments because low dark
counts and high detection efficiency are critical when photon rates are
already loss-limited.

**Q25.** Why convert a qubit's native emission wavelength to a telecom band
before sending it over fiber?
**A25.** Many qubit platforms emit at wavelengths (e.g. visible/near-IR)
with much higher fiber loss than the telecom C-band (~1550nm); nonlinear
frequency conversion trades some efficiency/noise for dramatically lower
transmission loss over realistic distances.

**Q26.** What does wavelength-division multiplexing (WDM) buy a quantum
network, similar to classical networks?
**A26.** Parallel entanglement-distribution channels over one fiber, by
assigning different frequency channels to different photon pairs/links —
increasing effective entanglement-generation rate without needing more
fiber.

**Q27.** Give one example of a real-world demonstration relevant to
photonic quantum interconnects.
**A27.** Examples include chip-to-chip photonic entanglement links between
integrated photonic circuits, campus-scale fiber entanglement distribution
testbeds, and satellite-based entanglement distribution (e.g. Micius)
extending photonic links beyond fiber-loss-limited ground distances.
