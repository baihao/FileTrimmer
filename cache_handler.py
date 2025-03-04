import json
import os
import hashlib
from pathlib import Path

class CacheHandler:
    @staticmethod
    def _get_file_hash(file_path):
        """Generate SHA256 hash of a file"""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    @staticmethod
    def write_cache(similar_groups, cache_path):
        """Serialize similar files groups to JSON cache"""
        cache_dir = Path(cache_path).parent
        cache_dir.mkdir(parents=True, exist_ok=True)
        
        serialized = [
            [{"path": f['path'], "hash": f['hash']} for f in group]
            for group in similar_groups
        ]
        
        with open(cache_path, 'w') as f:
            json.dump(serialized, f, indent=2)

    @staticmethod
    def read_cache(cache_path):
        """Deserialize cache file to similar files groups"""
        if not Path(cache_path).exists():
            return []
            
        with open(cache_path, 'r') as f:
            return json.load(f)

    @staticmethod
    def validate_and_compare_cache(directory, cache_path):
        """Update cache and return tuple of (unchanged_files, changed_or_new_files)"""
        # Get current files and their hashes
        current_files = {}
        for f in os.listdir(directory):
            if f.endswith('.docx'):
                path = os.path.join(directory, f)
                current_files[path] = CacheHandler._get_file_hash(path)

        # Read existing cache
        cached_groups = CacheHandler.read_cache(cache_path)
        cached_files = {}
        for group in cached_groups:
            for file in group:
                cached_files[file['path']] = file['hash']

        # Compare with current state
        unchanged = []
        changed_or_new = []
        for path, current_hash in current_files.items():
            if path in cached_files:
                if cached_files[path] == current_hash:
                    unchanged.append({"path": path, "hash": current_hash})
                else:
                    changed_or_new.append({"path": path, "hash": current_hash})
            else:
                changed_or_new.append({"path": path, "hash": current_hash})

        # Remove deleted files from cache
        updated_cache = [
            [file for file in group if os.path.exists(file['path']) 
             and CacheHandler._get_file_hash(file['path']) == file['hash']]
            for group in cached_groups
        ]
        updated_cache = [group for group in updated_cache if group]
        
        return unchanged, changed_or_new, updated_cache

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Cache Handler Test Utility')
    parser.add_argument('--dir', required=True, help='Directory to monitor')
    parser.add_argument('--cache', required=True, help='Path to cache file')
    parser.add_argument('--updated-cache', required=True, help='Path to updated cache file')
    
    args = parser.parse_args()
    
    unchanged, changed_or_new, updated_cache = CacheHandler.validate_and_compare_cache(
        args.dir, args.cache
    )
    
    # Write cleaned cache
    CacheHandler.write_cache(updated_cache, args.updated_cache)
    
    # Print results
    print(f"\nUnchanged files ({len(unchanged)}):")
    for f in unchanged[:3]:
        print(f" - {f['path']}")
    if len(unchanged) > 3:
        print(f" ... and {len(unchanged)-3} more")
        
    print(f"\nChanged/New files ({len(changed_or_new)}):")
    for f in changed_or_new[:3]:
        print(f" - {f['path']}")
    if len(changed_or_new) > 3:
        print(f" ... and {len(changed_or_new)-3} more")
        
    print(f"\nUpdated cache contains {len(updated_cache)} valid file groups")