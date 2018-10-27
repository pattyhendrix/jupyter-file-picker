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

    if file_paths == top_losses:
        file_paths = data.valid_ds.x[interp.top_losses(10[1]]


    image_blocks = []

    def main(file_paths):
        for fp in file_paths:
            img = make_img(fp)
            keep_button = make_button('Keep', fp, on_keep)
            delete_button = make_button('Delete', fp, on_delete)
            image_blocks.append((img, keep_button, delete_button, fp))
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

    def on_keep(btn):
        remove_from_list(btn.file_path)
        render()

    def remove_from_list(file_path):
        to_remove = []
        for img, keep_btn, delete_btn, fp in image_blocks:
            if file_path == fp:
                to_remove.append((img, keep_btn, delete_btn, fp))
        for img, keep_btn, delete_btn, fp in to_remove:
            image_blocks.remove((img, keep_btn, delete_btn, fp))

    def on_delete(btn):
        os.remove(btn.file_path)
        remove_from_list(btn.file_path)
        render()

    def make_button(label, file_path, handler):
        btn = widgets.Button(description=label)
        btn.on_click(handler)
        btn.file_path = file_path
        return btn

    def render():
        clear_output()
        children = []
        for img, keep_btn, delete_btn, fp in image_blocks:
            children.append(widgets.VBox([img, keep_btn, delete_btn], layout=Layout(width='250px')))
        display(widgets.HBox(children[:5]))

    main(file_paths)
