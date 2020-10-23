from app.security import requires_auth


@requires_auth
def get_item():

    return "Long dep trai"
