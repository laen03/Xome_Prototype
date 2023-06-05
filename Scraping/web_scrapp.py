import os
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import io
from PIL import Image
import time

PATH = "C:\\Users\\Journey Admin\\OneDrive - Icrave Design\\Projects\\Python\\Xome\\Scraping"

wd = webdriver.Chrome(PATH)

def get_images_from_google(wd, delay, max_images):
	def scroll_down(wd):
		wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		time.sleep(delay)

	url = "https://www.xome.com/auctions"
	wd.get(url)

	image_urls = set()
	skips = 0

	while len(image_urls) + skips < max_images:
		scroll_down(wd)

		thumbnails = wd.find_elements(By.CLASS_NAME, "property-link")

		for img in thumbnails[len(image_urls) + skips:max_images]:
			try:
				img.click()
				time.sleep(delay)
			except:
				continue
			modalParent = wd.find_elements(By.CLASS_NAME, "modal")
			for modal in modalParent:
       			z = modal.find_elements_by_css_selector("*")
    			print("Imagen modal:", z)
				for x in z:
					print(x)
				#Al parecer no hace una busqueda en profundidad, sino que se queda buscando en los mismos hijos del modal actual
				"""			
    			images = modal.find_elements(By.CLASS_NAME, "map-link1")
    			print("Images: ", images)
				for image in images:
					print("imagen como tal", img.get_attribute('class'))
					children = image.find_elements(By.TAG_NAME,"img")
					for child in children:
						print("por obtener el enlace")
						if child.get_attribute('src') in image_urls:
							print(">>>>>>>>>>>>>> Hizo skip!!")
							max_images += 1
							skips += 1
							break

						if child.get_attribute('src') and 'http' in child.get_attribute('src'):
							image_urls.add(child.get_attribute('src'))
							print(f"Found {len(image_urls)}")
			print("close button")
			for close in modalParent:
				closeButton = modal.find_elements(By.CLASS_NAME, "close-link")

				try:
					closeButton.click()
					time.sleep(delay)
				except:
					continue
				"""		
	return image_urls


def download_image(download_path, url, file_name):
	try:
		image_content = requests.get(url).content
		image_file = io.BytesIO(image_content)
		image = Image.open(image_file)
		file_path = download_path + file_name

		with open(file_path, "wb") as f:
			image.save(f, "JPEG")

		print("Success")
	except Exception as e:
		print('FAILED -', e)

urls = get_images_from_google(wd, 1, 6)

destinationFolderName = "imgs"
folderExists = os.path.exists(PATH + "\\" + destinationFolderName)
if not folderExists:
	os.makedirs(PATH + "\\" + destinationFolderName)


for i, url in enumerate(urls):
	download_image("imgs/", url, str(i) + ".jpg")

wd.quit()