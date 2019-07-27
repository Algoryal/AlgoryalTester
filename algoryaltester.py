import time


def results():
	global test_number
	global result_time
	global statuses

	print("Ran " + str(test_number) + " tests in ~" + str(result_time) + "s")
	print ("")
	if 'F' not in statuses:
		print(bcolors.OKGREEN + '--- OK ---' + bcolors.RESET)
	else:
		print(bcolors.FAIL + '--- FAILED ---' + bcolors.RESET)


def time_end():
	global end_time
	global result_time

	end_time = time.time()

	result_time = end_time - start_time
	result_time = round(result_time, 3)


def time_start():
	global start_time

	start_time = time.time()


def assertEquals(output, expected):
	time_start()

	run_assert_equals(output, expected)

	time_end()


class bcolors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	BG = '\033[7m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'
	RESET = '\033[0m'


def show_diff(text, n_text):
	text = str(text)
	n_text = str(n_text)
	import difflib
	seqm = difflib.SequenceMatcher(None, text, n_text)
	output = []
	for opcode, a0, a1, b0, b1 in seqm.get_opcodes():
		if opcode == 'equal':
			output.append(bcolors.RESET+seqm.a[a0:a1])
		elif opcode == 'insert':
			output.append(bcolors.WARNING+" EXTRA: " + bcolors.RESET + seqm.b[b0:b1]+bcolors.RESET)
		elif opcode == 'delete':
			output.append(bcolors.FAIL+" MISSING: " + bcolors.RESET + seqm.a[a0:a1]+bcolors.RESET)
		elif opcode == 'replace':
			output.append(bcolors.OKBLUE+" REPLACED: " + bcolors.RESET + seqm.b[b0:b1]+bcolors.RESET)
		else:
			print("unexpected opcode")
	return ''.join(output)


def run_assert_equals(output, expected):
	global test_number
	global statuses
	test_number += 1
	if str(output) == str(expected):
		print(bcolors.OKGREEN + "Test: " + str(test_number) + " Successful"+bcolors.RESET)
		print(bcolors.OKGREEN+"OK: "+bcolors.RESET+str(output))
		print(show_diff(output, expected))
		print("")
		statuses.append('S')
	else:
		print(bcolors.FAIL + "Test: " + str(test_number)+" Failed"+bcolors.RESET)
		print("Expected: " + bcolors.BOLD + str(expected) + bcolors.RESET)
		print("Actual: " + bcolors.BOLD + str(output) + bcolors.RESET)
		print(show_diff(output, expected))
		print("")
		statuses.append('F')


# Params
test_number = 0
statuses = []
start_time = 0
end_time = 0
result_time = 0
