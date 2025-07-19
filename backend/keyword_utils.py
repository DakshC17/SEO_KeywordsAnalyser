import re
from typing import List, Tuple
import random

def insert_keyword_intelligently(text: str, keyword: str) -> str:
    """
    Insert keyword intelligently into text without breaking sentence structure.
    """
    if not text or not keyword:
        return text
    
    # Check if keyword already exists (case insensitive)
    if keyword.lower() in text.lower():
        return text
    
    # Split text into sentences
    sentences = re.split(r'([.!?]+)', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    if not sentences:
        return f"{keyword}. {text}"
    
    # Find the best position to insert the keyword
    best_position = find_best_insertion_point(sentences, keyword)
    
    if best_position == -1:
        # If no good position found, append at the end
        return f"{text} {keyword}."
    
    # Insert keyword at the best position
    modified_sentences = insert_at_position(sentences, keyword, best_position)
    
    return ' '.join(modified_sentences)

def find_best_insertion_point(sentences: List[str], keyword: str) -> int:
    """Find the best sentence to insert the keyword."""
    
    # Strategy 1: Find sentences that are longer and could accommodate the keyword
    for i, sentence in enumerate(sentences):
        if not sentence.endswith(('.', '!', '?')):
            continue
            
        words = sentence.split()
        if len(words) > 5:  # Good length for insertion
            return i
    
    # Strategy 2: Find the middle sentence
    if len(sentences) > 2:
        return len(sentences) // 2
    
    # Strategy 3: Insert at the beginning
    return 0

def insert_at_position(sentences: List[str], keyword: str, position: int) -> List[str]:
    """Insert keyword at specified position in sentences."""
    if position >= len(sentences):
        sentences.append(f"{keyword}.")
        return sentences
    
    target_sentence = sentences[position]
    
    # If it's a punctuation mark, find the previous sentence
    if target_sentence in '.!?':
        if position > 0:
            target_sentence = sentences[position - 1]
            position = position - 1
        else:
            sentences.insert(0, f"{keyword}.")
            return sentences
    
    # Insert keyword naturally into the sentence
    modified_sentence = insert_keyword_in_sentence(target_sentence, keyword)
    sentences[position] = modified_sentence
    
    return sentences

def insert_keyword_in_sentence(sentence: str, keyword: str) -> str:
    """Insert keyword naturally within a sentence."""
    words = sentence.split()
    
    if len(words) < 3:
        return f"{sentence} {keyword}"
    
    # Insert positions (avoid very beginning and end)
    possible_positions = [
        len(words) // 3,      # Early in sentence
        len(words) // 2,      # Middle of sentence
        2 * len(words) // 3   # Later in sentence
    ]
    
    # Choose a random position for variety
    insert_pos = random.choice(possible_positions)
    
    # Insert with appropriate connectors
    connectors = ["", "and", "with", "including", "such as"]
    connector = random.choice(connectors)
    
    if connector:
        insertion = f"{connector} {keyword}"
    else:
        insertion = keyword
    
    # Insert at position
    words.insert(insert_pos, insertion)
    
    return ' '.join(words)

def calculate_keyword_density(text: str, keyword: str) -> float:
    """Calculate keyword density percentage."""
    if not text or not keyword:
        return 0.0
    
    text_lower = text.lower()
    keyword_lower = keyword.lower()
    
    keyword_count = text_lower.count(keyword_lower)
    total_words = len(text.split())
    
    if total_words == 0:
        return 0.0
    
    return (keyword_count / total_words) * 100

def get_keyword_positions(text: str, keyword: str) -> List[int]:
    """Get positions where keyword appears in text."""
    positions = []
    text_lower = text.lower()
    keyword_lower = keyword.lower()
    
    start = 0
    while True:
        pos = text_lower.find(keyword_lower, start)
        if pos == -1:
            break
        positions.append(pos)
        start = pos + 1
    
    return positions