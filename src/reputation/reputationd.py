# ================================================== #
#                    REPUTATIOND                     #
# ================================================== #
# Author: Brady Hammond                              #
# Created: 01/21/2017                                #
# Last Edited: N/A                                   #
# Last Edited By: N/A                                #
# ================================================== #
#                      IMPORTS                       #
# ================================================== #

import ioflo.app.run

# ================================================== #
#                        MAIN                        #
# ================================================== #

def main():
    from reputation import __version__
    args = ioflo.app.run.parseArgs(version=__version__)

    ioflo.app.run.run(name=args.name,
                      period=float(args.period),
                      real=args.realtime,
                      retro=args.retrograde,
                      filepath=args.filename,
                      behaviors=args.behaviors,
                      mode=args.parsemode,
                      username=args.username,
                      password=args.password,
                      verbose=args.verbose,
                      consolepath=args.console,
                      statistics=args.statistics)

if __name__ == "__main__":
    main()

# ================================================== #
#                        EOF                         #
# ================================================== #
