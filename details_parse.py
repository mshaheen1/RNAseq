from File_iterator import detailMaker
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("Input_path", help = "path to directory of input files")
parser.add_argument("Genome_path", help = "path to genome directory")
args = parser.parse_args()

detailMaker(args.Input_path)

def parser():
    o = open('details.txt','r').readlines()
    p = open('below_threshhold.txt','w')
    f = open('final_cut.txt', 'w')
    z = o[0]
    p.write(z)
    o = o[1:]
    
    for i in range(len(o)/2):
        temp1 = o[i*2].split('\t')
        temp1x = o[i*2]
        temp2 = o[i*2+1].split('\t')
        temp2x = o[i*2+1]
        
        f.write(temp1[0] + '\n' + temp2[0] + '\n')    
            
        if temp1.count("FAIL") != 0 or temp2.count("FAIL") != 0:
            p.write(temp1x + "\n" + temp2x + "\n")
    f.close()

def runSTAR(fastqList):
    fastqList = map(str.strip, fastqList)
    for i in range((len(fastqList)/2)):
        os.system("STAR --runThreadN 6 --genomeDir " + args.Genome_path + " --readFilesIn "
        + fastqList[i*2] + "_cutadapt.fastq.gz " + fastqList[i*2+1] + "_cutadapt.fastq.gz --readFilesCommand"
        + " zcat --outSAMtype BAM Unsorted")
        os.system("rm Log.progress.out")
        os.system("rm Log.out")
        os.system("rm SJ.out.tab")
        os.system("mv Aligned.out.bam " + fastqList[i*2][:-2] + ".bam")
        print ("Samtools is sorting " + fastqList[i*2][:-2] + " ...")
        os.system("samtools sort " + fastqList[i*2][:-2] + ".bam -o " + fastqList[i*2][:-2] + ".sorted.bam")
        os.system("rm " + fastqList[i*2][:-2] + ".bam") 

    os.system("rm Log.final.out")

def main():
    parser()
    f = open("final_cut.txt",'r')
    f = f.readlines()
    runSTAR(f)
    os.system("rm final_cut.txt")

main()
