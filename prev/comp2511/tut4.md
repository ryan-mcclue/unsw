<!-- SPDX-License-Identifier: zlib-acknowledgement -->

law of demeter -> least knowledge -> loose coupling
(the process of refactoring this would be method forwarding)

LSK
could make super class more generic, e.g. Car to Vehicle
could use composition (strategy pattern)

Design-By-Contract not really applicable for end-users; more so for developers
/**
@preconditions ... (cannot be weakened)
@postconditions ... (cannot be strengthened)
*/
