text = ''
text += str(50-0) + '.' + str(50 - 0) + ',green,200.200\t'
text += str(200-0) + '.' + str(200 - 0) + ',red,200.200'

msg = text
msg = msg.split('\t')
ms = []
for concaine in msg:
    ms.append(concaine.split(','))

print(ms)
m = []
