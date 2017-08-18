import numpy as np
a = np.arange(15).reshape(3,5)
sh = a.shape
sz = a.size
itemsz = a.itemsize
ndim = a.ndim
dimension_type = a.dtype
np.savetxt('demo_numpy.txt',(a,sh,sz,itemsz,ndim,dimension_type),newline='\r\n',fmt='%s')
