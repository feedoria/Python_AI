# from pathlib import Path
# from urllib.request import urlretrieve
# from tkinter import Tk, filedialog

# import cv2
# import numpy as np


# root = Tk()
# root.withdraw()

# selected_file = filedialog.askopenfilename(
#     title="Choose the PNG image",
#     filetypes=[("PNG images", "*.png")]
# )

# if not selected_file:
#     print("No image selected.")
#     raise SystemExit

# input_path = Path(selected_file)
# output_path = input_path.with_name(f"{input_path.stem}_upscaled_4x.png")

# model_path = Path(__file__).parent / "ESPCN_x4.pb"
# model_url = "https://github.com/fannymonori/TF-ESPCN/raw/master/export/ESPCN_x4.pb"

# if not model_path.exists():
#     print("Downloading AI model...")
#     urlretrieve(model_url, model_path)

# image = cv2.imread(str(input_path), cv2.IMREAD_UNCHANGED)

# if image is None:
#     print("Could not open the image.")
#     raise SystemExit

# if image.shape[2] == 4:
#     color = image[:, :, :3]
#     alpha = image[:, :, 3]
# else:
#     color = image
#     alpha = None

# super_resolution = cv2.dnn_superres.DnnSuperResImpl_create()
# super_resolution.readModel(str(model_path))
# super_resolution.setModel("espcn", 4)

# print("Upscaling image...")
# upscaled_color = super_resolution.upsample(color)

# if alpha is not None:
#     upscaled_alpha = cv2.resize(
#         alpha,
#         (
#             upscaled_color.shape[1],
#             upscaled_color.shape[0]
#         ),
#         interpolation=cv2.INTER_LANCZOS4
#     )

#     result = np.dstack((upscaled_color, upscaled_alpha))
# else:
#     result = upscaled_color

# cv2.imwrite(str(output_path), result)

# print(f"Original size: {image.shape[1]}x{image.shape[0]}")
# print(f"Upscaled size: {result.shape[1]}x{result.shape[0]}")
# print(f"Saved here: {output_path}")