```
$ python ./cslv.py
_________            .___       _________.__
\_   ___ \  ____   __| _/____  /   _____/|__| ____   ____   ___________
/    \  \/ /  _ \ / __ |/ __ \ \_____  \ |  |/ ___\ /    \_/ __ \_  __ \
\     \___(  <_> ) /_/ \  ___/ /        \|  / /_/  >   |  \  ___/|  | \/
 \______  /\____/\____ |\___  >_______  /|__\___  /|___|  /\___  >__|
        \/            \/    \/        \/   /_____/      \/     \/
+----------------------------------------------------------------------+
| Copyright (c) SAMSUNG Electronics Co., Ltd. All rights reserved.     |
| This software is a confidential stuff and proprietary of             |
| SAMSUNG Electronics Co., Ltd.                                        |
| So you shall not disclose this software other company or persons     |
| without permission of SAMSUNG and shall use this software only       |
| in accordance with the license agreement of SAMSUNG.                 |
+----------------------------------------------------------------------+
CodeSigner Lite Version 5 for SAMSUNG Processors

Usage: cslv_64 <OPTIONS>

Options:
  -h, -help                   show this help message and exit

  Options:
    cslv_64

    -key_id=<key_id>          Lower case alphabet or number string only
    -infile=<filename>        Boot Loader(IMGMAKE Case), Signed Boot Loader(VERIFY Case)
    -outfile=<filename>       Signed Boot Loader(IMGMAKE Case), Boot Loader(VERIFY Case)
    -sign_type=<0-8>          0~2: RSASSA-PSS 2048/3072/4096 3~5: ECDSA NIST-P Curve 256/384/521
                              6~8: ECDSA BrainPool Curve 256/384/512
    -rb_count=<0-9000>        Rollback Count (default: 0)
    -key_type=<0-9000>        Key type (default: 0)
    -key_index=<0-9000>       Key Index (default: 0)
    -dynamic_length=<yes|no>  el3 image (yes), the others (no)
    -export_pub=<filename>    Export publickey for testing (ex: testkey)

* sign_type option:
  0~2: RSASSA-PSS 2048/3072/4096
  3~5: ECDSA NIST 256/384/521
  6~8: ECDSA BRAINPOOL 256/384/512

Examples:   
  cslv_64 -infile bl2.img -outfile sbl2.img -sign_type 0 -key_type 0 -key_index 11 -rb_count 0 -dynamic_length no (-path ./)

$ python ./cslv.py -infile arch/arm64/boot/Image_pad.bin -outfile arch/arm64/boot/Image -sign_type 3 -key_type 1 -rb_count 0 -dynamic_length no
_________            .___       _________.__
\_   ___ \  ____   __| _/____  /   _____/|__| ____   ____   ___________
/    \  \/ /  _ \ / __ |/ __ \ \_____  \ |  |/ ___\ /    \_/ __ \_  __ \
\     \___(  <_> ) /_/ \  ___/ /        \|  / /_/  >   |  \  ___/|  | \/
 \______  /\____/\____ |\___  >_______  /|__\___  /|___|  /\___  >__|
        \/            \/    \/        \/   /_____/      \/     \/
+----------------------------------------------------------------------+
| Copyright (c) SAMSUNG Electronics Co., Ltd. All rights reserved.     |
| This software is a confidential stuff and proprietary of             |
| SAMSUNG Electronics Co., Ltd.                                        |
| So you shall not disclose this software other company or persons     |
| without permission of SAMSUNG and shall use this software only       |
| in accordance with the license agreement of SAMSUNG.                 |
+----------------------------------------------------------------------+
CodeSigner Lite Version 5 for SAMSUNG Processors

[*] sign_type: 3
[*] key_id: 
[*] infile: arch/arm64/boot/Image_pad.bin
[*] outfile: arch/arm64/boot/Image
[*] rb_count: 0
[*] key_index: 0
[*] key_type: 1
[*] dynamic_length: no
[*] sign_type: 3 (algorithm: ECDSA, Curve: NIST 256 bit, 68 Byte)
[*] sign_type: 3 (algorithm: ECDSA, Curve: NIST 256 bit, 68 Byte)
[*] Verification result is True
[*] All process was well done.
```
