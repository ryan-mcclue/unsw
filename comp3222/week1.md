<!-- SPDX-License-Identifier: zlib-acknowledgement -->

Quartus tool to target Altera FPGAs. 
This is the physical design, i.e. after VHDL stage

CAD used to simulate circuits? (CAD used to draw schematics?)
For course CAD tools, can be called EDA (electronic design automation)

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
x'₁ + x₁y₁ = (x'₁ + x₁)(x₁ + y₁)
x(x + xy) + y(x + xy) = (x + y)(x + xy)
- uniting (used a lot): X · Y + X · !Y = X 
- de Morgan's: !(X + Y + ...) = !X · !Y ...
can group say X · Y into XY term to be used with de Morgan's

prove deductively (algebra), exhaustively (truth table), set theory (Venn diagram)

first step in synthesising logic circuit is to · for each row with f = 1  
(formally, this process is writing a sum of minterms; or canonical sum-of-products)
(products = ANDed; sum = ORed)
also have maxterms; or canonical product-of-sums

cost metric will be (number of inputs + number of gates)

restricting to just synthesis subset of VHDL
entity (port contains signals; specify mode and type) ➞ 
architecture (concurrent signal assignment; use parenthesis to overcome VHDL precedence)

uniting theorem systematically followed by synthesisers into Karnaugh Maps
rows/columns labelled using Gray encoding for 3 or more tables (differ by 1 bit)
combine where truth tables give 1's in adjacent column/rows (differ by 1 bit). this yields torus behaviour
essentially obtain essential and non-essential prime implicants to get a cover
the process of selecting non-essential prime implicants goverened by trail-and-error hueristic? (and comparing with a POS method)

real-world practilities are functions having values that we don't care about.
similarly, may combine separate functions that share similarities to reduce overall cost

furthermore, having less multilevels (i.e. less levels of gates) can be clocked faster 

PLAs ➞ FPGA (grid of logic blocks connected with tracks) modern incarnation of programmable
FPGA blocks are lookup tables (LUTs). They are just very small memory, e.g. 2-input table is 4 cell memory with 2 layers of muxes (3-input, 3 layers etc.)
The signals we feed the LUT are to select the cells in the LUT we want the internal multiplexer to activate
So, we make the cells in the LUT the values in our truth table
Some complexity of CAD tools arises from various ways we could arrange LUTs

A fan-in (number of inputs) constraint is where have to layer LUTs to implement a function with too many inputs
we can factor out function to help with this

multilevel realisation might lower cost with more gates but yield a higher propagation delay

don't include input inverters in min-cost calculation

a multiplexer could just a be an AND gate

VLSI (very large scale integration) process of combining millions of transistors onto IC
prefer NAND and NOR as they require less transistors


.vwf (input nodes, functional + timing)
assignment editor locations to create bitstream to program board


* limitations in FPGA applications like in quantum computing? (FPGAs are cheaper and faster than MCUs)
* mentioned students getting internships; only in fintec? want more for embedded software
interesting you know the places where your students went; did you keep in touch or help them?
(very open in getting in touch with him on Teams)
* where are decimal logic circuits used? (binary digital logic is prevalent)
* is going through min-terms just an academic process?
i.e. can a computer program optimises this?
(I think this is what syntehsising VHDL does?)
  > Yes, synthesis tools will optimise canonical SOP/POS into min-cost 
* how is CAD process different for an IC over an FPGA? (differences when doing physical design?)
you mention far more costlier and riskier to use an IC solution. so why they more prevelant?
* IEEE standard languages VHDL and Verilog. 
ISO/IEC for C language
