import sys
if len(sys.argv) != 3:
    print "Usage:"
    print "python %s <Tiled file> <output file>"%sys.argv[0]
    print ""
    print "Tiled must be set to store layers using CSV"
    print "  To do this goto Edit, Preference, select CSV"
    exit(1)

def convert_bytes(bytes):
    #http://www.5dollarwhitebox.org/drupal/node/84
    bytes = float(bytes)
    if bytes >= 1099511627776:
        terabytes = bytes / 1099511627776
        size = '%.2fT' % terabytes
    elif bytes >= 1073741824:
        gigabytes = bytes / 1073741824
        size = '%.2fG' % gigabytes
    elif bytes >= 1048576:
        megabytes = bytes / 1048576
        size = '%.2fM' % megabytes
    elif bytes >= 1024:
        kilobytes = bytes / 1024
        size = '%.2fK' % kilobytes
    else:
        size = '%.2fb' % bytes
    return size


    
from xml.dom.minidom import parse, parseString
dom = parse(sys.argv[1])
m = dom.getElementsByTagName("layer")
numLayers = len(m)
levelData = None
width,height = None,None
    
print "Stage 1, sanity check."
if dom.getElementsByTagName("map")[0].getAttribute("orientation")!="orthogonal":
    print "Error: Map must be orthogonal."
    exit(2)
    
for layer in m:#sanity check.
    layer.__getitem__=layer.getAttribute
    w = int(layer["width"])
    h = int(layer["height"])
    if layer.getElementsByTagName("data")[0].getAttribute("encoding")!="csv":
        print "Error, encoding must be CSV"
    if width==None:
        width = w
        height = h
    else:
        if w!=width or h!=height:
            print "Error converting, layers must all be the same dimension"
            exit(1)
levelData = [width,height]
print "Stage 2, data extraction and compacting"
layers = [] #(name,[properties],data)
for layer in m:
    layer.__getitem__=layer.getAttribute
    name = layer["name"]
    props = []
    for prop in layer.getElementsByTagName("property"):
        prop.__getitem__=prop.getAttribute
        props.append((prop["name"],prop["value"]))
    data = layer.getElementsByTagName("data")[0]
    vals = map(int,data.childNodes[0].data.replace("\n","").split(","))
    
    printPos = True
    d = []
    for r in xrange(h):
        for c in xrange(w):
            v = vals[r*w+c]
            if v:
                if printPos:
                    d += (r,c),
                    printPos = False
                d.append(v)
            else:
                printPos = True
    layers.append((name,props,d))


print "Stage 3, stringification and compression"
data = "{}".format((levelData,layers))
l = len(data)
factor = 1
try:
    import zlib
    print "Zlib available. Compressing."
    data = zlib.compress(data,9)
    factor = l*1.0/len(data)
except:
    print "Failed to use zlib, defaulting to plain text."
    pass

print "Stage 4, Writing"
out = file(sys.argv[2],"wb")
out.write(data)

print "Filesize:",convert_bytes(len(data))
print "Compression factor: %.2f"%factor
out.close()

print "Stage 5, Testing"
layers2 = None
f = file(sys.argv[2],"rb")
data = f.read()
try:
    import zlib
    data = zlib.decompress(data)
except:
    print "Failed to decompress with zlib"
    pass

try:
    levDat,layers2 = eval(data,{"__builtins__":None},{})#little bit of safety
    if layers2==layers and levDat == levelData:
        print "Passed."
    else:
        print "Failed."
except:
    print "Failed decompression test."
    pass

    




x="""
level = "Level0"

f = file(Utils.LevelData(level))
vals = map(lambda x:x.strip().split(","),f.readlines())

rows = len(vals)
cols = len(vals[0])

ss = pygame.image.load(Utils.ImagePath("town01.png"))

surf = pygame.Surface((cols*32,rows*32))
for row in xrange(rows):
    for col in xrange(cols):
        v = vals[row][col]
        c,r = int(v[0],16),int(v[1:],16)
        tmp = ss.subsurface((c*32,r*32,32,32))
        surf.blit(tmp,(col*32,row*32))

pygame.image.save(surf,"output.png")
        """