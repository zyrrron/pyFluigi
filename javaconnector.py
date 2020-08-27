import jpype

import jpype.imports

from jpype.types import *

jpype.startJVM(classpath=['./pnr/fluigi-java/Fluigi-jar-with-dependencies.jar'])

import java
from org.cidarlab.fluigi.fluigi import *


test = dict()
test['flowChannelWidth'] = int(100)
test['controlChannelWidth'] = int(50)
test['chamberLength'] = int(100)
test['chamberWidth'] = int(100)
test['portRadius'] = int(100)
# map = JObject(test , JClass('java.util.Map'))
# print(Fluigi.testME2(map))
mint = "LOGIC ARRAY"
print(Fluigi.getDimensions(mint, java.util.HashMap(test)))