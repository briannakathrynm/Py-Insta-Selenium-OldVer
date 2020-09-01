import urllib


def url_to_img(url, filename):
    """
    Getting the actual photo file or video file from an Instagram url
    Args:
    url: photo/thumbnail URL from insights_details
    filename: filename to be saved to folder
    Returns:
    Image file, saved locally to folder listed below
    """
    image_url = url
    urllib.request.urlretrieve(image_url, ("C://Users/Brianna's HP17/Desktop/post_extraction/" + filename))
