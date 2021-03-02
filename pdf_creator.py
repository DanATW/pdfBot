from PIL import Image


def form_pdf(paths, user_id):
    imagelist = [Image.open(path).convert('RGB') for path in paths]
    imagelist[0].save(
        f'{user_id}.pdf',
        save_all=True,
        append_images=imagelist[1:]
        )
