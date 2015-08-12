## Python script to verify MD5 checksums of RNA seq data files downloaded from Broad
## Broad transfers include a file named 'MANIFEST' that contains all calculated checksums
##
## Usage:	module load centos6/python-2.7.3
##			python md5_verify.py [path] > md5_verify
##
## Note: DO NOT RUN ON LOGIN NODE -- SUBMIT A SLURM JOB AND REDIRECT STDOUT TO A FILE (i.e., > md5_verify)
##
##		sbatch -J md5sums -e md5sums.err -t 1-12:00:00 --mail-type=END --mail-user=rmoccia@fas.harvard.edu -p general -n 64 \
##		--ntasks-per-node=64 --mem=3750 --wrap="python /n/Eggan_Lab3/Users/Moccia/scripts/md5_verify_multi.py [path] > md5_verify 2>md5_verify.log"


from sys import argv
import os.path
import hashlib
import multiprocessing

if len(argv) > 1:
	DIR = argv[1]
else:
	DIR = ''

def md5check(args):
	filename = os.path.join(DIR, args[0])
	checksum = args[1]

	try:
		with open(filename, 'r') as f:
			m = hashlib.md5()
			block = f.read(131072)
			while block != '':
				m.update(block)
				block = f.read(131072)
		if m.hexdigest() != checksum:
			return (args[0], checksum, m.hexdigest())

	except IOError:
		return args[0]


if __name__ == '__main__':

	args = []
	count = 0


	with open(os.path.join(DIR, 'MANIFEST'), 'r') as f:
		for line in f:
			count += 1
			filename, checksum = line.strip().split()
			args.append([filename, checksum])

	pool = multiprocessing.Pool()
	results = pool.map_async(md5check, args)
	pool.close()
	pool.join()

	missing = []
	corrupt = []
	for r in results.get():
		if r == None:
			continue
		elif len(r) == 3:
			corrupt.append([str(x) for x in r])
		else:
			missing.append(str(r))

	print('Files analyzed: %d' %count)
	print('Matching MD5: %d' %(count-len(missing) - len(corrupt)))
	print('Missing: %d' %len(missing))
	if missing != []:
		for m in missing:
			print('\t%s' %m)
	print('Corrupted: %d' %len(corrupt))
	if corrupt != []:
		for c in corrupt:
			print('\t%s  %s  %s' %(c[0],c[1],c[2]))