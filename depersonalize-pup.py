import os
import sys
import struct
import hashlib
import binascii

def readInt32(file):
	return struct.unpack('i', file.read(4))[0]

SCEUF_HEADER_SIZE = 0x80
SCEUF_FILEREC_SIZE = 0x20

if len(sys.argv) <= 1:
	print("Usage: depersonalize-pup.py <pupfile> [scewm.bin]")
else:
	fd = open(sys.argv[1], "rb")
	fd.seek(0)
	magic = fd.read(5)
	if magic == b"SCEUF":
		print("Reading PUP....")
		
		fd.seek(0x18,0)
		total_files = readInt32(fd)
		print("Total files: "+str(total_files))
		
		for i in range(total_files):
			fd.seek(SCEUF_HEADER_SIZE + i * SCEUF_FILEREC_SIZE)
			file_record = fd.read(SCEUF_FILEREC_SIZE)
			file_type, offset, length, flags = struct.unpack("<QQQQ", file_record)
			print("File #"+str(i)+" located at "+hex(offset)+" and is "+str(length)+" bytes, of type "+str(file_type)+" FLAGS="+str(flags))
			fd.seek(offset)
			header = fd.read(5)
			if header == b"SCEWM":
				print("Found SCEWM! Replacing")

				fd.seek(offset)
				scewm = fd.read(length)
				open(sys.argv[1]+"-scewm.bin","wb").write(scewm)
				
				ofd = open(sys.argv[1]+"-depersonalized.pup","wb")
				fd.seek(0,0)
				pup_bytes = bytearray(fd.read())

				payload = b"I like to see cute girls die <3 sony "*length				
				if len(sys.argv) >= 3:
					payload = open(sys.argv[2],"rb").read()
				
				for b in range(length):
					pup_bytes[offset + b] = payload[b]
					
				ofd.write(pup_bytes)
				ofd.close()
				
				
				print("Replaced SCEWM.")
				
				print("Depersonalized pup saved to: "+sys.argv[1]+"-depersonalized.pup")
				fd.close()
				break;
