from routeros_api import RouterOsApiPool

def connect_to_router(router_ip, username, password):
    """
    Connect to the MikroTik router using RouterOS API.
    """
    try:
        api_pool = RouterOsApiPool(router_ip, username=username, password=password, plaintext_login=True)
        return api_pool
    except Exception as e:
        raise ConnectionError(f"Failed to connect to MikroTik router: {e}")
    
def create_hotspot_users(api, user_name, user_password, profile_name, timess="1d", hotsp="hotspot1"):
    """
    Create a Hotspot user in MikroTik.
    """
    try:
        user_data = {
            "name": user_name,
            "password": user_password,
            "profile": profile_name,
            "limit-uptime": timess,
            "server": hotsp,
        }
        api.get_resource('/ip/hotspot/user').add(**user_data)
        print(f"Hotspot User '{user_name}' created successfully.")
    except Exception as e:
        raise RuntimeError(f"Failed to create Hotspot user: {e}")

def delete_hotspot_user(api, username):
    """
    Delete a Hotspot user from MikroTik using get_resource.
    """
    try:
        hotspot_user_resource = api.get_resource('/ip/hotspot/user')
        hotspot_user_resource.remove(id=username)
        print(f"User '{username}' deleted successfully.")
    except Exception as e:
        raise RuntimeError(f"Failed to delete Hotspot user '{username}': {e}")

    
def create_user_profile(api, profile_name, rate_limit="1M/1M", shared_users="1"):
    """
    Create a user profile in MikroTik Hotspot.
    """
    try:
        profile_data = {
            "name": profile_name,
            "rate-limit": rate_limit,
            "shared-users": shared_users
        }
        api.get_resource('/ip/hotspot/user/profile').add(**profile_data)
        print(f"User Profile '{profile_name}' created successfully.")
    except Exception as e:
        raise RuntimeError(f"Failed to create user profile: {e}")
    
def delete_hotspot_profile(api, id):
    """
    Delete a Hotspot user from MikroTik using get_resource.
    """
    try:
        hotspot_user_resource = api.get_resource('/ip/hotspot/user/profile')
        hotspot_user_resource.remove(id=id)
        print(f"User '{id}' deleted successfully.")
    except Exception as e:
        raise RuntimeError(f"Failed to delete Hotspot user '{id}': {e}")
    
def get_all_hotspot_users(api):
    """
    Retrieve all Hotspot users from MikroTik.
    """
    try:
        users = api.get_resource('/ip/hotspot/user').get()
        return users
    except Exception as e:
        raise RuntimeError(f"Failed to fetch Hotspot users: {e}")

def get_all_user_profiles(api):
    """
    Retrieve all user profiles from MikroTik.
    """
    try:
        profiles = api.get_resource('/ip/hotspot/user/profile').get()
        return profiles
    except Exception as e:
        raise RuntimeError(f"Failed to fetch Hotspot user profiles: {e}")
    
def get_print_user(api, selected_users):
    try:
        resource = api.get_resource('/ip/hotspot/user')  # Contoh untuk Hotspot User
        users_data = []
        for user_id in selected_users:
            user_info = resource.get(id=user_id)
            if user_info:
                users_data.append(user_info)
        return users_data
    except Exception as e:
        raise Exception(f"Error saat mengambil data user: {str(e)}")