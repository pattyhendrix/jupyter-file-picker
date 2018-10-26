
file = open(im1_path, "rb")
image = file.read()

button = widgets.Button(description='slaughter')


def make_checkboxes(ims):
    checked_boxes = []

    for im in ims:
        img = widgets.Image(value=open(im, 'rb').read(), format='jpg', width=300, height=400)
        checkbox = widgets.Checkbox(value=False, description='Slaughter me')
        checkbox.id=im
        checked_boxes.append(checkbox)
        display(checkbox, img)
    return checked_boxes

def on_button_click(b):
   # print(b)
    for cb in checkboxes:
        if cb.value == True:
            print('deleting', cb.id)
            os.remove(cb.id)

checkboxes = make_checkboxes(five_images_path)


display(button)


button.on_click(on_button_click)
