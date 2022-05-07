def get_max_role_length(roles):
    max_role_length = max(len(role[0]) for role in roles)
    return max_role_length
