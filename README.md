# Super Story Summarizer

**This README will be properly formatted in the future, I'm too lazy to do it now.**

## Current features
- Nothing useful 🤣

## Planned features
What this project has in store for text-generation-webui!

### Main Ideas

- Map details of specific subjects (i.e. each character has own list of details)
- Add current event information (what is currently happening)
- Add extreme short-term information (what is CURRENTLY happening)
- Summarize context (i.e. style of narration, 2nd person vs 3rd person) - Save summary of context in specific branch of config JSON file for future use
- Summarize full histories (for old chats, allow summarizing certain # of messages at a time)
  
### Master Settings

- Active summarization (summarize each new line and push it to array) vs total summarization (get full story and summarize)
  - Active prompt: **LOW-MEDIUM USAGE : -CONTEXT ++DATA**

    - *Summarize the current events:*

      *(get last elements in history)*

      *(append to summary)*

  - Total prompt: **HIGH USAGE : --CONTEXT +DATA**

    - *All text after "%%% History" is the story up to this point.*

      *All text after "%%% Latest event" is what is currently happening in the story.*

      *Summarize the current story:*

      *%%% History*

      *(get current summary)*

      *%%% Latest event*

      *(get last elements in history)*

      *(replace summary)*
- Summary weight [float] **LOW USAGE : +CONTEXT**
  - Begin summarization/intensify summarization depending on:
    - current amount of data stored
    - total \# of messages
- Include timestamp [bool] **LOW USAGE : +CONTEXT**
- Summary break (how summary should be split, i.e. per day or per scene) [string] **CONFIG : -CONTEXT**
- Memory loss **LOW USAGE : --CONTEXT -DATA**
  - Keep all details of past summaries vs summarize further and further
  - Re-summarize based on time, sequence, or both?
- Map per subject **HIGH USAGE : ++CONTEXT ++DATA**
  - Main subjects separate from misc. subjects?
  - Specific subjects excluded or included?
- JSON branch order (i.e. break.subject or subject.break?)
  - Break -> Subject = More sequential
  - Subject -> Break = More plot/character-based

### UI Ideas

- JSON branch order
  - Configurable prompts and branches
    - Master prompt per root (i.e. "Summarize the {type_of_character} character {character}" for "characters" = "Summarize the main character char1")
    - Exclusion value per branch (i.e. "prompt$" for "characters.main.char2") 
    - Generation keys per branch (i.e. "gen1" for 2 main characters and main base), default to current root key (i.e. "main") [string]
    - Custom generation order based on generation key (default to order in tree)
  - Auto-generate on summarize? [toggleable, button]

