from .utils import ALIGN_LEFT, ALIGN_RIGHT, ALIGN_V_CENTER, ALIGN_H_CENTER, ALIGN_TOP, ALIGN_BOTTOM


class Image(object):
    def __init__(self, image_str=None):
        self.width = 0
        self.height = 0
        self.lines = []

        if image_str:
            self.load(image_str)


    def load(self, image_str):
        lines = image_str.split('-')
        self.width = len(bin(int(lines[0], 16))[3:])
        self.height = len(lines)

        self.lines = []
        for line in lines:
            bin_str = int(bin(int(line, 16))[3:], 2)
            self.lines.append(bin_str)


    @classmethod
    def create(cls, width, height):
        new_image = cls()
        new_image.width = width
        new_image.height = height
        for _ in range(height):
            new_image.lines.append(0)

        return new_image


    def paint(self,
              painter,
              paint_area,
              invert = False,
              paint_callback = None,
              alignment=0):
        """
        Paint the given image as pixels. Image defines lines of pixels that create an image.

        :param QPainter painter: the painter object for the widget
        :param paint_area: x, y, width, height of paintable area
        :param invert: if True, switch which pixels to draw
        :param paint_callback: function to draw/paint the pixel
        :param alignment: alignment of text image inside paint area
        """
        if not paint_callback:
            return

        x, y, width, height = paint_area

        offset = [0, 0, 0, 0]

        # calculate width alignment
        #
        width_diff = width - self.width
        if alignment & ALIGN_LEFT:
            offset[2] = width_diff
        elif alignment & ALIGN_RIGHT:
            offset[0] = width_diff
        else:
            centered = width_diff / 2.0
            offset[0] = int(centered)
            offset[2] = width_diff - offset[0]

        # calculate height alignment
        #
        height_diff = height - self.height
        if alignment & ALIGN_TOP:
            offset[3] = height_diff
        elif alignment & ALIGN_BOTTOM:
            offset[1] = height_diff
        else:
            centered = height_diff / 2.0
            offset[3] = int(centered)
            offset[1] = height_diff - offset[3]

        # fill in remaining area
        #
        if invert:
            for i in range(offset[1]):
                for j in range(width):
                    paint_callback(painter, x + j, y + i)

            for i in range(offset[3]):
                for j in range(width):
                    paint_callback(painter, x + j, y + i + offset[1] + self.height)

            for i in range(offset[1], height - offset[3]):
                for j in range(offset[0]):
                    paint_callback(painter, x + j, y + i)
                for j in range(offset[2]):
                    paint_callback(painter, x + j + offset[0] + self.width, y + i)

        for i in range(self.height):
            line = self.lines[i]
            check = 1 << (self.width - 1)

            for j in range(self.width):
                paint = bool(line & check)

                if invert:
                    paint = not paint

                if paint:
                    paint_callback(painter, x + j + offset[0], y + i + offset[1])

                check >>= 1


    def __add__(self, image):
        new_image = Image()
        new_image.width = self.width + image.width
        new_image.height = self.height + image.height




TITLE_IMAGE = '800c00000000000000c00007-801e00000004030001e000f9-807e0000f01c070087e00f81-80fe0381f07e1f01cff1f801-81'\
'ff1f81f0fe3f03efff0001-83ff1f81f0fe3f03f7f8000f-87ff1fc3f1fe1f87ef20031f-8ffe1fc3e1fe1f8fde201f18-8ff01fe3e3ff039fb8'\
'301f18-9fe03fe3e3ef0bbf781f1918-9f803fe3e3cf3bff780f1918-bf003ff3e7cffdfe78811918-be001ef3e7c7fdfc7bc11918-fc0fcefbe'\
'f87fdf83fc11918-fcffee7bef8ff1f83e011918-ffffee7fefbfc7fc3c01191f-ffffee3fefffc7fe1c711919-bf07ee1fdfffe7ff1cf11e01-'\
'800fee1fdfe3e7df9ff11801-801fde0fdf03e7cf8fe7000f-803fde0e1f0103c70f98007f-80ffbe007f007bc20f1003f8-83ff78007e01c840'\
'04101fc0-9ffe600008030f000018fe00-9ffc000003de71f8000ff000-9ff000000630c00c00078000-9fc000000589c00400020000-8f00000'\
'006c2d00600000000-8c00007ffad423c200000000-800003d55719868300000000-80001eaabc0000c100000000-8000f555e00000430000000'\
'0-8007aaabfff001ffc0000000-800d555f8008ff1578000000-801aabf0c003901aac000000-80355e00700d303556000000-802ff3802ff960'\
'7ebff80000-803af6802585c0c1e00e0000-80775d801583818700038700-8068eb000d83031c00009880-81d47580038606300ff07040-87aaf'\
'fe0068c0c607eb86c20-8d55f5ffe89818c1cd682610-9afaabaaa130318376ac3f08-95dd555560606306c5742788-9beaaaaae0c0c20d1ebeb'\
'086-95555555c181861b7d7d3ec5-9aeaffbf430304323ffafcc5-957fe4e24606042343ffc1c2-8ebfe4828c0cf431a0000ae2-875ff57b0819'\
'f419500035e3-80ebf2085833f60cbf00fbe1-8075fc6f9067f30651ff95f1-811afaafb04ff98320002bf1-8fcd6327a0cffcc1900055f1-bfe'\
'6b7f7a0c7fe64c8001bf1-fff35f57a0f1ff344781f671-fff9afb7a09c0f1868ff2b31-fffcd7e7b007e07024009692-fffe77cf98003fc0280'\
'02c7c-bffe031fcc0000006f81f001-8ffffb9fe7800000c0ff07ff-81fffbcff0f800079e007ff8-801ffd2ffe0ffffc3fffff80-8000000000'\
'00000000000000-800000000000000000000000-800000000000000000000000-800000000000000000000000-8000000eeeee1d5ddc000000-8'\
'000000aa88811c914000000-8000000eeeee19c99c000000-80000008c822114918000000-80000008aeee1d49d4000000-80000000000000000'\
'0000000-800000000000000000000000-800000000000000000000000'

title = Image(TITLE_IMAGE)