#!/usr/bin/env python3

import sys
import shutil
from pathlib import Path
from collections import defaultdict


def check_file_duplicates(file_path):
    duplicates = []
    seen = {}
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        for line_num, line in enumerate(lines, 1):
            cleaned = line.strip().lower()
            
            if not cleaned:
                continue
            
            if cleaned in seen:
                duplicates.append({
                    'word': line.strip(),
                    'line_num': line_num,
                    'first_occurrence': seen[cleaned]
                })
            else:
                seen[cleaned] = line_num
    
    except FileNotFoundError:
        print(f"Warning: File not found: {file_path}")
        return [], {}
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return [], {}
    
    return duplicates, seen


def remove_duplicates_from_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        seen = set()
        unique_lines = []
        removed_count = 0
        
        for line in lines:
            cleaned = line.strip().lower()
            
            if not cleaned:
                unique_lines.append(line)
                continue
            
            if cleaned not in seen:
                seen.add(cleaned)
                unique_lines.append(line)
            else:
                removed_count += 1
        
        if removed_count > 0:
            backup_path = file_path.with_suffix(file_path.suffix + '.bak')
            shutil.copy2(file_path, backup_path)
            print(f"  Backup created: {backup_path.name}")
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(unique_lines)
            
            return removed_count
        
        return 0
    
    except Exception as e:
        print(f"Error removing duplicates from {file_path}: {e}")
        return 0


def check_cross_file_duplicates(file_data):
    word_locations = defaultdict(list)
    
    for file_path, words in file_data.items():
        for word, line_num in words.items():
            word_locations[word].append((file_path, line_num))
    
    cross_duplicates = {
        word: locations 
        for word, locations in word_locations.items() 
        if len(locations) > 1
    }
    
    return cross_duplicates


def remove_cross_file_duplicates(cross_duplicates, repo_root):
    if not cross_duplicates:
        return 0
    
    removed_count = 0
    files_to_update = defaultdict(set)
    
    for word, locations in cross_duplicates.items():
        all_txt_path = None
        specific_paths = []
        
        for file_path, line_num in locations:
            path_str = str(file_path)
            if path_str.endswith('all.txt'):
                all_txt_path = file_path
            else:
                specific_paths.append(file_path)
        
        if all_txt_path:
            for specific_path in specific_paths:
                files_to_update[specific_path].add(word.lower())
        elif len(specific_paths) > 1:
            for specific_path in specific_paths[1:]:
                files_to_update[specific_path].add(word.lower())
    
    for file_path, words_to_remove in files_to_update.items():
        full_path = repo_root / file_path
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            backup_path = full_path.with_suffix(full_path.suffix + '.bak')
            shutil.copy2(full_path, backup_path)
            
            filtered_lines = []
            for line in lines:
                cleaned = line.strip().lower()
                if cleaned and cleaned in words_to_remove:
                    removed_count += 1
                    continue
                filtered_lines.append(line)
            
            with open(full_path, 'w', encoding='utf-8') as f:
                f.writelines(filtered_lines)
            
            print(f"  Removed {len(words_to_remove)} duplicate(s) from {file_path}")
        
        except Exception as e:
            print(f"Error updating {file_path}: {e}")
    
    return removed_count


def main():
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    data_dir = repo_root / 'data'
    
    print("=" * 60)
    print("WORDLIST DUPLICATION CHECK")
    print("=" * 60)
    print()
    
    txt_files = list(data_dir.rglob('*.txt'))
    
    if not txt_files:
        print("No .txt files found in data directory.")
        return 0
    
    print(f"Checking {len(txt_files)} file(s) for duplicates...\n")
    
    total_removed = 0
    file_data = {}
    
    for file_path in txt_files:
        relative_path = file_path.relative_to(repo_root)
        print(f"Checking: {relative_path}")
        
        duplicates, seen_words = check_file_duplicates(file_path)
        
        if duplicates:
            print(f"  Found {len(duplicates)} duplicate(s) in file - removing...")
            removed = remove_duplicates_from_file(file_path)
            total_removed += removed
            
            _, seen_words = check_file_duplicates(file_path)
            print(f"  Successfully removed {removed} duplicate(s)")
        else:
            print(f"  No duplicates within file ({len(seen_words)} unique entries)")
        
        file_data[relative_path] = seen_words
        print()
    
    print("-" * 60)
    print("Checking for duplicates across files...\n")
    
    cross_duplicates = check_cross_file_duplicates(file_data)
    
    if cross_duplicates:
        print(f"Found {len(cross_duplicates)} word(s) duplicated across files")
        print("Removing cross-file duplicates...\n")
        
        cross_removed = remove_cross_file_duplicates(cross_duplicates, repo_root)
        total_removed += cross_removed
        
        print(f"Successfully removed {cross_removed} cross-file duplicate(s)")
    else:
        print("No cross-file duplicates found")
    
    print()
    
    print("=" * 60)
    if total_removed > 0:
        print(f"RESULT: REMOVED {total_removed} DUPLICATE(S)")
        print("=" * 60)
        print("\nBackup files (.bak) have been created.")
        print("Please review the changes before committing.")
        return 0
    else:
        print("RESULT: NO DUPLICATES FOUND")
        print("=" * 60)
        return 0


if __name__ == "__main__":
    sys.exit(main())
