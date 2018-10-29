# TODO: re-render UI after we delete some photos
# TODO: styling of grid to make it nicer to navigate
# TODO: Write the readme
#
# TODO: Come back to this so function can accept data bunch or top losses
# if file_paths == top_losses:
#     file_paths = data.valid_ds.x[interp.top_losses(10)[1]]


from ipywidgets import widgets, Layout
from IPython.display import clear_output, HTML

def render_file_list(file_paths, button_label="Delete Selected", checkbox_label="Delete me", batch_size=5):
    """
        Takes in a list of fully-qualified file paths to images.
        Opens each image renders blocks with img and checkbox.
        On button click, deletes all selected images.

        written by:
            Zach Caceres @zachcaceres (https://github.com/zcaceres)
            Jason Patnick (https://github.com/pattyhendrix)
            Francisco


    """

    all_images = []
    batch = []

    def main(file_paths):
        """
            Puts all images from file_paths into memory and prepares initial render
        """
        for fp in file_paths:
            fp = Path(fp) # always convert to Posix path if not
            if (os.path.isfile(fp)):
                img = make_img(fp)
                delete_btn = make_button('Delete', file_path=fp, handler=on_delete)
                all_images.append((img, delete_btn, fp))
        render()

    def make_img(file_path):
        opened_file = open(file_path, 'rb')
        read_file = opened_file.read()
        img = widgets.Image(value=read_file, format='jpg', layout=Layout(width="300px", height="250px"))
        opened_file.close()
        return img

    def on_confirm(btn):
        to_remove = []
        for img, delete_btn, fp in batch:
            fp = delete_btn.file_path
            if (delete_btn.flagged_for_delete == True):
                delete_image(fp)
            to_remove.append((img, delete_btn, fp))
        for img, delete_btn, fp in to_remove:
            all_images.remove((img, delete_btn, fp))
        empty_batch()
        render()

    def empty_batch():
        batch[:] = []

    def delete_image(file_path):
        os.remove(file_path)

    def on_delete(btn):
        """
            Flags this image as delete or keep.
        """
        if (btn.flagged_for_delete is True):
            btn.flagged_for_delete = False
            btn.button_style = ""
        else:
            btn.flagged_for_delete = True
            btn.button_style = "danger"

    def make_button(label, file_path=None, handler=None, style=None):
        btn = widgets.Button(description=label)
        if (handler is not None):
            btn.on_click(handler)
        if (style is not None):
            btn.button_style = style
        btn.file_path = file_path
        btn.flagged_for_delete = False
        return btn

    def render():
        clear_output()
        if (len(all_images) == 0):
            return display('No images to show :)')
        widgets_to_render = []
        for img, delete_btn, fp in all_images[:batch_size]:
            widgets_to_render.append(widgets.VBox([img, delete_btn], layout=Layout(width='auto', height='300px')))
            batch.append((img, delete_btn, fp))
        display(widgets.HBox(widgets_to_render))
        display(make_button('Confirm', handler=on_confirm, style="primary"))

    main(file_paths)
