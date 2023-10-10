# Super Story Summarizer

**This README will be properly formatted in the future, I'm too lazy to do it now.**

# Current features
- Nothing useful 🤣

## Main Ideas

- Map details of specific subjects (i.e. each character has own list of details)
- Add current event information (what is currently happening)
- Add extreme short-term information (what is CURRENTLY happening)
- Summarize context (i.e. style of narration, 2nd person vs 3rd person) - Save summary of context in specific branch of JSON file for future use
  
## Master Settings

- Active summarization (summarize each new line and push it to array) vs total summarization (get full story and summarize)
  - Active prompt: **LOW-MEDIUM USAGE : -CONTEXT ++DATA**

    - *Summarize the current events:*

      *(get last elements in history)*

      *(append to summary)*

  - Total prompt: **HIGH USAGE : --CONTEXT +DATA**

    - *All text after “%%% History” is the story up to this point.*

      *All text after “%%% Latest event” is what is currently happening in the story.*

      *Summarize the current story:*

      *%%% History*

      *(join whole summary)*

      *%%% Latest event*

      *(get last elements in history)*
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

## UI Ideas

- JSON branch order
  - Configurable prompts and branches
    - Master prompt per root (“Summarize the {key} character {key.key}” for “characters” = “Summarize the main character char1”)
    - Exclusion prompt per branch (“prompt2” for “characters.main.char2”)
  - Auto-generate on summarize? [toggleable, button]

