edges = []

def duplicatedInsideInput(n):
	# CHECK THE OCCURANCE EVERY CHARACTER
	for i in n:
		if n.count(i) > 1: return True
	return False

while True:
	n = input(">>> ").split(",")

	duplicated = False
	if duplicatedInsideInput(n):
		# CHECK IF THE INPUTTED ARRAY (n) HAS SAME ELEMENT, EX. (a,a), (b,b)
		duplicated = True
	else:
		d = 0
		for e in edges:
			for i in n:
				if i in e:
					d +=1

			if d >= len(n):
				duplicated = True
				break
			d = 0

	if duplicated:
		print("Invalid Input!")
	else:
		edges.append(n)
