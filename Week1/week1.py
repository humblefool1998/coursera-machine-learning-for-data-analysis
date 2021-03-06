# -*- coding: utf-8 -*-
"""Week1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1nerMZtw8Iq6ad87vzHK9byQeudaMEZkx
"""

from google.colab import drive

drive.mount('/content/gdrive')

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
from sklearn.metrics import *
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree
from io import StringIO
from IPython.display import Image
import pydotplus
from sklearn.manifold import TSNE
from matplotlib import pyplot as plt
# %matplotlib inline
rnd_state = 23468

##import pandas as pd
data = pd.read_csv('/content/gdrive/My Drive/Colab Notebooks/sample.csv')
data.info()

data.drop('Unnamed: 32', axis=1, inplace=True)
data.diagnosis = np.where(data.diagnosis=='M', 1, 0) # Decode diagnosis into binary
data.describe()

data.head()

model = TSNE(random_state=rnd_state, n_components=2)
representation = model.fit_transform(data.iloc[:, 2:])

plt.scatter(representation[:, 0], representation[:, 1], 
            c=data.diagnosis, alpha=0.5, cmap=plt.cm.get_cmap('Set1', 2))
plt.colorbar(ticks=range(2));

predictors = data.iloc[:, 2:]
target = data.diagnosis

(predictors_train, predictors_test,
 target_train, target_test) = train_test_split(predictors, target, test_size = .3, random_state = rnd_state)

print('predictors_train:', predictors_train.shape)
print('predictors_test:', predictors_test.shape)
print('target_train:', target_train.shape)
print('target_test:', target_test.shape)

print(np.sum(target_train==0))
print(np.sum(target_train==1))

classifier = DecisionTreeClassifier(random_state = rnd_state).fit(predictors_train, target_train)

prediction = classifier.predict(predictors_test)

print('Confusion matrix:\n', pd.crosstab(target_test, prediction, colnames=['Actual'], rownames=['Predicted'], margins=True))
print('\nAccuracy: ', accuracy_score(target_test, prediction))

out = StringIO()
tree.export_graphviz(classifier, out_file = out, feature_names = predictors_train.columns.values, 
                     proportion = True, filled = True)

graph = pydotplus.graph_from_dot_data(out.getvalue())
img = Image(data = graph.create_png())

with open('output.png', 'wb') as f:
    f.write(img.data)

feature_importance = pd.Series(classifier.feature_importances_, index=data.columns.values[2:]).sort_values(ascending=False)
feature_importance

img