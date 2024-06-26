import re
import math
import random

def contact(profile_entries, join_words = ", and "):
        
        return join_words.join(item for item in profile_entries)
    
def add_double_quote(text):
    return "\""+text+"\""

def reorder_list_middle(original_list):
    n = len(original_list)
    middle = n // 2

    reordered_list = []

    if n % 2 == 1:  
        for i in range(middle):
            reordered_list.append(original_list[-2-i*2])
        for i in range(middle+1):
            reordered_list.append(original_list[i*2])
    else:
        for i in range(middle):
            reordered_list.append(original_list[-1-i*2])
        for i in range(middle):
            reordered_list.append(original_list[i*2])

    return reordered_list

class LaMP1Prompt():
    def __init__(self) -> None:
        pass

    def aggregated_prompt(self, input, retrieved_profile, tokenizer, max_input_len=512, max_task_len=256, order='start', random_seed=42):
        
        # changing the order of the profiles
        if order == 'start':
            pass
        elif order == 'end':
            retrieved_profile.reverse()
        elif order == 'middle':
            retrieved_profile = reorder_list_middle(retrieved_profile)
        elif order == 'random':
            random.seed(random_seed)
            random.shuffle(retrieved_profile)

        max_profile_length = (max_input_len-max_task_len)/len(retrieved_profile)
        profile_prompt = contact(
            self.__per_profile_entity_prompt(
                retrieved_profile, 
                tokenizer, 
                max_profile_length)
        )
        
        #! I am not sure about the actual modification for the task input
        final_input_text = self.__merge_profile_and_input(input, profile_prompt)
        return final_input_text

    def __per_profile_entity_prompt(self, profile, tokenizer, max_profile_length):
        
        # change the order of the retrieved profiles

        profile_entities = []
        for item in profile:
            
            final_profle = add_double_quote(item['title'])
            original_profile_tokens = tokenizer.encode(final_profle)
            
            if len(original_profile_tokens) > max_profile_length:
                trim_length = math.ceil(len(original_profile_tokens)-max_profile_length)
                trim_text_tokens = tokenizer.encode(item['title'])[:-trim_length]
                trim_profile = tokenizer.decode(trim_text_tokens[:-1])
            else:
                trim_profile = item['title']


            trim_final_profile = add_double_quote(trim_profile)
            profile_entities.append(trim_final_profile)

        return profile_entities
    
    def __merge_profile_and_input(self, original_string, additional_string):
        """
        To add the additional string into the first quote part in the original string
        param: orginal_string (str): the orginal sentence with some quoted part
        param: additional_string (str): the additional part will be added into the orginal part
        return: modified_string (str): the modified sentence
        """
        pattern = r'title "([^"]*)"'

        def replace(match):
            # This function is called for each match, and it replaces the match with the modified content
            quoted_text = match.group(1)  # Extract the text inside the quotes
            modified_text = f'"{quoted_text}" {additional_string}'  # Add the additional string
            return f'title {modified_text}'  # Reconstruct the entire quoted string

        # Use re.sub() to replace the quoted part with the modified content
        modified_string = re.sub(pattern, replace, original_string)

        return modified_string
    

class LaMP2Prompt():
    def __init__(self) -> None:
        pass

    def aggregated_prompt(self, input, retrieved_profile, tokenizer, max_input_len=512, max_task_len=256, order='start', random_seed=42):
        
        if len(retrieved_profile) == 0:
            return input
        
        # changing the order of the profiles
        if order == 'start':
            pass
        elif order == 'end':
            retrieved_profile.reverse()
        elif order == 'middle':
            retrieved_profile = reorder_list_middle(retrieved_profile)
        elif order == 'random':
            random.seed(random_seed)
            random.shuffle(retrieved_profile)
        
        max_profile_length = (max_input_len-max_task_len)/len(retrieved_profile)
        profile_prompt = contact(
            self.__per_profile_entity_prompt(
                retrieved_profile, 
                tokenizer, 
                max_profile_length)
        )

        final_input_text = self.__merge_profile_and_input(input, profile_prompt)
        return final_input_text

    def __per_profile_entity_prompt(self, profile, tokenizer, max_profile_length):
        
        profile_entities = []
        for item in profile:
            
            final_profile = 'the tag for the movie:' + add_double_quote(item['description']) + ' is ' + add_double_quote(item['tag'])
            original_profile_tokens = tokenizer.encode(final_profile)
            if len(original_profile_tokens) > max_profile_length:
                trim_length = math.ceil(len(original_profile_tokens)-max_profile_length)
                trim_text_tokens = tokenizer.encode(item['description'])[:-trim_length]
                trim_profile = tokenizer.decode(trim_text_tokens[:-1])
            else:
                trim_profile = item['description']
            
            trim_final_profile = 'the tag for the movie:' + add_double_quote(trim_profile) + ' is ' + add_double_quote(item['tag'])
            #trim_profile_text = tokenizer.decode(trim_profile_tokens[:-1])
            profile_entities.append(trim_final_profile)
        
        return profile_entities

    def __merge_profile_and_input(self, original_string, additional_string):

        return additional_string + '. ' + original_string
    
class LaMP2Prompt_old():
    def __init__(self) -> None:
        pass

    def aggregated_prompt(self, input, retrieved_profile, tokenizer, max_input_len=512, max_task_len=256, order='start', random_seed=42):
        
        if len(retrieved_profile) == 0:
            return input
        
        # changing the order of the profiles
        if order == 'start':
            pass
        elif order == 'end':
            retrieved_profile.reverse()
        elif order == 'middle':
            retrieved_profile = reorder_list_middle(retrieved_profile)
        elif order == 'random':
            random.seed(random_seed)
            random.shuffle(retrieved_profile)
        
        max_profile_length = (max_input_len-max_task_len)/len(retrieved_profile)
        profile_prompt = contact(
            self.__per_profile_entity_prompt(
                retrieved_profile, 
                tokenizer, 
                max_profile_length)
        )

        final_input_text = self.__merge_profile_and_input(input, profile_prompt)
        return final_input_text

    def __per_profile_entity_prompt(self, profile, tokenizer, max_profile_length):
        
        profile_entities = []
        for item in profile:
            
            final_profile = 'the category for the article:' + add_double_quote(item['text']) + ' is ' + add_double_quote(item['category'])
            original_profile_tokens = tokenizer.encode(final_profile)
            if len(original_profile_tokens) > max_profile_length:
                trim_length = math.ceil(len(original_profile_tokens)-max_profile_length)
                trim_text_tokens = tokenizer.encode(item['text'])[:-trim_length]
                trim_profile = tokenizer.decode(trim_text_tokens[:-1])
            else:
                trim_profile = item['text']
            
            trim_final_profile = 'the category for the article:' + add_double_quote(trim_profile) + ' is ' + add_double_quote(item['category'])
            #trim_profile_text = tokenizer.decode(trim_profile_tokens[:-1])
            profile_entities.append(trim_final_profile)
        
        return profile_entities

    def __merge_profile_and_input(self, original_string, additional_string):

        return additional_string + '. ' + original_string

class LaMP3Prompt():
    def __init__(self) -> None:
        pass
    
    def aggregated_prompt(self, input, retrieved_profile, tokenizer, max_input_len=512, max_task_len=256, order='start', random_seed=42):
        """
        To merge the task input and the user profile into the modified input
        """
        if len(retrieved_profile) == 0:
            return input
        
        # changing the order of the profiles
        if order == 'start':
            pass
        elif order == 'end':
            retrieved_profile.reverse()
        elif order == 'middle':
            retrieved_profile = reorder_list_middle(retrieved_profile)
        elif order == 'random':
            random.seed(random_seed)
            random.shuffle(retrieved_profile)
        
        input_length = len(tokenizer(input)['input_ids'])
        if input_length < 256:
            max_profile_length = (max_input_len-max_task_len)/len(retrieved_profile)
        else:
            max_profile_length = 0 if input_length>max_input_len else (max_input_len-input_length)/len(retrieved_profile)
        profile_prompt = contact(
            self.__per_profile_entity_prompt(
                retrieved_profile, 
                tokenizer, 
                max_profile_length)
        )

        final_input_text = self.__merge_profile_and_input(input, profile_prompt)
        return final_input_text

    def __per_profile_entity_prompt(self, profile, tokenizer, max_profile_length):
        
        profile_entities = []
        for item in profile:
            
            final_profile = item['score'] + ' is the score for' + add_double_quote(item['text'])
            original_profile_tokens = tokenizer.encode(final_profile)
            if len(original_profile_tokens) > max_profile_length:
                trim_length = math.ceil(len(original_profile_tokens)-max_profile_length)
                trim_text_tokens = tokenizer.encode(item['text'])[:-trim_length]
                trim_profile = tokenizer.decode(trim_text_tokens[:-1])
            else:
                trim_profile = item['text']
            
            trim_final_profile = item['score'] + ' is the score for' + add_double_quote(trim_profile)
            #trim_profile_text = tokenizer.decode(trim_profile_tokens[:-1])
            profile_entities.append(trim_final_profile)
        
        return profile_entities

    def __merge_profile_and_input(self, original_string, additional_string):

        return additional_string + '. ' + original_string



class LaMP4Prompt():
    def __init__(self) -> None:
        pass
    
    def aggregated_prompt(self, input, retrieved_profile, tokenizer, max_input_len=512, max_task_len=256, order='start', random_seed=42):
        """
        To merge the task input and the user profile into the modified input
        """
        if len(retrieved_profile) == 0:
            return input
        
        # changing the order of the profiles
        if order == 'start':
            pass
        elif order == 'end':
            retrieved_profile.reverse()
        elif order == 'middle':
            retrieved_profile = reorder_list_middle(retrieved_profile)
        elif order == 'random':
            random.seed(random_seed)
            random.shuffle(retrieved_profile)
        
        max_profile_length = (max_input_len-max_task_len-5)/len(retrieved_profile)
        profile_prompt = contact(
            self.__per_profile_entity_prompt(
                retrieved_profile, 
                tokenizer, 
                max_profile_length)
        )

        final_input_text = self.__merge_profile_and_input(input, profile_prompt)
        return final_input_text

    def __per_profile_entity_prompt(self, profile, tokenizer, max_profile_length):
        
        profile_entities = []
        for item in profile:
            
            final_profile = add_double_quote(item['title']) + ' is the title for' + add_double_quote(item['text'])
            original_profile_tokens = tokenizer.encode(final_profile)
            if len(original_profile_tokens) > max_profile_length:
                trim_length = math.ceil(len(original_profile_tokens)-max_profile_length)
                trim_text_tokens = tokenizer.encode(item['text'])[:-trim_length]
                trim_profile = tokenizer.decode(trim_text_tokens[:-1])
            else:
                trim_profile = item['text']
            
            trim_final_profile = add_double_quote(item['title']) + ' is the title for' + add_double_quote(trim_profile)
            #trim_profile_text = tokenizer.decode(trim_profile_tokens[:-1])
            profile_entities.append(trim_final_profile)
        
        return profile_entities

    def __merge_profile_and_input(self, original_string, additional_string):

        return additional_string + '. ' + original_string

class LaMP5Prompt():
    def __init__(self) -> None:
        pass
    
    def aggregated_prompt(self, input, retrieved_profile, tokenizer, max_input_len=512, max_task_len=256, order='start', random_seed=42):
        """
        To merge the task input and the user profile into the modified input
        """
        if len(retrieved_profile) == 0:
            return input
        
        # changing the order of the profiles
        if order == 'start':
            pass
        elif order == 'end':
            retrieved_profile.reverse()
        elif order == 'middle':
            retrieved_profile = reorder_list_middle(retrieved_profile)
        elif order == 'random':
            random.seed(random_seed)
            random.shuffle(retrieved_profile)
        
        max_profile_length = (max_input_len-max_task_len)/len(retrieved_profile)
        profile_prompt = contact(
            self.__per_profile_entity_prompt(
                retrieved_profile, 
                tokenizer, 
                max_profile_length)
        )

        final_input_text = self.__merge_profile_and_input(input, profile_prompt)
        return final_input_text

    def __per_profile_entity_prompt(self, profile, tokenizer, max_profile_length):
        
        profile_entities = []
        for item in profile:
            
            final_profile = add_double_quote(item['title']) + ' is the title for' + add_double_quote(item['abstract'])
            original_profile_tokens = tokenizer.encode(final_profile)
            if len(original_profile_tokens) > max_profile_length:
                trim_length = math.ceil(len(original_profile_tokens)-max_profile_length)
                trim_text_tokens = tokenizer.encode(item['abstract'])[:-trim_length]
                trim_profile = tokenizer.decode(trim_text_tokens[:-1])
            else:
                trim_profile = item['abstract']
            
            trim_final_profile = add_double_quote(item['title']) + ' is the title for' + add_double_quote(trim_profile)
            #trim_profile_text = tokenizer.decode(trim_profile_tokens[:-1])
            profile_entities.append(trim_final_profile)
        
        return profile_entities

    def __merge_profile_and_input(self, original_string, additional_string):

        return additional_string + '. Following the given patterns ' + original_string

class LaMP6Prompt():
    def __init__(self) -> None:
        pass

    def aggregated_prompt(self, input, retrieved_profile, tokenizer, max_input_len=512, max_task_len=256, order='start', random_seed=42):
        """
        To merge the task input and the user profile into the modified input
        """
        max_profile_length = (max_input_len-max_task_len)/len(retrieved_profile)
        profile_prompt = contact(
            self.__per_profile_entity_prompt(
                retrieved_profile, 
                tokenizer, 
                max_profile_length)
        )

        final_input_text = self.__merge_profile_and_input(input, profile_prompt)
        return final_input_text

    def __per_profile_entity_prompt(self, profile, tokenizer, max_profile_length):
        
        profile_entities = []
        for item in profile:
            
            final_profile = add_double_quote(item['title']) + ' is the title for' + add_double_quote(item['text'])
            original_profile_tokens = tokenizer.encode(final_profile)
            if len(original_profile_tokens) > max_profile_length:
                trim_length = math.ceil(len(original_profile_tokens)-max_profile_length)
                trim_text_tokens = tokenizer.encode(item['text'])[:-trim_length]
                trim_profile = tokenizer.decode(trim_text_tokens[:-1])
            else:
                trim_profile = item['text']
            
            trim_final_profile = add_double_quote(item['title']) + ' is the title for' + add_double_quote(trim_profile)
            #trim_profile_text = tokenizer.decode(trim_profile_tokens[:-1])
            profile_entities.append(trim_final_profile)
        
        return profile_entities

    def __merge_profile_and_input(self, original_string, additional_string):

        return additional_string + '. ' + original_string

class LaMP7Prompt():
    def __init__(self) -> None:
        pass

    def aggregated_prompt(self, input, retrieved_profile, tokenizer, max_input_len=512, max_task_len=256, order='start', random_seed=42):
        """
        To merge the task input and the user profile into the modified input
        """
        if len(retrieved_profile) == 0:
            return input
        
        # changing the order of the profiles
        if order == 'start':
            pass
        elif order == 'end':
            retrieved_profile.reverse()
        elif order == 'middle':
            retrieved_profile = reorder_list_middle(retrieved_profile)
        elif order == 'random':
            random.seed(random_seed)
            random.shuffle(retrieved_profile)
        
        max_profile_length = (max_input_len-max_task_len-10)/len(retrieved_profile)
        profile_prompt = contact(
            self.__per_profile_entity_prompt(
                retrieved_profile, 
                tokenizer, 
                max_profile_length)
        )

        final_input_text = self.__merge_profile_and_input(input, profile_prompt)
        return final_input_text

    def __per_profile_entity_prompt(self, profile, tokenizer, max_profile_length):
        
        profile_entities = []
        for item in profile:
            
            final_profile = add_double_quote(item['text'])
            original_profile_tokens = tokenizer.encode(final_profile)
            if len(original_profile_tokens) > max_profile_length:
                trim_length = math.ceil(len(original_profile_tokens)-max_profile_length)
                trim_text_tokens = tokenizer.encode(item['text'])[:-trim_length]
                trim_profile = tokenizer.decode(trim_text_tokens[:-1])
            else:
                trim_profile = item['text']
            
            trim_final_profile = add_double_quote(trim_profile)
            #trim_profile_text = tokenizer.decode(trim_profile_tokens[:-1])
            profile_entities.append(trim_final_profile)
        
        return profile_entities

    def __merge_profile_and_input(self, original_string, additional_string):

        return additional_string + ' are written by a person. Following the given patterns ' + original_string