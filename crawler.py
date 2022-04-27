from bs4 import BeautifulSoup
import requests
import argparse
import os

def parse_arguments():
    """
    parse_arguments Parses the command-line arguments provided by the user.
    
    :return: Namespace of arguments
    """ 
    parser = argparse.ArgumentParser(description='Downloads .png images from URL')

    # add required arguments section
    required_arguments = parser.add_argument_group('required arguments')
    # add required arguments
    required_arguments.add_argument('-u', "--url", help='URL as source of images', required=True)
    required_arguments.add_argument('-o', "--output_dir", help='Output directory for downloaded images', required=True)
    # add optional arguments
    parser.add_argument('-n', "--username", help='Username for BasicAuth')
    parser.add_argument('-p', "--password", help='Password for BasicAuth')

    return parser.parse_args()

def create_output_dir(output_dir):
    """
    create_output_dir Creates directory recursively(with parents).

    :param output_dir: Directory to be created
    """ 
    try:
        # create directory recursively, skip if exists
        os.makedirs(output_dir, exist_ok=True)
    except Exception as e:
        print(f"Failed to create output directory!\n{e}")
        exit(1)

def make_request(url, username, password):
    """
    make_request Makes GET request to URL with basic auth.

    :param url: Endpoint for the request
    :param username: Username for basic auth
    :param password: Password for basic auth
    :return (response, exception): The response of the request, or exception if error occured
    """ 
    # initial empty response
    response = None
    # initial empty exception
    exception = None

    try:
        # get content of URL, with auth if provided
        if username and password:
            response = requests.get(url, auth=(username, password))
        else:
            response = requests.get(url)
    except Exception as e:
        exception = e

    return response, exception

def get_image_url(image):
    """
    get_image_url Gets the image URL from html tag.

    :param image: The image html tag
    :return image_url: The endpoint of the image
    """ 
    image_url = None
    # Look for image URL in 4 properties
    if image.has_attr("data-srcset"):
        image_url = image["data-srcset"]
    elif image.has_attr("data-src"):
        image_url = image["data-src"]
    elif image.has_attr("data-fallback-src"):
        image_url = image["data-fallback-src"]
    elif image.has_attr("src"):
        image_url = image["src"]

    return image_url

def write_content_to_file(content, file):
    """
    write_content_to_file Writes content to a file.

    :param content: The content tobe written
    :param file: The full path filename where the content is written
    :return (write_success, exception): The success of the writing and error if it wasn't
    """ 
    # initial false success
    write_success = False
    # initial empty exception
    exception = None
    
    try:
        with open(file, "wb+") as f:
            # save image content
            f.write(content)
            # flag saving successful
            write_success = True
    except Exception as e:
        exception = e

    return write_success, exception

def download_images(images, output_dir, username, password):
    """
    download_images Downloads images to output directory.

    :param images: List of image html tags
    :param output_dir: Full path of the output image directory
    :param username: Username for basic auth
    :param password: Password for basic auth
    """ 
    # initial image downloads count
    count = 0
    # check if images count is not zero
    if len(images) == 0:
        print("No images found!")
    else:
        for image in images:
            # get image URL html tag
            image_url = get_image_url(image)
            # check if there is source URL for the image
            if image_url is None:
                print("No image source URL found!")
            else:
                # initial response, empty
                response, exception = make_request(image_url, username, password)
                # check response
                if exception is not None:
                    print(f"Response to URL: {image_url} failed! Image skipped. Error: {exception}")
                else:
                    # save final image URL (can be redirected)
                    final_image_url = response.url
                    # save the image content if it's URL ends with .png
                    if not final_image_url.lower().endswith('.png'):
                        print(f"Image with URL: {image_url} was NOT downloaded! Only .png extention is allowed!")
                    else:
                        # extract image content from request response
                        image_content = response.content
                        # open new file in the output_dir as image-{count}.png
                        write_success, exception = write_content_to_file(image_content, f"{output_dir}/image-{count}.png")
                        if not write_success:
                            print(f"Image saving failed! Error: {exception}")
                        else:
                            # print image download success
                            print(f"Image with URL: {image_url} was downloaded as {output_dir}/image-{count}.png")
                            # increment image count
                            count += 1
                        
        print(f"Total {count} Images Downloaded Out of {len(images)} found!")


# MAIN FUNCTION START
def main():
    # parse command-line arguments
    args = parse_arguments()

    # create output directory
    create_output_dir(args.output_dir)

    # initial response, empty
    response, exception = make_request(args.url, args.username, args.password)

    # check if request is successful
    if exception is not None:
        print(f"Response to URL: {args.url} failed! Error: {exception}")
    else:
        # parse html code
        soup = BeautifulSoup(response.text, 'html.parser')

        # find all images in URL
        images = soup.findAll('img')

        # download all images to output_dir
        download_images(images, args.output_dir, args.username, args.password)


# CALL MAIN FUNCTION
if __name__ == '__main__':
    main()
