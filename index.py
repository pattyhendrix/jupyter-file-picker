# TODO: re-render UI after we delete some photos
# TODO: styling of grid to make it nicer to navigate
# TODO: Write the readme
# TODO: add progress bar

# Two buttons: OK and Delete
# Click OK and the file path is removed from memory but not deleted
# Delete does both
# What if we called a render() function every time we do these mutations so we could
# immediately refresh the list on every button click?
# Live feed.

from ipywidgets import widgets

def render_file_list(file_paths, button_label="Delete Selected", checkbox_label="Delete me"):
    """
        Takes in a list of fully-qualified file paths to images.
        Opens each image renders blocks with img and checkbox.
        On button click, deletes all selected images.
    """

    image_checkbox_pairs = []

    def setup(file_paths):
        for fp in file_paths:
            img = make_img(fp)
            checkbox = make_checkbox(checkbox_label, fp)
            image_checkbox_pairs.append((img, checkbox, fp))

    def make_img(file_path):
        opened_file = open(file_path, 'rb')
        read_file = opened_file.read()
        img = widgets.Image(value=read_file, format='jpg', width=300, height=400)
        opened_file.close()
        return img

    def make_checkbox(checkbox_label, file_path):
        cb = widgets.Checkbox(value=False, description=checkbox_label)
        cb.file_path = file_path
        return cb

    def on_button_click(b):
        for img, cb, fp in image_checkbox_pairs:
            if cb.value == True:
                print('Deleting:', cb.file_path)
                os.remove(cb.file_path)
                image_checkbox_pairs = [tuple for tuple in image_checkbox_pairs if tuple[1].value is not True]
        render()

    def make_button(label):
        delete_button = widgets.Button(description=label)
        delete_button.on_click(on_button_click)
        return delete_button

    def render():
        print('re-rendering!', len(image_checkbox_pairs))
        display(image_checkbox_pairs)

    setup(file_paths)
    display(make_button(button_label))
