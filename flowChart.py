from pyflowchart import Flowchart

with open('nomor1B.py') as f:
    code = f.read()

fc = Flowchart.from_code(code)
print(fc.flowchart())