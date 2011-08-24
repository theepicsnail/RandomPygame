import Configuration

def ImagePath(name):
	return Configuration.ImagePath%name
	
    
def AudioPath(name):
	return Configuration.AudioPath%name

def tupleSum(*a):
    return map(sum,zip(*a))