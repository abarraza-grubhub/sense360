import pandas as pd
from typing import List, Dict
from collections import namedtuple
from tag_definitions import Tag
from transcript_loader import TranscriptSection
from tqdm import tqdm  # Import tqdm for progress bars


QuoteTagExample = namedtuple('QuoteTagExample', ['quote', 'tag'])



QUOTE_TAGGING_PROMPT = """

Context:
You are a User Experience Research tagging assistant, helping Grubhub identify valuable insights from user quotes during interviews.

Instructions:

You will be given an input text formatted as follows:
<input_text>
{quote_text}
</input_text>

Your task is to identify relevant quotes and tag them accordingly. Provide your output in JSON format using the structure below:
[
    {{
        'quote': 'The specific text to be tagged',
        'tag': 'The assigned tag for the quote',
        'confidence': 'Score between 0 and 1 representing your confidence in the assigned tag'
    }}
]
If no quotes need to be tagged, return an empty JSON array [] instead.
The JSON can include several quotes to be tagged.

You can only use the following tags (tags are separated with the placeholder '<tag_separator>'):
<tags>
{eligible_tags}
<tags>


Below are instructions on when certain tags should be applied. You can use these instructions in addition to examples to decide the appropriate tag:

<tag_instructions>
{tag_instructions}
<tag_instructions>


A few examples of quotes that have been manually tagged by experts:

<examples>
{few_shot_examples}
</examples>

The <input_text> may contain multiple quotes, and not all of it must be tagged. Focus on tagging parts that provide valuable insights for supporting user study analysis.


In the output, I want the under the 'quote' to include the biggest chunks of consecutive text that belong to the same tag.

This is an example of an incorrect output:

[{{
    'quote': "He's, you know, old school. So I usually like, I've been doing like the grocery shopping for him because it's hard for him to get out and drive and go to the grocery store himself.",
    'tag': 'grocery',
    'confidence': 1.0
}},

{{
    'quote': "So I've been like doing the grocery shopping for him. And then I usually do like the Instacart. And so I'll let him know when it's coming to his house and then he just leave it by the door and then he'll, he'll let me know. You know, he know. He lets me know what he wants.",
    'tag': 'grocery',
    'confidence': 1.0
}}
]

For the input: 
<input_text>
He's, you know, old school. So I usually like, I've been doing like the grocery shopping for him because it's hard for him to get out and drive and go to the grocery store himself. So I've been like doing the grocery shopping for him. And then I usually do like the Instacart. And so I'll let him know when it's coming to his house and then he just leave it by the door and then he'll, he'll let me know. You know, he know. He lets me know what he wants.
</input_text>

The expected output would look more like this:

[{{
    'quote': "He's, you know, old school. So I usually like, I've been doing like the grocery shopping for him because it's hard for him to get out and drive and go to the grocery store himself. So I've been like doing the grocery shopping for him. And then I usually do like the Instacart. And so I'll let him know when it's coming to his house and then he just leave it by the door and then he'll, he'll let me know. You know, he know. He lets me know what he wants.",
    'tag': 'grocery',
    'confidence': 1.0
}}
]



Your turn.
Only return the JSON output for the tag.


<input_text>
{quote_text}
</input_text>
                
"""


class TranscriptTagger:
    def __init__(self, tags: List[Tag], llm_instance, quote_tag_map, quote_vector_store, tag_vector_store, threshold: float = 0.7, k: int = 5):
        """
        Initialize the TranscriptTagger class.

        Parameters:
        - tags (List[Tag]): List of available tags with definitions.
        - llm_instance: Instance of the language model (e.g., ChatBedrock).
        - quote_vector_store: Pre-trained FAISS vector store with example quotes and their tags.
        - tag_vector_store: Pre-trained FAISS vector store with tag information.
        - threshold (float): Minimum confidence required to assign a tag.
        """
        self.tags = tags
        self.llm_instance = llm_instance
        self.quote_tag_map = quote_tag_map
        self.quote_vector_store = quote_vector_store
        self.tag_vector_store = tag_vector_store
        self.threshold = threshold
        self.k = k
        
        
        # TODO: check this .lower() here if necessary in the future
        # tag_quote_map
        tag_quote_map = {}
        for quote, tag in self.quote_tag_map.items():
            if tag.lower() not in tag_quote_map:
                tag_quote_map[tag.lower()] = []  # Initialize an empty list for new tags
            tag_quote_map[tag.lower()].append(quote)  # Add the quote to the appropriate tag
        self.tag_quote_map = tag_quote_map

    def tag_instructions(self):
        tag_instructions = []
        for tag in self.tags:
            if tag.instructions:
                tag_instructions.append(f"<new_instruction>\nTag: {tag.tag}\nInstructions of when to use: {tag.instructions}\n</new_instruction>")

        tag_instructions = "\n\n".join(tag_instructions)
        
        if not tag_instructions:
            tag_instructions = "No instructions were provided to label tags."
        
        return tag_instructions
    
    def construct_prompt(self, quote: str, examples: List[QuoteTagExample]) -> str:
        
        if examples:
            few_shot_examples = ", ".join([self.format_example(example) for example in examples])
            few_shot_examples = "["+ few_shot_examples + "]"
        else:
            few_shot_examples = "We do not have relevant examples."
        
        eligible_tags = "<tag_separator>".join(list(self.tag_quote_map.keys()))
        
        if not eligible_tags:
            eligible_tags = "no_tags_are_available"
        
        try:
            prompt = QUOTE_TAGGING_PROMPT.format(quote_text=quote if quote else "",
                                                 eligible_tags=eligible_tags,
                                                 tag_instructions=self.tag_instructions(),
                                                 few_shot_examples=few_shot_examples
                                                )
        except Exception as e:
            print(few_shot_examples)
            raise e

        return prompt

    def process_llm_response(self, response) -> pd.DataFrame:
        """
        Processes the response from the language model to extract quotes, tags, and confidence.

        Parameters:
        - response (str): JSON string response from the language model.

        Returns:
        - pd.DataFrame: DataFrame containing Quote, Tag, and Confidence columns.
        """
        
        # Ensure response is always a valid JSON, either a list of tags or an empty list.
        if not response or response == "[]":
            return pd.DataFrame(columns=['quote', 'tag', 'confidence'])
        
        try:
            responses = pd.read_json(response)
            return responses
        except ValueError:
            # If the response is not a valid JSON, return an empty DataFrame
            return pd.DataFrame(columns=['quote', 'tag', 'confidence'])

    
    def query_language_model(self, prompt: str) -> pd.DataFrame:
        return self.llm_instance.invoke(prompt).content.strip()
    
    
    def format_example(self, example: QuoteTagExample):
        return f"""{{"quote": "{example.quote}", "tag":"{example.tag}", "confidence": 1.0}}"""

    
    def few_shot_examples_from_quote(self, quote) -> List[QuoteTagExample]:
        retrieved_quotes = self.quote_vector_store.similarity_search(quote, self.k)
        
        few_shot_examples = [QuoteTagExample(quote = quote.page_content, 
                                             tag = self.quote_tag_map.get(quote.page_content))
                             for quote in retrieved_quotes
                            ]
        return few_shot_examples
    
    def few_shot_examples_from_tags(self, tags) -> List[QuoteTagExample]:
        
        related_tags = set()
        
        for tag in tags:
            for related_tag in self.tag_vector_store.similarity_search(tag, self.k):
                related_tags.add(related_tag.page_content.lower())

        
        # Get quotes associated to the related tags
        
        few_shot_examples = []
        for tag in related_tags:
            quotes = self.tag_quote_map.get(tag)[:3] # Limit to 5 examples per extra tag
            if quotes:
                for quote in quotes:
                    example = QuoteTagExample(quote = quote,
                                              tag = tag)
                    few_shot_examples.append(example)
            
        return few_shot_examples
        
    
    def few_shot_examples(self, quote: str) -> List[QuoteTagExample]:
        """
        Get examples
        """
        
        examples = self.few_shot_examples_from_quote(quote)
        related_tag_examples = self.few_shot_examples_from_tags([example.tag for example in examples])

        examples.extend(related_tag_examples)
        
        return examples[:20]
    
    
    def tag_section(self, section: TranscriptSection) -> pd.DataFrame:
        """
        Tags sentences from a single interview response.

        Parameters:
        - section (TranscriptSection): A transcript section containing a question and answer.

        Returns:
        - DataFrame: DataFrame containing Quote, Tag, Confidence, and Tag Group columns.
        """
        q, a = section.q, section.a
        
        examples = self.few_shot_examples(a)
        
        # Construct prompt and query language model
        prompt = self.construct_prompt(a, examples)
        response = self.query_language_model(prompt)

        # Process the response from the model to generate tags
        df = self.process_llm_response(response)

        # Append Tag Group for each tag based on available tag definitions
        df['Tag Group'] = df['tag'].apply(lambda x: next((tag.tag_group for tag in self.tags if tag.tag == x), ''))

        # Rename columns for clarity
        df.rename(columns={'quote': 'Quote', 'tag': 'Tag', 'confidence': 'Confidence'}, inplace=True)
        
        return df
        

    def tag_transcript(self, transcript: List[TranscriptSection]) -> pd.DataFrame:
        """
        Tags sentences from a single transcript containing multiple sections.

        Parameters:
        - sections (List[TranscriptSection]): List of TranscriptSection for a single participant.

        Returns:
        - DataFrame: DataFrame containing Quote, Tag, Confidence, and Tag Group columns.
        """
        all_results = []
        for section in tqdm(transcript, desc="Tagging sections in transcript"):
            df = self.tag_section(section)
            if not df.empty:
                all_results.append(df)

        # Concatenate all results into a single DataFrame
        final_df = pd.concat(all_results, ignore_index=True) if all_results else pd.DataFrame()
        final_df = final_df if not final_df.empty else pd.DataFrame(columns=['Quote', 'Tag', 'Confidence', 'Tag Group'])
        
        final_df =  self.add_tag_group(final_df)
        
        return final_df

    def tag_transcripts(self, transcripts: Dict[str, List[TranscriptSection]]) -> pd.DataFrame:
        """
        Tags sentences from multiple interview responses in different transcripts.

        Parameters:
        - transcripts (Dict[str, List[TranscriptSection]]): Dictionary where keys are Participant names and values are lists of TranscriptSection.

        Returns:
        - DataFrame: Pandas DataFrame containing Quote, Participant, Tag Group, and Tag columns.
        """
        all_results = []
        for participant, transcript in tqdm(transcripts.items(), desc="Tagging transcripts for each participant"):
            df = self.tag_transcript(transcript)
            if not df.empty:
                df['Participant'] = participant
                all_results.append(df)

        # Concatenate all results into a single DataFrame
        final_df = pd.concat(all_results, ignore_index=True) if all_results else pd.DataFrame()
        final_df = final_df if not final_df.empty else pd.DataFrame(columns=['Quote', 'Tag', 'Confidence', 'Tag Group', 'Participant'])
        final_df =  self.add_tag_group(final_df)
        
        return final_df

    def add_tag_group(self, df):
        # Create a dictionary to map tag to tag_group for quick lookup
        tag_to_group = {tag.tag.lower(): tag.tag_group for tag in self.tags}

        # Use apply to fill in the Tag Group based on the tag_to_group dictionary
        df['Tag Group'] = df['Tag'].apply(lambda x: tag_to_group.get(x.lower(), 'No Tag Group'))
        
        return df
