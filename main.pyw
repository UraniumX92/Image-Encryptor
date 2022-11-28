"""
XOR Image Encryptor
"""

from encryptor import ImageEncryptor

path = str(__file__)
plist = path.split('\\')
plist[-1] = 'img\enc.ico'
icon_path = "\\".join(plist)

app = ImageEncryptor(geometry="1200x700",icon=icon_path)
app.mainloop()
