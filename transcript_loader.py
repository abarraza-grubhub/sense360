import os
import re
from docx import Document

from typing import NamedTuple


class TranscriptSection(NamedTuple):
    q: str
    a: str

def is_participant(text):
    # Check if the text matches the participant pattern (P followed by a digit)
    return bool(re.match(r'^P\d+', text))

def process_transcript(file_path):
    doc = Document(file_path)
    qna_list = []
    current_q = None
    skip_first = True
    
    for para in doc.paragraphs:
        text = para.text.strip()
        
        if skip_first:
            skip_first = False
            continue
        
        if text.startswith("Bookmark:") or not text:
            # Ignore bookmark lines and empty lines
            continue
        
        if is_participant(text):
            # This is a participant answer
            answer = text.split(']', 1)[-1].strip() if ']' in text else text
            if current_q is not None:
                section = TranscriptSection(q=current_q, a=answer)
                qna_list.append(section)
                # qna_list.append({'q': current_q, 'a': answer})
                current_q = None
            else:
                section = TranscriptSection(q='', a=answer)
                qna_list.append(section)
                # qna_list.append({'q': '', 'a': answer})
        else:
            # This is a non-participant question
            question = text.split(']', 1)[-1].strip() if ']' in text else text
            current_q = question
    
    return qna_list

def load_transcripts(folder_path):
    transcripts_dict = {}
    
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.docx'):
            file_path = os.path.join(folder_path, file_name)
            qna_list = process_transcript(file_path)
            transcripts_dict[os.path.splitext(file_name)[0]] = qna_list
    
    return transcripts_dict
