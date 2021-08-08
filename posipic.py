from PIL import Image
import PIL.ExifTags
import os
import argparse
from geopy.geocoders import Nominatim
from os import path

class KML:
    def __init__(self):
        self.placemarklist = []

    def add_placemark(self, name, camera, longi, lati):
        self.placemarklist.append(Placemark(name, camera, longi, lati))

    def output(self):
        outstring = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n" \
                    "<kml xmlns=\"http://www.opengis.net/kml/2.2\">\n\t<Document>\n"
        for placemark in self.placemarklist:
            outstring = outstring + placemark.output()
        outstring = outstring + "\t</Document>\n</kml>\n"
        return outstring


class Placemark:
    def __init__(self, name, camera, longi, lati):
        self.name = name
        self.camera = camera
        self.longi = longi
        self.lati = lati

    def output(self):
        outstring = "\t\t<Placemark>\n\t\t\t<name>{}</name>\n\t\t\t<ExtendedData>" \
                    "\n\t\t\t\t<Data name=\"filename\"><value>{}</value></Data>" \
                    "\n\t\t\t\t<Data name=\"model\"><value>{}</value></Data>" \
                    "\n\t\t\t\t<Data name=\"tool\"><value>{}</value></Data>" \
                    "\t\t\t</ExtendedData>\n\t\t\t<Point>\n\t\t\t\t<coordinates>{},{}</coordinates>\n\t\t\t</Point>" \
                    "\n\t\t</Placemark>\n".format(self.name, self.name, self.camera, "PosiPic 1.0", self.lati, self.longi)
        return outstring

class TAG:
    def __init__(self, tag, name, value):
        self.tag = tag
        self.name = name
        self.value = value

class GPSTAG(TAG):
    def __init__(self, tag, name, value):
        super().__init__(tag, name, value)
        self.gpsfloat = 0
        self.convert()

    def convert(self):
        if self.tag == 2 or self.tag == 4:
            d = float(self.value[0])
            m = float(self.value[1])
            s = float(self.value[2])
            self.gpsfloat = d + (m / 60.0) + (s / 3600.0)


class Images:
    def __init__(self, filepathname):
        self.exiftags = [272, 306, 36867, 34853]
        self.exifgpstags = [1, 2, 3, 4]
        self.exif = False
        self.gps = False
        self.image = False
        self.open(filepathname)

    def open(self, filepathname):
        self.filepathname = filepathname
        self.filename = os.path.basename(filepathname)
        self.taglist = []
        self.gpstaglist = []
        try:
            image = Image.open(self.filepathname)
            self.image = True
            exif_data_PIL = image._getexif()
            if len(exif_data_PIL):
                self.exif = True
            for tagnr in self.exiftags:
                if tagnr in exif_data_PIL:
                    value = exif_data_PIL[tagnr]
                    if tagnr == 34853:
                        self.gps = True
                        for gpstagnr in self.exifgpstags:
                            if gpstagnr in value:
                                subvalue = value[gpstagnr]
                                self.gpstaglist.append(GPSTAG(gpstagnr, PIL.ExifTags.GPSTAGS[gpstagnr], subvalue))
                        #self.address = geolocator.reverse("{},{}".format()
                    else:
                        self.taglist.append(TAG(tagnr, PIL.ExifTags.TAGS[tagnr], value))
            image.close()
            #print('processing {}'.format(self.filepathname))
        except IOError:
            self.image = False
            #print('Skipping file not parsable {}'.format(self.filepathname))

    def output(self):
        outputdict = {'filename': self.filename}
        for tag in self.taglist:
            outputdict[tag.name] = tag.value
        for tag in self.gpstaglist:
            if tag.gpsfloat:
                outputdict[tag.name] = tag.gpsfloat
            else:
                outputdict[tag.name] = tag.value
        return outputdict

def run_posipic(pdir, out):
    imagelist = []
    status = {'result': 0, 'numfiles': 0, 'numimg': 0, 'numexif': 0, 'numgps': 0}
    # Validate input
    if not path.exists(pdir):
        status['result'] = 1 #  No such dir
        return status
    geolocator = Nominatim(user_agent="posipic")
    kml = KML()
    for r, d, f in os.walk(pdir):
        for file in f:
            status['numfiles'] += 1
            img = Images(os.path.join(r,file))
            if img.image:
                # Only add images
                status['numimg'] += 1
                imagelist.append(img)

    for img in imagelist:
        if img.exif:
            status['numexif'] += 1
        if img.gps:
            status['numgps'] += 1
        imgdata = img.output()
        if 'GPSLatitude' in imgdata:
            address = geolocator.reverse("{},{}".format(imgdata['GPSLatitude'], imgdata['GPSLongitude']),
                                         exactly_one=True)
            #print(address)
            kml.add_placemark(imgdata['filename'], imgdata['Model'], imgdata['GPSLatitude'], imgdata['GPSLongitude'])

    try:
        f = open(out, 'w')
        f.write(kml.output())
        f.close()
    except OSError:
        status['result'] = 2  # Unable to save
    return status

if __name__ == "__main__":
    #privesc_parameter = {}
    parser = argparse.ArgumentParser(description='posipic v1.0')
    parser.add_argument('-d', '--dir', help='Directory to search for images with gps exif data', required=True)
    parser.add_argument('-o', '--out', help='Output kml file', required=True)

    args = parser.parse_args()
    run_posipic(args.dir, args.out)




