import boto3

"""
Refactor the next function using yield to return the array of objects found by the
`s3.list_objects_v2` function that matches the given prefix.
"""


def get_s3_objects(bucket, prefix=""):
    s3 = boto3.client("s3")

    kwargs = {"Bucket": bucket, "Prefix": prefix}

    while True:
        resp = s3.list_objects_v2(**kwargs)
        for obj in resp.get("Contents", []):
            yield obj

        if "NextContinuationToken" in resp:
            kwargs["ContinuationToken"] = resp["NextContinuationToken"]
        else:
            break


"""
Please, full explain this function: document iterations, conditionals, and the
function as a whole
"""


def fn(main_plan, obj, extensions=[]):
    """
    Processes a main plan and a list of items, taking into account additional extensions. The returned object is
    probably used to update the quantities or remove items from a main list.

    Parameters
    ----------
    main_plan : object
        The main plan object containing an id attribute.
    obj : dict
        A dictionary containing items data. Each item is expected to have an id and price attribute.
    extensions : list, optional
        A list of dictionaries where each dictionary has 'price' (object with an id attribute)
        and 'qty' (integer quantity) keys. Default is an empty list.

    Returns
    -------
    list
        A list of dictionaries representing the processed items. Each dictionary contains at least an 'id' key.
        Additional keys may include 'qty' for quantity or 'deleted' to indicate removal.
    """

    items = []  # List to store the processed items.
    sp = False  # Flag to indicate if the main plan is present in the items.
    cd = False  # Flag to indicate if any item has been marked as deleted. (NOT USED)

    ext_p = {}  # Dictionary to store extension prices' by id and their quantities.

    # Populate the ext_p dictionary with price id and quantity from extensions.
    for ext in extensions:
        ext_p[ext["price"].id] = ext["qty"]

    # Iterate through each item in obj["items"].data.
    for item in obj["items"].data:
        product = {"id": item.id}  # Create a product dictionary with the item's ID.

        # Check if the item's price ID is neither the main plan ID nor in extensions.
        if item.price.id != main_plan.id and item.price.id not in ext_p:
            product["deleted"] = True  # Mark the product as deleted.
            cd = True  # Set the condition deleted flag to True.
        # Check if the item's price ID is in the extensions.
        elif item.price.id in ext_p:
            qty = ext_p[item.price.id]  # Get the quantity from extensions.
            if qty < 1:
                product["deleted"] = (
                    True  # Mark the product as deleted if quantity is less than 1.
                )
            else:
                product["qty"] = qty  # Set the product's quantity.
            del ext_p[item.price.id]  # Remove the processed extension.
        # Check if the item's price ID is the main plan ID.
        elif item.price.id == main_plan.id:
            sp = True  # Set the plan flag to True.

        items.append(product)  # Add the processed product to the items list.

    # If the main plan is not present, add it with a quantity of 1.
    if not sp:
        items.append({"id": main_plan.id, "qty": 1})

    # Add any remaining valid extensions to the items list.
    for price, qty in ext_p.items():
        if qty < 1:
            continue  # Skip if the quantity is less than 1.
        items.append({"id": price, "qty": qty})  # Add the extension with its quantity.

    return items


"""
Having the class `Caller` and the function `fn`
Refactor the function `fn` to execute any method from `Caller` using the argument `fn_to_call`
reducing the `fn` function to only one line.
"""


class Caller:
    add = lambda a, b: a + b
    concat = lambda a, b: f"{a},{b}"
    divide = lambda a, b: a / b
    multiply = lambda a, b: a * b


def fn_caller(fn_to_call, *args):
    result = None

    if fn_to_call == "add":
        result = Caller.add(*args)
    if fn_to_call == "concat":
        result = Caller.concat(*args)
    if fn_to_call == "divide":
        result = Caller.divide(*args)
    if fn_to_call == "multiply":
        result = Caller.multiply(*args)

    return result


"""
A video transcoder was implemented with different presets to process different videos in the application. The videos should be
encoded with a given configuration done by this function. Can you explain what this function is detecting from the params
and returning based in its conditionals?
"""


def fn(config, w, h):
    v = None
    ar = w / h

    if ar < 1:
        v = [r for r in config["p"] if r["width"] <= w]
    elif ar > 4 / 3:
        v = [r for r in config["l"] if r["width"] <= w]
    else:
        v = [r for r in config["s"] if r["width"] <= w]

    return v


"""
Having the next helper, please implement a refactor to perform the API call using one method instead of rewriting the code
in the other methods.
"""
import requests


class Helper:
    DOMAIN = "http://example.com"
    SEARCH_IMAGES_ENDPOINT = "search/images"
    GET_IMAGE_ENDPOINT = "image"
    DOWNLOAD_IMAGE_ENDPOINT = "downloads/images"

    AUTHORIZATION_TOKEN = {
        "access_token": None,
        "token_type": None,
        "expires_in": 0,
        "refresh_token": None,
    }

    def search_images(self, **kwargs):
        token_type = self.AUTHORIZATION_TOKEN["token_type"]
        access_token = self.AUTHORIZATION_TOKEN["access_token"]

        headers = {
            "Authorization": f"{token_type} {access_token}",
        }

        URL = f"{self.DOMAIN}/{self.SEARCH_IMAGES_ENDPOINT}"

        send = {"headers": headers, "params": kwargs}

        response = request.get(requests, method)(URL, **send)
        return response

    def get_image(self, image_id, **kwargs):
        token_type = self.AUTHORIZATION_TOKEN["token_type"]
        access_token = self.AUTHORIZATION_TOKEN["access_token"]

        headers = {
            "Authorization": f"{token_type} {access_token}",
        }

        URL = f"{self.DOMAIN}/{self.GET_IMAGE_ENDPOINT}/{image_id}"

        send = {"headers": headers, "params": kwargs}

        response = request.get(requests, method)(URL, **send)
        return response

    def download_image(self, image_id, **kwargs):
        token_type = self.AUTHORIZATION_TOKEN["token_type"]
        access_token = self.AUTHORIZATION_TOKEN["access_token"]

        headers = {
            "Authorization": f"{token_type} {access_token}",
        }

        URL = f"{self.DOMAIN}/{self.DOWNLOAD_IMAGE_ENDPOINT}/{image_id}"

        send = {"headers": headers, "data": kwargs}

        response = request.post(requests, method)(URL, **send)
        return response
