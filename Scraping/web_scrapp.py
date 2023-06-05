import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
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
	nextPageButtonID = "right-navigation"
	imagesPerPage = 0

	while len(image_urls) + skips < max_images:
		scroll_down(wd)

		

		thumbnails = wd.find_elements(By.CLASS_NAME, "property-link")
		for img in thumbnails[len(image_urls) + skips:max_images]:
			# Revisar la cantidad de thumbnails descargados para pasar de página
			# (cuando llega a Found 48 imprimió total thumbnails 250)
			print("imagesPerPage", imagesPerPage)
			try:
				img.click()
				time.sleep(delay)
				imagesPerPage += 1
			except:
				continue
			
			wd.switch_to.frame("iframe-flyout-body")
			try:
				# Some properties don't have an image, the next line is for triggering the except
				wd.find_element(By.CLASS_NAME, "no-image-container")
				print("Property without picture")
				wd.switch_to.default_content()
				closeButton = wd.find_element(By.ID, "top-navigation-flyout-close")
				print("button found")
				closeButton.click()
				time.sleep(delay)
				max_images += 1
				skips += 1
				break
			except NoSuchElementException:
				firstImage = wd.find_element(By.CLASS_NAME, "flex-active-slide")
				images = firstImage.find_elements(By.CLASS_NAME, "map-link1")

				for image in images:
					print("imagen como tal")
					children = image.find_element(By.TAG_NAME,"img")
					if children:
						print("por obtener el enlace")
						if children.get_attribute('src') in image_urls:
							print(">>>>>>>>>>>>>> Hizo skip!!")
							max_images += 1
							skips += 1
							break

						if children.get_attribute('src') and 'http' in children.get_attribute('src'):
							image_urls.add(children.get_attribute('src'))
							print(f"Found {len(image_urls)}")
							break
				wd.switch_to.default_content()
				time.sleep(delay)
				closeButton = wd.find_element(By.ID, "top-navigation-flyout-close")
				try:
					closeButton.click()
					time.sleep(delay)
				except:
					continue
		print("Total thumbnails", len(thumbnails))
		button = wd.find_element(By.ID, "right-navigation")
		try:
			button.click()
			time.sleep(delay)
		except:
			continue		
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

urls = get_images_from_google(wd, 1, 51)

destinationFolderName = "imgs"
folderExists = os.path.exists(PATH + "\\" + destinationFolderName)
if not folderExists:
	os.makedirs(PATH + "\\" + destinationFolderName)


for i, url in enumerate(urls):
	download_image("imgs/", url, str(i) + ".jpg")

wd.quit()