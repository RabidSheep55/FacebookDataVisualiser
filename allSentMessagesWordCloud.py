import json, os, collections, re
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt

with open(os.path.join("temp", "allSentMessages.json"), 'r') as file:
    messages = json.load(file)

pattern = re.compile('[\W_]+')
mess = collections.Counter([pattern.sub('', j.lower()) for i in messages for j in i.split(' ')])
longerWords = collections.Counter([pattern.sub('', j.lower()) if len(j) > 2 else '' for i in messages for j in i.split(' ')])

print(longerWords.most_common(100))

# Create and generate a word cloud image:
wordcloud = WordCloud(scale=1, background_color='white', width=1920, height=1080, max_words=400 ).generate_from_frequencies(longerWords)

# Display the generated image:
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()
