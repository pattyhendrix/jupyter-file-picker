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
    
    if file_paths == top_losses:
        file_paths = data.valid_ds.x[interp.top_losses(9)[1]]


    def setup(file_paths):
        checkboxes = []
        for fp in file_paths:
            img = make_img(fp)
            checkbox = make_checkbox(checkbox_label, fp)
            checkboxes.append(checkbox)
            display(checkbox, img)
        return checkboxes

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
        for cb in checkboxes:
            if cb.value == True:
                print('Deleting:', cb.file_path)
                os.remove(cb.file_path)

    def make_button(label):
        delete_button = widgets.Button(description=label)
        delete_button.on_click(on_button_click)
        return delete_button

    checkboxes = setup(file_paths)
    display(make_button(button_label))
