"""
Custom errors for the Restful API
is defined here.
"""

custom_errors = {
    'BucketListNameExistsError': {
        'message': "A Bucketlist with the name already exists",
        'status': 406,
    },
    'BucketListNameIsEmpty': {
        'message': "The BucketList name cannot be empty",
        'status': 406,
    }
}
