import Configuration

def ImagePath(name):
	return Configuration.ImagePath%name
	
    
def AudioPath(name):
	return Configuration.AudioPath%name

def tupleSum(*a):
    return map(sum,zip(*a))
    
num2pos = lambda x:((x-1)/16,(x-1)%16) if x else None
#num2pos = lambda x:((x/16)%32,(x%16)+x/512*16)