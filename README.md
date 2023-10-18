# Super Story Summarizer

*This README will be properly formatted in the future, I'm too lazy to do it now.*

**WARNING: As of 2023-10-16, I am having difficulty progressing due to building upon Gradio and its inability to have dynamic elements i.e. textboxes while keeping this a zero-external-library extension. Although it is possible to simply create 100 textboxes with ids 1–10 * 1–10 and hide them, I would rather not do that, though I will if I have to. JavaScript -> Python communication is simple enough thanks to button clicking events, but vice versa is not, when using Gradio.**

## Current features
- Nothing useful 🤣

## Planned features
What does this project have in store for text-generation-webui?

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
	- Override values per branch (i.e. "prompt" for "characters.main.char2") [string, string]
	  - Generation keys per branch (i.e. "gen1" for 2 main characters and main base), default to current root key (i.e. "main") [string]
	- Custom generation order based on generation key (default to order in tree)
  - Auto-generate on summarize? [toggleable, button]
  - Set different file per config [dropdown]
    - Set default [button]

