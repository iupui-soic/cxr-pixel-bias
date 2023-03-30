import numpy as np
import png, os, pydicom, pathlib, cv2

#source folder of DICOM files
#output folder for PNG files
source_path = r'path_to_folder'
output_folder = r'path_to_folder'

#traverse all paths and find all DICOM files
paths = []
for path, subdirs, files in os.walk(source_path):
    for name in files:
        temp  = os.path.join(path)
        if temp not in paths:
            paths.append(temp + '\\')

#conversion process for DICOM images
def dicom2png(source_folder, output_folder):
    list_of_files = os.listdir(source_folder)
    for file in list_of_files:
        ds = pydicom.dcmread(os.path.join(source_folder,file))
        shape = ds.pixel_array.shape

        # Convert to float to avoid overflow or underflow losses.
        image_2d = ds.pixel_array.astype(float)
        
        #if the image is monochrome1 then it will be inverted so uninvert it
        if ds.PhotometricInterpretation == "MONOCHROME1":
            image_2d = np.amax(image_2d) - image_2d

        # Rescaling grey scale between 0-255
        image_2d_scaled = (np.maximum(image_2d,0) / image_2d.max()) * 255.0

        
        # Convert to uint
        image_2d_scaled = np.uint8(image_2d_scaled)

        # Write the PNG file
        with open(os.path.join(output_folder,file)+'.png' , 'wb') as png_file:
            w = png.Writer(shape[1], shape[0], greyscale=True)
            w.write(png_file, image_2d_scaled)
                
        
        #except:
            #print('Could not convert: ', file)

for path in paths:
    dicom2png(path, output_folder)
    print(path)
