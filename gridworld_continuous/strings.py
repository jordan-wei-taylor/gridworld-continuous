four_rooms = """
#############
#     #     #
#     #     #
#           #
#     #     #
#     #     #
## ####     #
#     ### ###
#     #     #
#     #     #
#           #
#     #     #
#############
"""

four_rooms_symmetrical = """
#############
#     #     #
#     #     #
#           #
#     #     #
#     #     #
### ##### ###
#     #     #
#     #     #
#           #
#     #     #
#     #     #
#############
"""

four_rooms_corridor = """
#############
#           #
# ######### #
# #   #   # #
#     #     #
# #   #   # #
# ######### #
# #   #   # #
#     #     #
# #   #   # #
# ######### #
#           #
#############
"""


def four_rooms_string(variant):
    name  = 'four_rooms'
    valid = {}
    for key, value in globals().copy().items():
        if name in key and isinstance(value, str):
            key = key[len(name) + 1:]
            if len(key) == 0:
                key = None
            valid[key] = value
    
    if variant in valid:
        return valid[variant]
    
    raise Exception(f'"{variant}" not recognised!\n\nExpected one of {"{" + str(list(valid))[1:-1] + "}"}')
