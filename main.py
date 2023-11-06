#!/opt/homebrew/bin/python3

from food_label import FoodLabel
import json

if __name__ == "__main__":
    for label in json.load(open('labels.json', 'r')):
        image = FoodLabel(
            label.get('name'),
            label.get('name_ur'),
            label.get('category'),
            width=512,
            height=512
        )
        image.save()
