from docx import Document
from difflib import SequenceMatcher
import os
import json
import hashlib
from pathlib import Path
import argparse
from cache_handler import CacheHandler

class WordFileComparator:
    # Removed: Entire File class definition
    
    class UnionFind:
        def __init__(self, n):
            self.parent = list(range(n))
            self.rank = [1] * n
        
        def find(self, p):
            if self.parent[p] != p:
                self.parent[p] = self.find(self.parent[p])
            return self.parent[p]
        
        def union(self, p, q):
            rootP = self.find(p)
            rootQ = self.find(q)
            if rootP != rootQ:
                if self.rank[rootP] > self.rank[rootQ]:
                    self.parent[rootQ] = rootP
                elif self.rank[rootP] < self.rank[rootQ]:
                    self.parent[rootP] = rootQ
                else:
                    self.parent[rootQ] = rootP
                    self.rank[rootP] += 1

    def __init__(self):
        pass

    def find_similar(self, directory, similarity_threshold=0.7):
        # Replace File class with dict
        docx_files = [{
            'path': os.path.join(directory, f),
            'hash': CacheHandler._get_file_hash(os.path.join(directory, f))
        } for f in os.listdir(directory) if f.endswith('.docx')]
        
        uf = self.UnionFind(len(docx_files))
        
        for i in range(len(docx_files)):
            for j in range(i+1, len(docx_files)):
                if uf.find(i) != uf.find(j) \
                and self._compare_documents(docx_files[i], docx_files[j], similarity_threshold):
                    uf.union(i, j)
        
        groups = {}
        for idx, file in enumerate(docx_files):
            root = uf.find(idx)
            groups.setdefault(root, []).append(file)
        
        return list(groups.values())
    
    def find_similar_with_cache(self, directory, cache_path, similarity_threshold=0.7):
        unchanged, changed, cache = CacheHandler.validate_and_compare_cache(directory, cache_path)

        print("Unchanged:", unchanged)
        print("Changed:", changed)
        print("Cache:", cache)

        docx_files = unchanged + changed
        uf = self.UnionFind(len(docx_files))
        #create a dictionary to store the index of each file
        file_index = {file['path']: idx for idx, file in enumerate(docx_files)}
        #create the union find according to the cache
        for group in cache:
            for i in range(len(group)-1):
                uf.union(file_index[group[i]['path']], file_index[group[i+1]['path']])
        #compare the changed files with the unchanged files
        for file in changed:
            for i in range(len(docx_files)):
                if uf.find(i)!= uf.find(file_index[file['path']]):
                    if self._compare_documents(file, docx_files[i], similarity_threshold):
                        uf.union(i, file_index[file['path']]) 

        groups = {}
        for idx, file in enumerate(docx_files):
            root = uf.find(idx)
            groups.setdefault(root, []).append(file)

        return list(groups.values())       

    def _get_text_from_docx(self, file_path):
        doc = Document(file_path)
        return '\n'.join([para.text for para in doc.paragraphs])

    def _compare_documents(self, file1, file2, similarity_threshold):
        # Update to use dict access
        if file1['hash'] == file2['hash']:
            return True
        text1 = self._get_text_from_docx(file1['path'])
        text2 = self._get_text_from_docx(file2['path'])
        return SequenceMatcher(None, text1, text2).ratio() >= similarity_threshold

    # Remove these methods:
    # @staticmethod
    # def write_cache...
    # @staticmethod
    # def read_cache...

# Updated main section
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Compare Word documents for similarity')
    parser.add_argument('--dir', required=True, help='Directory containing Word files')
    parser.add_argument('--cache', required=True, help='Path to cache file')
    parser.add_argument('--use-cache', required=False, action='store_true', help='Use previous cache')
    parser.add_argument('--similarity', type=float, default=0.7, help='Similarity threshold (0.0 to 1.0)')
    
    args = parser.parse_args()
    
    comparator = WordFileComparator()
    similar_files = []
    if args.use_cache:
        similar_files = comparator.find_similar_with_cache(args.dir, args.cache, args.similarity) 
    else:
        similar_files = comparator.find_similar(args.dir, args.similarity)
    
    for group in similar_files:
        print(f"Similar files group: {', '.join(str(f['path']) for f in group)}")
    
    # Use CacheHandler instead of static method
    CacheHandler.write_cache(similar_files, args.cache)
    print(f"Comparison results cached at {args.cache}")