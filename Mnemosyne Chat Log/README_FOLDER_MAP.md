# Mnemosyne Chat Log Folder Map

This workspace is organized for preservation first.

## 00_FINAL_DELIVERABLES

Final anthology outputs:

- `Mnemosyne_COMPLETE_CAUSAL_LOG_ANTHOLOGY.txt`
- `Mnemosyne_COMPLETE_CAUSAL_LOG_ANTHOLOGY.manifest.json`
- `Mnemosyne_COMPLETE_CAUSAL_LOG_ANTHOLOGY.verification.txt`
- `Mnemosyne_COMPLETE_CAUSAL_LOG_ANTHOLOGY.zip`

Use this folder first.

## 01_SOURCE_OG_LOGS

Original source logs and uploaded zip files. Do not delete unless you are fully done with preservation.

## 02_DERIVED_EXTRACTED_CHATS

Derived extracted chats, cleaned JSONL, causal chunks, and earlier extracted zip outputs. Useful for inspection, but the final anthology already includes these contents.

## 03_TOOLS

Scripts used to extract, assemble, and verify the anthology.

## 80_WORKING_EXTRACTS

Temporary extracted zip contents and raw working files. Safe deletion candidate after you trust `00_FINAL_DELIVERABLES` and `01_SOURCE_OG_LOGS`.

## 90_LEGACY_USER_EPISODE_SPLITS

The older manually split episode folders. They may overlap with OG logs. Kept because no-omission was priority one.

## Deletion Recommendation

Do not delete `00_FINAL_DELIVERABLES` or `01_SOURCE_OG_LOGS`.

Likely safe to delete later, after backup:

- `80_WORKING_EXTRACTS`
- `02_DERIVED_EXTRACTED_CHATS/extracted_chats.zip`
- `02_DERIVED_EXTRACTED_CHATS/extracted_chats/causal_path/combined_causal_path.md` if you only use chunk files

Maybe delete later only if you accept losing duplicate legacy organization:

- `90_LEGACY_USER_EPISODE_SPLITS`

I did not delete anything during cleanup.
