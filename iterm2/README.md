# iTerm2 backup

`legacy-state.itermexport` is the original `iTerm2 State.itermexport`, preserved
without modification. It is intentionally not installed by the script.

This archive contains preferences, secure preference flags, and SQLite files for
chat and restorable session state. These are broader than portable terminal
settings. Its database contents have not been audited for private information.

Keep this only as a migration backup. For future sharing, export the selected
profiles or preferences you actually need, review the export, and keep full state
backups in private backup storage. New `.itermexport` files are ignored by default.
The legacy export was already tracked; moving or later deleting it does not remove
its previous contents from Git history.
