import os
from datasets import Dataset, DatasetDict, load_dataset
from PIL import Image
import resource
resource.setrlimit(resource.RLIMIT_NOFILE, (50000,-1))
from sklearn.model_selection import train_test_split

image_folder = "img_files"
tex_folder = "tex_files"

dataset_length = len(os.listdir(image_folder))
dataset_dict = {}
print(f"Dataset length: {dataset_length}")
image_fnames = [f"{image_folder}/{img}" for img in os.listdir(image_folder)]
tex_fnames = [path.replace("jpg", "tex").replace("img", "tex") for path in image_fnames]

images = [Image.open(path) for path in image_fnames if '.jpg' in path]
labels = [open(path, 'r').read() for path in tex_fnames if '.tex' in path]

images, eval_images = train_test_split(images, test_size=0.2, shuffle=False)
labels, eval_labels = train_test_split(labels, test_size=0.2, shuffle=False)

train_dataset_dict = {"images": images, "tex":labels}
eval_dataset_dict = {"images":eval_images, "tex":eval_labels}
train_dataset = Dataset.from_dict(train_dataset_dict)
eval_dataset = Dataset.from_dict(eval_dataset_dict)
dataset = DatasetDict({
    "train":train_dataset,
    "validation":eval_dataset,
})

dataset.push_to_hub("michaelyhuang23/autodiagram2")
