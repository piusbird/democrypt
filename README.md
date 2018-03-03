# stupidcrypt
A Stupid Encryption Utility to test libsodium and pynacl
Please don't use this in production there are at least three flaws I can think of off 
hand.

First Python has no easy or reliable way to securely erase memory so all keys plain-text, may be 
subject to snooping by rouge processes or root

Secondly I did not use a proper Key derivation function, the password which encrypts the 
session key is stored as unsalted personalized blake2b hash. I opted for speed and pedagogical 
simplicity over paranoia 

Thirdly there is no plausible deniablity provided the first 11 bytes of the header say 
"STUPID-KEY\n". So if the fuzz or the mafia ever catch you get ready for a very bad time.

All that being said however apart from the memory erasure issue. This should be as secure as 
the underlying libsodium primitives, and there are quite a few notable encryption systems 
don't provide plausible deniablity *cough* LUKS *cough*. And even with a KDF a hash collision 
or rainbow table would mean you're still  screwed, just more slowly, and if that is your 
preference who am I to judge.

Still and all I'm very new at this crypto stuff so there are probably more flaws that I haven't 
found yet. Therefore I'm not responsible for any encounters with angry hoodie clad skeletons, 
which may occur as a result of using this software  

