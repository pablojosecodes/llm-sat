
d = '''
1. C
2. B
3. A
4. A
5. C
6. B
7. D
8. B
9. C
10. B
11. A
'''


import re
output = re.sub(r'\d+', '', d)
output = output.replace('. ', "")
print(output)  # 'hello world'
