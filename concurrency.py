import concurrent.futures as futures

mopeExecutor = futures.ThreadPoolExecutor(max_workers=4)

def runc(task):
	return mopeExecutor.submit(task)