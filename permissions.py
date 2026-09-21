import json

PERMISSION_FILE = "permissions.json"


def load_permissions():

    try:

        with open(PERMISSION_FILE, "r") as file:
            return json.load(file)

    except FileNotFoundError:

        return {}


def has_permission(permission):

    permissions = load_permissions()

    return permissions.get(permission, False)


def set_permission(permission, value):

    permissions = load_permissions()

    permissions[permission] = value

    with open(PERMISSION_FILE, "w") as file:

        json.dump(
            permissions,
            file,
            indent=4
        )


def show_permissions():

    permissions = load_permissions()

    result = "🔒 Permissions\n\n"

    for permission, value in permissions.items():

        if value:
            status = "✅ Allowed"
        else:
            status = "❌ Blocked"

        result += f"{permission} : {status}\n"

    return result