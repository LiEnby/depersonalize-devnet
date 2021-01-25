import os
import sys
import pikepdf

def getHiddenSerial(serialNumber, seperator):
	hiddenSerial = ""
	for i in range(0,len(serialNumber)):
		hiddenSerial += serialNumber[i] + seperator
	return hiddenSerial



if len(sys.argv) <= 1:
	print("Usage: depersonalize-doc.py <doc.pdf>")
else:
	print("Reading PDF....")
	outfile = sys.argv[1]+"-depersonalized.pdf"
	
	pdf = pikepdf.open(sys.argv[1])
	# Delete metadata...
	with pdf.open_metadata(set_pikepdf_as_editor=False, update_docinfo=False) as meta:
		del meta["xmp:ModifyDate"]
		del meta["xmp:MetadataDate"]
		del meta["xmpMM:InstanceID"]
	del pdf.docinfo["/ModDate"]
	del pdf.trailer.ID

	
	streams = []
	for pageNo in range(0, len(pdf.pages)):
		streams.clear()
		serialCode = ""
		for contentNo in range(0,len(pdf.pages[pageNo].Contents)):
			cstream = pikepdf.parse_content_stream(pdf.pages[pageNo].Contents[contentNo])
			for elm in cstream:
				if len(elm[0]) > 0:
					strValue = ""
					try:
						strValue = str(elm[0][0])
					except:
						pass
					if strValue.startswith("Document serial number: "):
						serialCode = strValue[24:]
		
		his1 = getHiddenSerial(serialCode, "=")
		his2 = getHiddenSerial(serialCode, ":")
		
		for contentNo in range(0,len(pdf.pages[pageNo].Contents)):
			cstream = pikepdf.parse_content_stream(pdf.pages[pageNo].Contents[contentNo])
			for elm in cstream:
				if len(elm[0]) > 0:
					strValue = ""
					try:
						strValue = str(elm[0][0])
					except:
						pass
					if not strValue.find(serialCode) == -1 or not strValue.find(his1) == -1 or not strValue.find(his2) == -1:
						new_content_stream = pikepdf.unparse_content_stream([])
						nstream = pdf.make_stream(new_content_stream)
						pdf.pages[pageNo].Contents[contentNo] = nstream
						break
		print("Creating page: "+str(pageNo))
		
	pdf.save(outfile, encryption=False)
	pdf.close()
	
	print("Removed serial number,")