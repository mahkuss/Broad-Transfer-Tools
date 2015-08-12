"""
Tool to compress .fastq files in parallel using system calls to gzip
Accepts a filename as an argument; will search for .fastq files in current
working directory if no argument provided
Will not zip the file if it is not a .fastq
"""

from sys import argv
import os
import multiprocessing
# import functools
# import gzip
import subprocess

def gzip_worker(args):
	"""
	Main function to spawn a worker that will gzip a file if it has .fastq as the extension.
	"""
	p = multiprocessing.current_process()
	print('Start zipping %s: %s %s' %(args[1], p.name, p.pid))
	path = args[0]
	filename = args[1]
	assert os.path.splitext(filename)[1] == '.fastq', '%s is not a fastq file' %filename 
	
	call = 'gzip -c ' + os.path.join(path, filename) + ' > ' + os.path.join(path, filename) + '.gz'
	subprocess.call(call, shell=True)
	print('Completed zipping %s: %s %s' %(filename, p.name, p.pid))


if __name__ == "__main__":
	if len(argv) > 1:
		path, filename = os.path.split(os.path.abspath(argv[1]))
		files = [filename]
	else:
		path = os.getcwd()
		files = [f for f in os.listdir(path) if os.path.splitext(f)[1] == '.fastq']

	print('CPUs Available: %s\n' %multiprocessing.cpu_count())

	args = [ [path, f] for f in files ]

	pool = multiprocessing.Pool()
	results = pool.map_async(gzip_worker, args)
	pool.close()
	pool.join()

	success = True

	for r in results.get():
		if r != None:
			success = False
			print(r)

	if success:
		print('All .fastq files sucessfully compressed')