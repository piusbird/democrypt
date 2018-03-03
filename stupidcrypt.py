#!/usr/bin/env python2
# Stupid file encrypter 
# Encrypts a file wirg a password
# This is for demonstartion purposes only
# It should be reasonably secure but keep in mind
# That python has limitations which make it suboptimal 
# for this sort of thing


import sys
import getopt
import nacl
import getpass
import nacl.hash
import nacl.secret
import nacl.utils
import nacl.encoding
SYS_HEADER = b"STUPID-KEY\n"
persona = b"Stupid Encrypter"



fname = sys.argv[1]
encmode = True

rp = open(fname, 'rb')
fheader = rp.read(11)
if fheader == SYS_HEADER:
	encmode = False

if encmode:
	hash_buf = ''	
	rp.seek(0)
	rbuf = rp.read()
	rp.close()
	firstpass = getpass.getpass()
	secondtry = getpass.getpass("Password (again): ")
	if firstpass == secondtry:
		hash_buf = nacl.hash.blake2b(firstpass, digest_size=32, person=persona, encoder=nacl.encoding.RawEncoder)
	else:
		print "Error: Passwords don't match"
		sys.exit(1)
	seskey = nacl.utils.random(nacl.secret.SecretBox.KEY_SIZE)
	mbox = nacl.secret.SecretBox(seskey)
	enc_content = mbox.encrypt(rbuf)
	pbox = nacl.secret.SecretBox(hash_buf)
	enc_seskey = pbox.encrypt(seskey)
	wfname = fname + '.enc'
	wp = open(wfname, "wb")
	wp.write(SYS_HEADER)
	wp.write(enc_seskey)
	wp.write(enc_content)
	wp.close()
else:
	fpos = rp.tell()
	if fpos != 11:
		rp.seek(0)
		rp.read(11)
	enc_seskey = rp.read(72)
	pwd = getpass.getpass()
	hash_buf = nacl.hash.blake2b(pwd, digest_size=32, person=persona, encoder=nacl.encoding.RawEncoder)	
	pbox = nacl.secret.SecretBox(hash_buf)
	dseskey = pbox.decrypt(enc_seskey)
	mbox = nacl.secret.SecretBox(dseskey)
	ecmbuf = rp.read()
	mbuf = mbox.decrypt(ecmbuf)
	wfname = fname + '.out'
	wp = open(wfname, 'wb')
	wp.write(mbuf)
	wp.close()
	rp.close()
sys.exit(0)
