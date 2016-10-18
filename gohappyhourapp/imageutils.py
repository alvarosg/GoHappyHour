

def ObtainReducedSize(width_in,height_in,maxsize):

	if width_in<=maxsize and height_in<=maxsize:
		size= (width_in,height_in)
	else:
		if width_in>height_in:
			size= (maxsize,maxsize*height_in/width_in)
		else:
			size= (maxsize*width_in/height_in,maxsize)

	print maxsize, width_in,height_in
	print size
	return size

def ObtainSizeLocationPicture(width_in,height_in):
	return ObtainReducedSize(width_in,height_in,600)

def ObtainSizeOfferPicture(width_in,height_in):
	return ObtainReducedSize(width_in,height_in,600)

def ObtainSizeLocationThumbnail(width_in,height_in):
	return ObtainReducedSize(width_in,height_in,50)

def ObtainSizeOfferThumbnail(width_in,height_in):
	return ObtainReducedSize(width_in,height_in,50)
    