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


# Change this to a primitive to dump any given index of a given color
# Then, handle the weaving of those together in a different function
def _dumpLSBRGBA(f,rIndex = [],gIndex = [],bIndex = [],aIndex = []):
        """
        Input: 
                rIndex, gIndex, bIndex, aIndex as array of integer indexes (up to 8) to dump
                ex: [0],None,None would dump only the least significant bit of the Red field
        Action:
                Creates a byte array containing the output of the LSB dump (RGBA order) requested
                If needed, it will use the least significant bit first, then bit plane order of red->green->blue->alpha
        Returns:
                Byte array of the result of the action
                ex: b'\x01\x02\x03\x04' etc
        """

        ##################
        # Combine Output #
        ##################
        # We'll be keeping the binary string here
        binStr = ''

        # Figure out valid index ranges
        indexes = list(set(rIndex + gIndex + bIndex + aIndex))
        indexes.sort()

        # Figure out what we have to work with
        bands = f.getbands()

        # Get the image bytes
        fBytes = f.tobytes()

        # TODO: The following assumes an ordering of RGBA. If this is ever not the case, things will get mixed up
        # Loop through all the bytes of the image
        for byte in range(0,f.size[0] * f.size[1] * len(bands),len(bands)):
                # Loop through all the possible desired indexes
                for index in indexes:
                        # If this is a value we're extracting
                        if index in rIndex:
                                binStr += str(fBytes[byte + 0] >> index & 1)
                        if index in gIndex:
                                binStr += str(fBytes[byte + 1] >> index & 1)
                        if index in bIndex:
                                binStr += str(fBytes[byte + 2] >> index & 1)
                        if index in aIndex:
                                binStr += str(fBytes[byte + 3] >> index & 1)

        # Parse those into bytes
        bArray = []
        for i in range(0,len(binStr),8):
                bArray.append(int(binStr[i:i+8],2))

        # Change bytes into a bit array for writing
        bits = ''.join([chr(b) for b in bArray]).encode('iso-8859-1')

        return bits


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

