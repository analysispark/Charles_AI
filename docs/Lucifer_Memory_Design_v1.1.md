# Lucifer Memory Design v1.1

## Purpose
Lucifer should automatically convert conversations into structured memory to enable better recall and knowledge management. The system focuses on preserving project history, user decisions, and behavioral patterns rather than knowledge retrieval.

## Memory Folders
Memory/
├── RAW
├── Summaries
├── Decisions
├── Insights
└── Tasks

## Requirements

1. **Raw conversation logs** must be stored in Memory/RAW.
2. Lucifer must be able to analyze a conversation and generate:
   - Summary
   - Decisions
   - Insights
   - Tasks
3. Generated memories must be saved as Markdown files.
4. Every memory file must include metadata:
   ---
   date:
   project:
   source:
   tags:
   ---

5. **Phase 1** should NOT be fully automatic.
   Instead, the user will manually trigger memory generation using a command such as:
   "Summarize today's conversation"

6. When triggered, Lucifer should:
   - Read the current conversation
   - Generate Summary
   - Generate Decisions
   - Generate Insights
   - Generate Tasks
   - Save each result into the appropriate Memory folder

7. **Do not implement Vault search**
8. **Do not implement RAG**
9. **Do not implement Vector Database**
10. Focus only on Memory processing and storage

## Proposed Architecture

### Core Components
- Memory Manager: Orchestrates memory generation process
- Conversation Reader: Reads current conversation data
- Memory Generator: Creates summaries, decisions, insights, tasks
- File Writer: Saves generated memories as Markdown files
- Metadata Handler: Manages metadata for each memory file

### Data Flow
1. User triggers memory generation command
2. Conversation Reader extracts conversation data
3. Memory Generator processes conversation and creates structured outputs:
   - Summary: High-level overview of conversation
   - Decisions: Key decisions made during conversation with IDs (D-0001, D-0002...)
   - Insights: Key insights focusing on user preferences and behavior patterns
   - Tasks: Action items with status tracking (todo, in-progress, completed)
4. File Writer saves each output to respective folders with metadata
5. System confirms successful memory generation

## File Structure
Memory/
├── RAW/
│   ├── 2023-10-01_conversation.md
│   └── 2023-10-02_conversation.md
├── Summaries/
│   ├── 2023-10-01_summary.md
│   └── 2023-10-02_summary.md
├── Decisions/
│   ├── 2023-10-01_decisions.md
│   └── 2023-10-02_decisions.md
├── Insights/
│   ├── 2023-10-01_insights.md
│   └── 2023-10-02_insights.md
└── Tasks/
    ├── 2023-10-01_tasks.md
    └── 2023-10-02_tasks.md

## Processing Flow
1. User command "Summarize today's conversation" is received
2. System identifies current conversation session
3. Conversation data is extracted and formatted
4. Each memory type is generated:
   - Summary: High-level overview of conversation
   - Decisions: Key decisions made during conversation with IDs (D-0001, D-0002...)
   - Insights: Key insights focusing on user preferences and behavior patterns
   - Tasks: Action items with status tracking (todo, in-progress, completed)
5. Generated content is saved to respective folders with metadata
6. System confirms successful memory generation

## Example Outputs

### Memory/RAW/2023-10-01_conversation.md
