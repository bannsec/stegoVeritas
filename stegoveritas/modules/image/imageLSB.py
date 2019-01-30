from config import TEMPFILE
import subprocess
import os
import shutil
import time
import magic

def testOutput(b,args):
        """
        Input:
                b = byte array output, generally from the dump functions
                ex: b = b'\x01\x02\x03'
        Action:
                Test if output is worth keeping.
                Initially, this is using the Unix file command on the output and checking for non "Data" returns
        Return:
                Nothing. Move output into keep directory if it's worth-while    
        """

        # TODO: Test new logic...
        # TODO: Iterate through binary offset to find buried data

        m = magic.from_buffer(b,mime=True)

        # Generic Output
        if m != 'application/octet-stream':
            m = magic.from_buffer(b,mime=False)
            print("Found something worth keeping!\n{0}".format(m))
            # Save it to disk
            with open(os.path.join(args.outDir,str(time.time())), "wb") as f:
                f.write(b)

        """
        # Write out the buffer  
        temp = open(TEMPFILE,"wb")
        temp.write(b)
        temp.close()

        # Run the file command
        out = subprocess.check_output(["file",TEMPFILE])

        # We like anything that's not just data
        if b': data\n' not in out:
                print("Found something worth keeping!\n{0}".format(out))
                shutil.move(TEMPFILE,os.path.join(args.outDir,str(time.time())))

        try:
                # Remove our mess
                os.unlink(TEMPFILE)
        except OSError:
                pass
        """


def _dumpLSB(img,index):
        """
        Mostly obsolete since extraction method changed
        Input:
                img == PIL image (type PIL.Image.Image)
                index == integer from LSB to extract (0 == first bit, 1 == second bit, etc)
        Action:
                Extract array of bits represented as integers
        Returns:
                Bit integer array (i.e.: [0,1,1,0,0,1,0,1 ...]
        """
        # Make sure we're working with the right thing
        if type(img) != Image.Image:
                raise Exception("_dumpLSB: image type should be PIL.Image.Image.\nActual image type is {0}".format(type(img)))

        # Check index
        if index >= 8:
                raise Exception("_dumpLSB: index cannot be >= 8.\nActual index is {0}".format(index))

        # Perform bit extraction
        out = [str((byte >> index) & 1) for byte in img.tobytes()]

        return out


def auto(f,args):
        # Try all the same indexes first. More likely stuff up front.
        # i.e.: 0,0,0  1,1,1,  2,2,2
        for i in range(0,8):
                print("Trying {0}.{0}.{0}".format(i))
                o = _dumpLSBRGBA(f=f,rIndex=[i],gIndex=[i],bIndex=[i])
                testOutput(o,args)

        # Try Red
        i = []
        for x in range(8):
                i.append(x)
                print("Trying Red {0}".format(i))
                o = _dumpLSBRGBA(f=f,rIndex=i)
                testOutput(o,args)

        # Try Green
        i = []
        for x in range(8):
                i.append(x)
                print("Trying Green {0}".format(i))
                o = _dumpLSBRGBA(f=f,gIndex=i)
                testOutput(o,args)

        # Try Blue
        i = []
        for x in range(8):
                i.append(x)
                print("Trying Blue {0}".format(i))
                o = _dumpLSBRGBA(f=f,bIndex=i)
                testOutput(o,args)

        # Try Alpha
        if "A" in f.mode:
                i = []
                for x in range(8):
                        i.append(x)
                        print("Trying Alpha {0}".format(i))
                        o = _dumpLSBRGBA(f=f,aIndex=i)
                        testOutput(o,args)

        # Try across the board
        # i.e.: 0,0,0  01,01,01 etc
        i = []
        for x in range(8):
                i.append(x)
                print("Trying {0}x{0}x{0}".format(i))
                o = _dumpLSBRGBA(f=f,rIndex=i,gIndex=i,bIndex=i)
                testOutput(o,args)

        return
        for r in range(0,8):
                for g in range(0,8):
                        for b in range(0,8):
                                print("Trying {0}.{1}.{2}".format(r,g,b))
                                o = _dumpLSBRGBA(f=f,rIndex=[r],gIndex=[g],bIndex=[b])
                                testOutput(o,args)

