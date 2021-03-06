import argparse

from packman import molecule
from packman.anm import ANM
'''
##################################################################################################
#                                          Interface                                             #
##################################################################################################
'''

def IO():
    """User interface for the user to provide the parameters
    Todo:
        * None
    
    Returns:
        Namespace: Various arguments in various formats
    """
    parser=argparse.ArgumentParser(description='Rigid Domain ANM (RD-ANM). (https://github.com/Pranavkhade/PACKMAN)')
    parser.add_argument('-pdbid','--pdbid', metavar='PDB_ID', type=str, help='If provided, the PBD with this ID will be downloaded and saved to FILENAME.')
    parser.add_argument('filename', metavar='FILENAME', help='Path and filename of the PDB file.')

    parser.add_argument("--chain", help='Enter The Chain ID')
    parser.add_argument("--dr", default=15, help='Distance cutoff for the ANM.')
    parser.add_argument("--power", default=0, help='Power of the distance in non-parametric ANM.')
    args=parser.parse_args()
    return args


'''
##################################################################################################
#                                              Main                                              #
##################################################################################################
'''


def main():
    """
    """
    ARGS = IO()

    #Load the Hinge Information
    filename = ARGS.filename
    chain    = ARGS.chain
    dr       = float(ARGS.dr)
    power    = float(ARGS.power)


    #File loading 
    mol=molecule.load_structure(filename)

    if(chain is not None):
        calpha=[i for i in mol[0][chain].get_calpha()]
    else:
        calpha=[i for i in mol[0].get_calpha()]

    
    Model=ANM([i.get_location() for i in calpha],atoms=calpha,dr=dr,power=power)
    Model.calculate_hessian()
    Model.calculate_decomposition()
    
    for i in range(6,17,1):
        Model.calculate_movie(i,scale=2,n=20)



    return True


'''
##################################################################################################
#                                               IO                                               #
##################################################################################################
'''

if(__name__=='__main__'):
    main()
