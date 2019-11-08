import os
import json
import nltk
import torch
from torch.utils.data import Dataset, DataLoader
from skimage import io
nltk.download('words')
words = set(nltk.corpus.words.words())

# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
from google.cloud import language_v1
from google.cloud.language_v1 import enums

# Instantiates a client
#client = language.LanguageServiceClient()
client = language_v1.LanguageServiceClient()
type_ = enums.Document.Type.PLAIN_TEXT
language = "en"
encoding_type = enums.EncodingType.UTF8
unique_ingredients = {}
img_names = []

def walk_json_files(directory):
	count = 0
	ingredients_raw = {}
	for f in os.listdir(directory):
		f_name = f
		f = directory+'/'+f
		img_f = f_name[4:]
		img_f = 'img' + img_f
		img_f = img_f[:-4]
		img_f += 'jpg'
		if count==10:
			break
		img_names.append(img_f)
		with open(f,'r') as f:
			data = json.load(f)
			ingredients_raw[f_name] = data['ingredientLines']

		count+=1
	return ingredients_raw,img_names

def classify_ingredients(raw_ingredients):
	processed_ingredients = {}
	for f in raw_ingredients:
		processed_ingredients[f] = set()
		for ingredient in raw_ingredients[f]:
			ingredient = ' '.join([ingredient.lower() for ingredient in ingredient.split()])
			ingredient = ' '.join(w for w in nltk.wordpunct_tokenize(ingredient) if w.lower() in words or not w.isalpha())
			document = {"content": ingredient, "type": type_, "language": language}
			response = client.analyze_syntax(document,encoding_type=encoding_type)
			i = 0
			while i < len(response.tokens):
				text = response.tokens[i]
				part_of_speech = response.tokens[i].part_of_speech
				if enums.PartOfSpeech.Tag(part_of_speech.tag).name=="NOUN":
					ingr = text.lemma
					while i+1 < len(response.tokens):
						if enums.PartOfSpeech.Tag(response.tokens[i+1].part_of_speech.tag).name=="NOUN":
							ingr += " "
							ingr += response.tokens[i+1].lemma
						else:
							break
						i+=1
					
					processed_ingredients[f].add(ingr)
					#print(u"Token text: {}".format(text.lemma))
					#print(u"Part of Speech tag: {}".format(enums.PartOfSpeech.Tag(part_of_speech.tag).name))
				i+=1
	return processed_ingredients

def remove_outliers(processed_ingredients):
	freq = {}
	unique = {}
	count = 0
	for f in processed_ingredients:
		for ingredient in processed_ingredients[f]:
			for word in ingredient.split():
				if word not in freq:
					freq[word] = 1
				else:
					freq[word] += 1
			if ingredient not in unique:
				unique[ingredient] = count
				count+=1

	return unique
	
def build_graph(processed_ingredients):
	graph = {}
	for f in processed_ingredients:
		for ingredient in processed_ingredients[f]:
			if ingredient not in graph:
				graph[ingredient] = set()
			for each in processed_ingredients[f]:
				if each not in graph[ingredient]:
					graph[ingredient].add(each)

	return graph
	
def to_one_hot(unique_ingredients,processed_ingredients):
	ingredients = {}
	for f in processed_ingredients:
		ingredients[f] = []
		one_hot = [0 for i in range(len(unique_ingredients))]
		for ingredient in processed_ingredients[f]:
			one_hot[unique_ingredients[ingredient]] = 1
		ingredients[f] = one_hot

	return ingredients
		
class IngredientDataset(Dataset):
	def __init__(self,ingredients,img_folder,img_names):
		self.img_names = img_names
		self.ingredients = ingredients
		self.img_folder = img_folder

	def __len__(self):
		return len(self.img_names)

	def __getitem__(self, idx):
		img_name = os.path.join(self.img_folder,str(self.img_names[idx]))
		print(img_name)
		img = io.imread(img_name)
		img_nm = self.img_names[idx]
		img_nm = img_nm[3:]
		img_nm = "meta"+img_nm
		img_nm = img_nm[:-3]
		img_nm += "json"
		ingredient = self.ingredients[img_nm]
		pair = {'img': img, 'ingredient': ingredient}

		return pair
	

raw_ingredients,img_names = walk_json_files("/afs/crc.nd.edu/user/x/xdong2/Graph2Img/Yummly28K/metadata27638")
processed_ingredients = classify_ingredients(raw_ingredients)
unique_ingredients = remove_outliers(processed_ingredients)
ingredients = to_one_hot(unique_ingredients,processed_ingredients)

ingredient_dataset = IngredientDataset(ingredients,'./Yummly28K/images27638',img_names)

for i in range(len(ingredient_dataset)):
	sample = ingredient_dataset[i]
	print(sample)

#graph = build_graph(processed_ingredients)
#print(graph)


