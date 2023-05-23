# depersonalize-devnet
tools to remove watermark personalization from PSVita Development Files
this allows them to be shared without sony knowing where they came from.

btw- they might change the personalization format after version 3.73. . . 

depersonalize_doc.py-

before:          
![image](https://user-images.githubusercontent.com/39113159/116801075-9cbd7380-ab5a-11eb-9444-fea9b64e7136.png)
after:     
![image](https://user-images.githubusercontent.com/39113159/116801094-b6f75180-ab5a-11eb-8c70-b63f577beacd.png)


            
(note this breaks the PUP Signature and you have to use a [plugin](https://github.com/KuromeSan/depersonalize-devnet/tree/master/pup_verify_bypass) to bypass signature verification at install time for this to acturally install)
