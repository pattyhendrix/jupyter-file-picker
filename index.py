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
            Francisco Ingham @inghamfran (https://github.com/lesscomfortable)
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

    def make_img(file_path, height='250px', width='300px', format='jpg'):
        """
            Returns an image widget for specified file name.
        """
        opened_file = open(file_path, 'rb')
        read_file = opened_file.read()
        img = widgets.Image(value=read_file, format=format, layout=Layout(width=width, height=height))
        opened_file.close()
        return img

    def on_confirm(btn):
        """
            Handler for Confirm button click. Deletes all flagged images.
        """
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
        """
            Returns a Button widget with specified handler
        """
        btn = widgets.Button(description=label)
        if (handler is not None):
            btn.on_click(handler)
        if (style is not None):
            btn.button_style = style
        btn.file_path = file_path
        btn.flagged_for_delete = False
        return btn

    def make_vertical_box(children, width='auto', height='300px'):
        return widgets.VBox(children, layout=Layout(width=width, height=height))

    def make_horizontal_box(children):
        return widgets.HBox(children)

    def render():
        """
            Re-renders Jupyter cell for a batch of images.
        """
        clear_output()
        if (len(all_images) == 0):
            return display('No images to show :)')
        widgets_to_render = []
        for img, delete_btn, fp in all_images[:batch_size]:
            widgets_to_render.append(make_vertical_box([img, delete_btn]))
            batch.append((img, delete_btn, fp))
        display(make_horizontal_box(widgets_to_render))
        display(make_button('Confirm', handler=on_confirm, style="primary"))

    main(file_paths)
