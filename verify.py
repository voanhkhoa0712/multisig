
from demo.curve import *



px = 2791919217030134880261367517096688539463165688461878137297495257516293508965
py = 10752653959125568890966566729297343219772250331186225368449729616195356057481

rx = 25099358978983554848238841593657940143726438794761932320656938045906904881455
ry = 19162187116871110263897410183426934327846724283887871801900349095524318596225

s = 28796573032610260297090403943384922118949029022494040632249919345822091842259


P = Point(px, py, E)
R = Point(rx, ry, E)
e = hash_signature(P, R, 'multi signature 18TN')
e = bytes_to_long(e)


print(s * G == R + P * e)