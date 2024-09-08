<!-- SPDX-License-Identifier: zlib-acknowledgement -->

OO doesn't like switch statements as 'harder maintanence for adding new behaviour'
so like:

switch (type/strategy) {

}

becomes:

interface ChargingStrategy {
  functionFunc()
}

class Strategy1 implements ChargingStrategy {

}
