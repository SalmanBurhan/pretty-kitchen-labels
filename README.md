# pretty-kitchen-labels
 Generating pretty multilingual (EN/UR) spice/pantry labels using the
 Pillow library.

# Usage
 1. In the `labels.json` file, define the list of entries in the following form:
```json
[
    {
        "name": "Name in English",
        "name_ur": "نام اردو میں",
        "category": "Category Name in English"
    }
]
```
2. Create an empty directory named `labels`.

3. Run ```shell python main.py```
