from io import BytesIO


class BMP:
    """ Class for storing a bmp file image """

    def __init__(self, route):
        stream = open(route, 'rb')  # Opening the file route

        # Bitmap file header
        self.signature = stream.read(2)
        self.size = int.from_bytes(stream.read(4), byteorder='little')
        self.reserved = int.from_bytes(stream.read(4), byteorder='little')
        self.offset = int.from_bytes(stream.read(4), byteorder='little')

        # Bitmap info header
        self.hdr_size = int.from_bytes(stream.read(4), byteorder='little')
        self.width = int.from_bytes(stream.read(4), byteorder='little')
        self.height = int.from_bytes(stream.read(4), byteorder='little')
        self.planes = int.from_bytes(stream.read(2), byteorder='little')
        self.bpp = int.from_bytes(stream.read(2), byteorder='little')
        self.compression = int.from_bytes(stream.read(4), byteorder='little')
        self.img_size = int.from_bytes(stream.read(4), byteorder='little')
        self.h_res = int.from_bytes(stream.read(4), byteorder='little')
        self.v_res = int.from_bytes(stream.read(4), byteorder='little')
        self.palette_size = int.from_bytes(stream.read(4), byteorder='little')
        self.main_colors = int.from_bytes(stream.read(4), byteorder='little')

        # Pixel list
        # For DES the pixel array must be linear
        self.pixels = bytearray()

        # Define the padding for the width to be multiple of 4
        self.padding = (self.width * 3) % 4
        if self.padding != 0:
            self.padding = 4 - self.padding

        # For a list with bytearrays describing RGB components of a pixel
        self.pixels = bytearray(stream.read(self.height * (self.width + self.padding) * 3))

        self.trail = bytearray(stream.read())

        stream.close()


    @staticmethod
    def create_image(bmp, route):
        """This method writes the information within the BMP class to a
             new BMP file.

             All header instance variables are converted to bytes with
             corresponding lengths to the BMP structure and then joined
             with each pixel infromation with the proper padding filled in.
             """

        img = bytes(
            bmp.signature +
            bmp.size.to_bytes(4, byteorder='little', signed=False) +
            bmp.reserved.to_bytes(4, byteorder='little', signed=False) +
            bmp.offset.to_bytes(4, byteorder='little', signed=False) +
            bmp.hdr_size.to_bytes(4, byteorder='little', signed=False) +
            bmp.width.to_bytes(4, byteorder='little', signed=True) +
            bmp.height.to_bytes(4, byteorder='little', signed=True) +
            bmp.planes.to_bytes(2, byteorder='little', signed=False) +
            bmp.bpp.to_bytes(2, byteorder='little', signed=False) +
            bmp.compression.to_bytes(4, byteorder='little', signed=False) +
            bmp.img_size.to_bytes(4, byteorder='little', signed=False) +
            bmp.h_res.to_bytes(4, byteorder='little', signed=True) +
            bmp.v_res.to_bytes(4, byteorder='little', signed=True) +
            bmp.palette_size.to_bytes(4, byteorder='little', signed=False) +
            bmp.main_colors.to_bytes(4, byteorder='little', signed=False))

        img += bmp.pixels

        img += bytes(bmp.trail)

        stream = open(route, 'wb')
        stream.write(img)

    def get_bytes(self):
        """This method writes the information within the BMP class to a
             new BMP file.

             All header instance variables are converted to bytes with
             corresponding lengths to the BMP structure and then joined
             with each pixel infromation with the proper padding filled in.
             """
        img = bytes(
            self.signature +
            self.size.to_bytes(4, byteorder='little', signed=False) +
            self.reserved.to_bytes(4, byteorder='little', signed=False) +
            self.offset.to_bytes(4, byteorder='little', signed=False) +
            self.hdr_size.to_bytes(4, byteorder='little', signed=False) +
            self.width.to_bytes(4, byteorder='little', signed=True) +
            self.height.to_bytes(4, byteorder='little', signed=True) +
            self.planes.to_bytes(2, byteorder='little', signed=False) +
            self.bpp.to_bytes(2, byteorder='little', signed=False) +
            self.compression.to_bytes(4, byteorder='little', signed=False) +
            self.img_size.to_bytes(4, byteorder='little', signed=False) +
            self.h_res.to_bytes(4, byteorder='little', signed=True) +
            self.v_res.to_bytes(4, byteorder='little', signed=True) +
            self.palette_size.to_bytes(4, byteorder='little', signed=False) +
            self.main_colors.to_bytes(4, byteorder='little', signed=False))

        img += self.pixels

        img += bytes(self.trail)

        return img