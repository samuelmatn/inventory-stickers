import os
import shutil
import pyqrcode
import jinja2

class InventoryElement:
	def __init__(self, code, item, company):
		self.code = code
		self.item = item
		self.company = company

def loadInventory():
	with open('inventory.txt') as input:
		lines = [line.rstrip() for line in input]
	def getElement(offset):
		return InventoryElement(*lines[offset:offset+3])
	return [getElement(offset) for offset in range(0, len(lines), 4)]

def generateCodes(inventory):
	os.makedirs('output/codes')
	for element in inventory:
		code = pyqrcode.create(element.code)
		code.svg('output/codes/' + element.code + '.svg')

def generateStickers(inventory):
	loader = jinja2.FileSystemLoader(searchpath='./')
	environment = jinja2.Environment(loader=loader)
	template = environment.get_template('template/index.html')
	render = template.render(inventory = inventory)
	with open('output/index.html', 'w') as output:
		output.write(render)
	shutil.copyfile('template/style.css', 'output/style.css')

def main():
	inventory = loadInventory()
	if os.path.exists('output'):
		shutil.rmtree('output')
	os.makedirs('output')
	generateCodes(inventory)
	generateStickers(inventory)

if __name__ == "__main__":
	main()