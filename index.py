# TODO: re-render UI after we delete some photos
# TODO: styling of grid to make it nicer to navigate
# TODO: Write the readme
# TODO: add progress bar

from ipywidgets import widgets, Layout
from IPython.display import clear_output, HTML

def render_file_list(file_paths, button_label="Delete Selected", checkbox_label="Delete me"):
    """
        Takes in a list of fully-qualified file paths to images.
        Opens each image renders blocks with img and checkbox.
        On button click, deletes all selected images.
    """

    image_checkbox_pairs = []

    def main(file_paths):
        for fp in file_paths:
            img = make_img(fp)
            checkbox = make_checkbox(checkbox_label, fp)
            image_checkbox_pairs.append((img, checkbox, fp))
        render()

    def make_img(file_path):
        opened_file = open(file_path, 'rb')
        read_file = opened_file.read()
        img = widgets.Image(value=read_file, format='jpg', width=300, height=300)
        opened_file.close()
        return img

    def make_checkbox(checkbox_label, file_path):
        cb = widgets.Checkbox(value=False, description=checkbox_label)
        cb.file_path = file_path
        return cb

    def on_button_click(b):
        to_remove = []
        for img, cb, fp in image_checkbox_pairs:
            if cb.value == True:
                os.remove(cb.file_path)
                to_remove.append((img, cb, fp))
        for img, cb, fp in to_remove:
            image_checkbox_pairs.remove((img, cb, fp))
        render()

    def make_button(label):
        delete_button = widgets.Button(description=label)
        delete_button.on_click(on_button_click)
        return delete_button

    def render():
        clear_output()
        children = []
        for img, cb, fp in image_checkbox_pairs:
            children.append(widgets.VBox([img, cb], layout=Layout(height='250px', width='250px')))
        display(widgets.HBox(children[:5]))
        display(make_button(button_label))

    main(file_paths)
