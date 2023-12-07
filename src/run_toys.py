#!/bin/python3
import subprocess
import shutil, os
import argparse

def main():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("-o", "--output", type=str, default="toys_output", help="Output folder")
    parser.add_argument("-x", "--xfitter", type=str, 
                        default="/afs/desy.de/user/a/amoroso/cmsarea/xfitter-patchtoys/", help="path to xfitter installation")
    parser.add_argument("-n", "--ntoys", type=int, default=10, help="Number of toys to be generated")
    parser.add_argument("-s", "--steering", type=str, default="steering_backup.txt", help="xfitter steering file")
    parser.add_argument("-r", "--rseed", type=int, default=0, help="randopm number seed")

    args = parser.parse_args()

    xfitterpath = args.xfitter
    outfolder = args.output
    ntoys = args.ntoys
    rseed = args.rseed

    for itoy in range(ntoys):

        # Open the steering template
        with open("steering_backup.txt", "r") as f:
            contents = f.read()
        # Set the random seed
        new_contents = contents.replace("ISeedMC = 123456", "ISeedMC = "+str(rseed+itoy))
        # Write the modified steering
        with open("steering.txt", "w") as f:
            f.write(new_contents)

        # Run xfitter
        if not os.path.exists(os.path.join(xfitterpath, "bin/xfitter")):
            raise FileNotFoundError("xfitter executable not found")
        try:
            subprocess.run(os.path.join(xfitterpath, "bin/xfitter"))
        except subprocess.CalledProcessError:
            raise RuntimeError("xfitter execution failed")
        else:
            print("xfitter executed successfully")


        # Check if output directory exists, create it if it doesn't
        if not os.path.exists(outfolder):
            os.makedirs(outfolder)

    
        # Move and rename fittedresults.txt
        width = len(str(ntoys))
        zero_padded_itoy = str(itoy).zfill(width)
        new_filename = f'fittedresults_{zero_padded_itoy}.txt'
        shutil.move('output/fittedresults.txt', outfolder + '/' + new_filename)

if __name__ == "__main__":
    main()
