# example:
#cd c:\python27
# python sorting_pk2.py bars remix-master\examples\music\Cannonball.mp3 
#

"""
based on:
sorting_timbre.py
Sorts AudioQuanta (bars, beats, tatums, segments) by timbral bin (0-11).
By Thor Kell, 2012-11-14

sorting_pk2.py extends this to make it useful for providing input files for
SliceX (FL Studio) that are grouped & named by key and timbre
"""

import echonest.remix.audio as audio
usage = """
python sorting_pk2.py <bars|beats|tatums|segments><input_filename> [reverse]

"""
def main(units, input_filename):
    audiofile = audio.LocalAudioFile(input_filename)
    chunks = audiofile.analysis.__getattribute__(units)
    timbre_range = range(11)
    tonic = audiofile.analysis.key['value']

    
    # For any chunk, return the timbre value of the given bin
    def sorting_function(chunk):
        timbre = chunk.mean_timbre()
        return timbre[timbre_bin]

    #loop through all 11 bins of timbre and output them
    for timbre_bin in timbre_range:
        print(timbre_bin)
        sorted_chunks = sorted(chunks, key=sorting_function, reverse=reverse)

        #would be nice to output string keys rather than bins
        # just zip range 0-11 to    (c, c-sharp, d, e-flat, e, f, f-sharp, g, a-flat, a, b-flat, b)
        
        out = audio.getpieces(audiofile, sorted_chunks)
        out.encode('chopped_%s_%s_%s' % (units,timbre_bin,tonic))

if __name__ == '__main__':
    import sys
    try:
        unit = sys.argv[1]
        input_filename = sys.argv[2]
        
        if len(sys.argv) == 4 and sys.argv[3] == 'reverse':
            reverse = True
        else:
            reverse = False

    except:
        print usage
        sys.exit(-1)
    main(unit, input_filename)
