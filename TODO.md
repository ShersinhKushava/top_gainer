# TODO: Fix Errors in views.py

- [x] Add safe type conversions for float and int in data processing loop
- [x] Add checks for API response structure before accessing nested keys
- [x] Replace broad Exception with specific exceptions (requests.RequestException, KeyError, ValueError, pymongo.errors.ConnectionFailure)
- [x] Add try-except around MongoDB operations to handle connection issues
