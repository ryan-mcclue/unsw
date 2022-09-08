<!-- SPDX-License-Identifier: zlib-acknowledgement -->
CAD used to simulate circuits? (CAD used to draw schematics?)

FPGAs get higher throughput due to parallel circuits with less power than CPU

designing digital logic systems (fundamental abstraction underlying all digital devices), 
i.e. select digital logic components and the interconnections between them
designing in hardware gives lowest cost, highest peformance 

VHDL (VHSIC hardware description language) (very high speed integration circuit)
they are descriptions of the hardware you want to implement, not programs
compile into something that is uploaded to an FPGA?

precedence: ! ➞ · ➞ +

series: light(x₁,x₂) = x₁ · x₂ (and)
parallel: light(x₁,x₂) = x₁ + x₂ (or)
inversion: light(x₁) = !x (not)
logic operations implemented with transistors as circuit elements known as logic gates

complexity of logic circuit/network directly related to number of gates and inputs

analysing circuit, can draw truth table or digital waveform 

to simplify circuit, utilise boolean algebra theorems:
(duality is a meta-theorem)
- identity: (X + 0 = X) ⟷ (X · 1 = 1)
- null: (X + 1 = 1) ⟷ (X · 0 = 0)
- idempotency (can just add duplicate): (X + X = X) ⟷ (X · X = X)
- involution: !(!X) = X
- complementarity: (X + !X = 1) ⟷ (X · !X = 0)
- commutative (doesn't matter what order same operation): (X + Y) = (Y + X)
- associative (doesn't matter what sequence same operation) (X · Y) · Y = X · (Y · Y)
- distributive (multiplying out, i.e. pulling out common factor)
- uniting (used a lot?): X · Y + X · !Y = X 
- de Morgan's: !(X + Y + ...) = !X · !Y ...
can group say X · Y into XY term to be used with de Morgan's

prove deductively (algebra), exhaustively (truth table), set theory (Venn diagram)

first step in synthesising logic circuit is to · for each row with f = 1  
(formally, this process is writing a sum of minterms; or canonical sum-of-products)
(products = ANDed; sum = ORed)

cost metric will be (number of inputs + number of gates)

* limitations in FPGA applications like in quantum computing?
* mentioned students getting internships; only in fintec? want more for embedded software
interesting you know the places where your students went; did you keep in touch or help them?
(very open in getting in touch with him on Teams)
* where are decimal logic circuits used? (binary digital logic is prevalent)
* is going through min-terms just an academic process?

* TUTORIAL STYLE PROBLEMS?


