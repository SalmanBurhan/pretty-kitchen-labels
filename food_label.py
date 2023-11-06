#!/opt/homebrew/bin/python3

from PIL import Image, ImageDraw, ImageFont
import enum


class LOCATIONS(enum.Enum):
    TOP_LEFT = enum.auto()
    CENTER = enum.auto()
    FOOD_NAME = enum.auto()
    FOOD_NAME_UR = enum.auto()
    FOOD_CATEGORY = enum.auto()


class FoodLabel:

    def __init__(self, name: str, name_ur: str, category: str, width=1024, height=1024):
        self.IMAGE = Image.new('RGB', (width, height), 'white')
        self.DRAW = ImageDraw.Draw(self.IMAGE)

        self.NAME = name
        self.NAME_UR = name_ur
        self.CATEGORY = category

        self.NAME_LOCATION = [(0, 0), (0, 0)]
        self.NAME_UR_LOCATION = [(0, 0), (0, 0)]
        self.LINE_LOCATION = [(0, 0), (0, 0)]
        self.CATEGORY_LOCATION = [(0, 0), (0, 0)]

        self.__render(name, name_ur, category)

    @property
    def __size(self):
        return self.IMAGE.size

    @property
    def __width(self):
        return self.__size[0]

    @property
    def __height(self):
        return self.__size[1]

    def __coordinates_for(self, text: str, font, location: LOCATIONS = LOCATIONS.TOP_LEFT):
        if location == LOCATIONS.TOP_LEFT:
            return (0, 0)
        elif location == LOCATIONS.CENTER:
            text_width, text_height = self.DRAW.textsize(text, font=font)
            return ((self.__width - text_width) / 2, (self.__height - text_height) / 2)
        elif location == LOCATIONS.FOOD_NAME:
            text_width, text_height = self.DRAW.textsize(text, font=font)
            coordinates = ((self.__width - text_width) / 2,
                           (self.__height - text_height) / 4)
            self.NAME_LOCATION = [coordinates, (text_width, text_height)]
            return coordinates
        elif location == LOCATIONS.FOOD_NAME_UR:
            text_width, text_height = self.DRAW.textsize(text, font=font)
            coordinates = ((self.__width - text_width) / 2,
                           self.NAME_LOCATION[0][1] + self.NAME_LOCATION[1][1])
            self.NAME_UR_LOCATION = [coordinates, (text_width, text_height)]
            return coordinates
            # return ((self.__width - text_width) / 2, (self.__height - text_height) / 2 - (text_height / 1.5))
        elif location == LOCATIONS.FOOD_CATEGORY:
            text_width, text_height = self.DRAW.textsize(text, font=font)
            coordinates = ((self.__width - text_width) / 2,
                           self.LINE_LOCATION[0][1] + self.LINE_LOCATION[1][1] + 18)
            self.CATEGORY_LOCATION = [coordinates, (text_width, text_height)]
            return coordinates
            # return ((self.__width - text_width) / 2, (self.__height - text_height) / 2 + (text_height * 2.25))

    def __font(self, face='Montserrat', weight='Regular', size=30):
        return ImageFont.truetype(f'fonts/{face}/{face}-{weight}.ttf', size)

    def __text(self, text, location: LOCATIONS = LOCATIONS.TOP_LEFT, color=(0, 0, 0), font=None):
        font = self.__font(font[0], font[1], font[2]
                           ) if font else self.__font()
        self.DRAW.text(
            self.__coordinates_for(text, font, location),
            text,
            fill=color,
            align="center",
            font=font
        )

    def __line(self):
        shape = [
            (self.__width / 2 - 50,
             self.NAME_UR_LOCATION[0][1] + self.NAME_UR_LOCATION[1][1] + 25),
            (self.__width / 2 + 50,
             self.NAME_UR_LOCATION[0][1] + self.NAME_UR_LOCATION[1][1] + 25)
        ]
        self.LINE_LOCATION = [shape[0], (shape[0][0] + shape[1][0], 3)]
        self.DRAW.line(shape, fill=(0, 0, 0), width=3)

    def __render(self, name: str, name_ur: str, category: str):
        self.__text(name.upper(), LOCATIONS.FOOD_NAME,
                    font=('Montserrat', 'Regular', 60))
        self.__text(name_ur.upper(), LOCATIONS.FOOD_NAME_UR,
                    font=('Cairo', 'Light', 40))
        self.__line()
        self.__text(category.upper(), LOCATIONS.FOOD_CATEGORY,
                    font=('Montserrat', 'LightItalic', 30))

    def show(self):
        self.IMAGE.show()

    def save(self, directory="labels"):
        sanitized_name = self.NAME.replace('\n', ' ')
        sanitized_name_ur = self.NAME_UR.replace('\n', ' ')
        print(f'Saving label:\t{sanitized_name} ({sanitized_name_ur})')
        self.IMAGE.save(f'{directory}/{sanitized_name}.jpeg', 'JPEG')

    ''' debugging
    def data(self):
        f = BytesIO()
        self.IMAGE.save(f, 'JPEG')
        f.seek(0)
        return f
    '''
