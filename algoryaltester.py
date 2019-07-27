import time


class BColors:
	def __init__(self):
		pass

	HEADER = '\033[95m'
	OK_BLUE = '\033[94m'
	OK_GREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	BG = '\033[7m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'
	RESET = '\033[0m'


def results(write_to_config_file):
	import json
	global test_number
	global result_time
	global statuses
	global test_output
	status = ''
	output = ''

	print("Ran " + str(test_number) + " tests in ~" + str(result_time) + "s")
	print("")

	test_output.append("Ran " + str(test_number) + " tests in ~" + str(result_time) + "s")
	test_output.append("")

	if 'F' not in statuses:
		print(BColors.OK_GREEN + '--- OK ---' + BColors.RESET)

		status = 'Successful'
		test_output.append('--- OK ---')
	elif 'F' in statuses and 'S' in statuses:
		print(BColors.WARNING + '--- WARNING ---' + BColors.RESET)

		status = 'Warning'
		test_output.append('--- WARNING ---')
	else:
		print(BColors.FAIL + '--- FAILED ---' + BColors.RESET)

		status = 'Failed'
		test_output.append('--- FAILED ---')

	data = {
		"status": status,
		"output": test_output,
		"time": result_time
	}
	if write_to_config_file:
		with open('test.json', 'w+') as f:
			json.dump(data, f)


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


def show_diff(text, n_text):
	import difflib
	global test_output

	text = str(text)
	n_text = str(n_text)
	sequence = difflib.SequenceMatcher(None, text, n_text)
	output = []
	for op_code, a0, a1, b0, b1 in sequence.get_opcodes():
		if op_code == 'equal':
			output.append(BColors.RESET+sequence.a[a0:a1])
		elif op_code == 'insert':
			output.append(BColors.WARNING+" EXTRA: " + BColors.RESET + sequence.b[b0:b1]+BColors.RESET)
		elif op_code == 'delete':
			output.append(BColors.FAIL+" MISSING: " + BColors.RESET + sequence.a[a0:a1]+BColors.RESET)
		elif op_code == 'replace':
			output.append(BColors.OK_BLUE+" REPLACED: " + BColors.RESET + sequence.b[b0:b1]+BColors.RESET)
		else:
			print("unexpected op_code")

			test_output.append("unexpected op_code")
	return ''.join(output)


def run_assert_equals(output, expected):
	global test_number
	global statuses
	global test_output

	test_number += 1
	if str(output) == str(expected):
		print(BColors.OK_GREEN + "Test: " + str(test_number) + " Successful"+BColors.RESET)
		print(BColors.OK_GREEN+"OK: "+BColors.RESET+str(output))
		print(show_diff(output, expected))
		print("")

		statuses.append('S')

		test_output.append("Test: " + str(test_number) + " Successful")
		test_output.append("OK: "+str(output))
		test_output.append(
			show_diff(output, expected).replace(
				"\u001b[0m", ''
			).replace(
				"\u001b[93m", ''
			).replace(
				"\u001b[94m", ''
			).replace(
				"\u001b[91m", ''
			)
		)
		test_output.append("")
	else:
		print(BColors.FAIL + "Test: " + str(test_number)+" Failed"+BColors.RESET)
		print("Expected: " + BColors.BOLD + str(expected) + BColors.RESET)
		print("Actual: " + BColors.BOLD + str(output) + BColors.RESET)
		print(show_diff(output, expected))
		print("")

		statuses.append('F')

		test_output.append("Test: " + str(test_number)+" Failed")
		test_output.append("Expected: " + str(expected))
		test_output.append("Actual: " + str(output))
		test_output.append(
			show_diff(output, expected).replace(
				"\u001b[0m", ''
			).replace(
				"\u001b[93m", ''
			).replace(
				"\u001b[94m", ''
			).replace(
				"\u001b[91m", ''
			)
		)
		test_output.append("")


# Params
test_number = 0
statuses = []
start_time = 0
end_time = 0
result_time = 0
test_output = []

results(True)
