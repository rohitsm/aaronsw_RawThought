array = []
#current_link = "http://www.aaronsw.com/weblog/oclcscam"
current_link = "http://www.aaronsw.com/weblog/newobjectivity"
m=0
for line in open("EntryLinks.txt", "r").readlines():
	array.append(line.strip("\n"))

print array.index(current_link)
print array[array.index(current_link)]
