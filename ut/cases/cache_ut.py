import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from cache_handler import CacheHandler

unchanged, changed_or_new = CacheHandler.validate_and_compare("test_files", "test_cache.json")
print("Unchanged:", unchanged)
print("Changed/New:", changed_or_new)
