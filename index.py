# TODO: re-render UI after we delete some photos
# TODO: styling of grid to make it nicer to navigate
# TODO: Write the readme
#
# TODO: Come back to this so function can accept data bunch or top losses
# if file_paths == top_losses:
#     file_paths = data.valid_ds.x[interp.top_losses(10)[1]]


from ipywidgets import widgets, Layout
from IPython.display import clear_output, HTML

def render_file_list(file_paths, button_label="Delete Selected", checkbox_label="Delete me"):
    """
        Takes in a list of fully-qualified file paths to images.
        Opens each image renders blocks with img and checkbox.
        On button click, deletes all selected images.
    """

    render_list = []
    batch = []

    def main(file_paths):
        for fp in file_paths:
            img = make_img(fp)
            delete_button = make_button('Delete', file_path=fp, handler=on_delete)
            render_list.append((img, delete_button, fp))
        render()

    def make_img(file_path):
        opened_file = open(file_path, 'rb')
        read_file = opened_file.read()
        img = widgets.Image(value=read_file, format='jpg', width=300, height=300)
        opened_file.close()
        return img

    def on_confirm(btn):
        to_remove = []
        for img, delete_btn, fp in render_list:
            fp = delete_btn.file_path
            if (delete_btn.flagged_for_delete == True):
                delete_image(fp)
            to_remove.append((img, delete_btn, fp))
        for img, delete_btn, fp in to_remove:
            render_list.remove((img, delete_btn, fp))
        render()

    def delete_image(file_path):
        print('deleting', file_path)
        # TODO: REENABLE ME AFTER TESTING! os.remove(file_path)

    def on_delete(btn):
        """
            Flags this image as delete or keep.
        """
        if (btn.flagged_for_delete is True):
            btn.flagged_for_delete = False
            btn.description = "Keep"
            btn.button_style = "success"
        else:
            btn.flagged_for_delete = True
            btn.description = "Delete"
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
        children = []
        if (len(render_list) == 0):
            return display('No images to show :)')
        for img, delete_btn, fp in render_list:
            children.append(widgets.VBox([img, delete_btn], layout=Layout(width='250px')))
        display(widgets.HBox(children[:5]))
        display(make_button('Confirm', handler=on_confirm, style="primary"))

    main(file_paths)
