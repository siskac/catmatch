from google_images_download import google_images_download

cat_breedTuples = [('maine_coon', 'maine coon'), ('norwegian_forest', 'norwegian forest'), \
		   ('russian_blue', 'russian blue'), ('selkirk_rex', 'selkirk rex'), \
		   ('siberian', 'siberian cat'), ('siamese', 'siamese cat'), \
		   ('egyptian_mau', 'egyptian mau'), ('american_shorthair', 'american shorthair cat'), \
		   ('cornish_rex', 'cornish rex'), ('british_shorthair', 'british shorthair cat'), \
		   ('scottish_fold', 'scottish fold cat'), ('ragdoll', 'ragdoll cat'), \
		   ('persian', 'persian cat'), ('devon_rex', 'devon rex'), \
		   ('abyssinian', 'abyssinian cat'), ('munchkin', 'munchkin cat'), \
		   ('sphynx', 'sphynx cat'), ('turkish_angora', 'turkish angora'), ('bengal', 'bengal cat'), \
		   ('birman', 'birman cat'), ('savannah', 'savannah cat'), ('himalayan', 'himalayan cat'), \
		   ('exotic', 'exotic shorthair'), ('burmese', 'burmese cat'), \
		   ('manx', 'manx cat'), ('balinese', 'balinese cat'), ('ragamuffin', 'ragamuffin cat')]
# bombays are black burmese cats
# cats to def have point coloration: balinese, himalayan, siamese, birman
# persians are one color
# abysinnians are always ticked
# sphynx cat - do not look into coat
# always spotted: egyptian mau

coat_patternTuples = [('tuxedo', 'tuxedo cat'), ('tortoise', 'tortoise cat'), ('van', 'van cat'), \
		      ('spotted_tabby', 'spotted tabby cat'), ('mackeral_tabby', 'mackeral tabby cat'), \
		      ('calico', 'calico cat'), ('harlequin', 'harlequin coat cat'), \
		      ('snowshoe', 'snowshoe cat'), ('classic_tabby', 'classic tabby cat'), \
		      ('van', 'van cat'), ('ticked_tabby', 'ticked tabby cat'), ('point', 'color point cat')] 
# point coats will be combo of coat_pointTuples

coat_colorTuples = [('red', 'red color cat'), ('chocolate', 'chocolate coat cat'), ('cream', 'cream color cat'), \
		    ('black', 'black cat'), ('lilac', 'lilac cat'), ('blue', 'blue coat cat'), ('fawn', 'fawn color cat'), \
		    ('smoke', 'smoke coat cat'), ('white', 'white coat cat')]

response = google_images_download.googleimagesdownload()



global arguments
global path

arguments = {'keywords': '', 'limit': 500, 'image_directory': '', 'output_directory': '', 'chromedriver': '/usr/local/bin/chromedriver'}
path = '/Users/siskac/repos/whatcat/images/'

def catImages(catTuples, type_dir):
	arguments['output_directory'] = path + type_dir 
	for cat in catTuples:
		print cat[1]
		arguments['keywords'] = cat[1]
		arguments['image_directory'] = cat[0]
		try:
			absolute_image_paths = response.download(arguments)
		except:
			pass

catImages(cat_breedTuples, 'breed')
catImages(coat_pointTuples, 'coat_point')
catImages(coat_colorTuples, 'coat_color')
catImages(coat_patternTuples, 'coat_pattern')
