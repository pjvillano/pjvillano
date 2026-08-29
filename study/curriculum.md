# Curriculum: Quantum Computing & Distributed Quantum Computing (Photonic Interconnects Focus)

A roadmap for studying quantum computing with an emphasis on how quantum
processors are networked together — especially over photonic links. Modules
build on each other; within a module, subtopics are roughly ordered but not
strictly sequential.

Companion material: `study/flashcards.md`, `study/quiz-bank.md`,
`study/companion.html` (interactive version, published as an Artifact).

---

## Module 1 — Quantum Computing Fundamentals

1. **Qubits & state** — superposition, the Bloch sphere, single-qubit vs.
   multi-qubit state space (why N qubits need 2^N amplitudes).
2. **Entanglement & measurement** — Bell states, no-cloning theorem,
   measurement collapse, why entanglement is a resource, not just correlation.
3. **Gates & circuits** — universal gate sets, single- vs. two-qubit gates,
   circuit depth, why two-qubit gate fidelity dominates system error budgets.
4. **Decoherence & noise** — T1/T2 times, gate error vs. idle error, why
   "coherence time" alone doesn't tell you if a system is useful.
5. **Quantum error correction (QEC) basics** — physical vs. logical qubits,
   the surface code at a conceptual level, error thresholds, why QEC is the
   central obstacle to fault tolerance.
6. **NISQ vs. fault-tolerant era** — what NISQ devices can and can't do,
   variational algorithms as a NISQ-era workaround, the resource-estimate gap
   to fault tolerance.
7. **Hardware modalities overview** — superconducting transmons, trapped
   ions, photonic qubits, neutral atoms; rough tradeoffs (gate speed,
   connectivity, coherence, scalability path).

## Module 2 — Distributed Quantum Computing

1. **Why distribute** — chip-scale connectivity and cooling limits, modular
   architectures, the case for networking many smaller processors instead of
   building one giant one.
2. **Entanglement as the networking primitive** — why distributed quantum
   computing/networking is fundamentally about generating and distributing
   entanglement, not shipping qubits.
3. **Quantum teleportation** — protocol mechanics, why it needs a classical
   channel plus pre-shared entanglement, what it does and doesn't let you do
   faster-than-light (it doesn't).
4. **Entanglement swapping & purification** — extending entanglement across
   multiple hops (swapping), improving fidelity of noisy entangled pairs
   (purification protocols like BBPSSW/DEJMPS).
5. **Quantum repeaters** — the DLCZ (Duan-Lukin-Cirac-Zoller) protocol and
   successors, why repeaters are needed to beat direct-transmission loss
   scaling over long fiber distances, memory-based vs. all-photonic repeaters.
6. **Distributed quantum algorithms** — distributed quantum computing vs.
   quantum networking for QKD, basics of distributed circuit cutting /
   modular algorithm execution across linked nodes.
7. **The quantum internet stack** — proposed layered architectures
   (physical, link, network, transport, application), how it parallels and
   diverges from the classical OSI stack, current standardization efforts.

## Module 3 — Photonic Interconnects

1. **Photons as flying qubits** — why photons are the natural "wire" for
   quantum information (weak interaction with environment, near-lightspeed
   transmission) and the flip side (hard to store, easy to lose).
2. **Photonic qubit encodings** — polarization, time-bin, path (dual-rail),
   frequency encoding; tradeoffs for fiber transmission and integration.
3. **Matter–photon transduction** — interfacing static/matter qubits with
   flying photonic qubits: ion-photon entanglement (relevant to trapped-ion
   systems), atom-photon interfaces (cavity QED, Rydberg), microwave-to-
   optical transduction for superconducting qubits.
4. **Loss, decoherence & fidelity budgets** — fiber attenuation (~0.2 dB/km
   at telecom wavelength), why loss (not just decoherence) is the dominant
   photonic-link error mechanism, link budget calculations.
5. **Integrated photonics for interconnects** — waveguides, on-chip
   modulators and switches, superconducting nanowire single-photon
   detectors (SNSPDs), why integration matters for scaling beyond
   free-space/bulk-optics demos.
6. **Frequency conversion & multiplexing** — converting native emission
   wavelengths to telecom bands for low-loss fiber transport, wavelength-
   division multiplexing for parallel entanglement channels.
7. **Real systems & testbeds** — notable photonic-interconnect
   demonstrations (chip-to-chip, campus-scale, satellite-based QKD),
   how different hardware modalities approach the matter-photon interface
   (e.g. trapped-ion photonic interconnects vs. superconducting
   microwave-optical transduction).

---

## Suggested study order

Module 1 → Module 2 (sections 1–4) → Module 3 (sections 1–3) → Module 2
(sections 5–7, quantum repeaters land better once transduction/loss are
understood) → Module 3 (sections 4–7).

## How this file grows

Ask the `quantum-systems-tutor` agent to expand a section, add a new
subtopic, or go deeper on anything here — it will extend this file and add
matching flashcards/quiz questions rather than replacing what exists.
