def top_losses_paths(interpreter, images_folder):
    get_images_paths = images_folder[interpreter.top_losses(len(images_folder))[1]]
    return list(get_images_paths)
