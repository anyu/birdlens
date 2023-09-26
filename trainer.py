from fastcore.all import *
from fastai.vision.all import *
import torch

path = Path('bird_images')

dls = DataBlock(
    blocks=(ImageBlock, CategoryBlock), # inputs = images, output = categories
    get_items=get_image_files,
    splitter=RandomSplitter(valid_pct=0.2, seed=42), # Split  data into training and validation sets
    get_y=parent_label, # get parent folder as name
    item_tfms=RandomResizedCrop(224, min_scale=0.3), # picks a random scaled crop of an image and resize it to 224x224 pixels
    batch_tfms=aug_transforms(), # applies augmentations to an entire batch
).dataloaders(path, bs=32)

print("Completed data loading")

dls.show_batch()

learn = vision_learner(dls, resnet34, metrics=error_rate)
learn.fine_tune(10) # 10 epochs

learn.show_results()

Image.open('test.jpg').to_thumb(256,256)

predict, n, prob = learn.predict(PILImage.create('test.jpg'))
print(f"It's {predict}!")
percent = prob[n]*100
print(f"{percent:.02f}% confident.")

# Export fine-tuned model
learn.export('model.pkl')