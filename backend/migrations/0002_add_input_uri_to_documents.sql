ALTER TABLE documents
ADD COLUMN input_uri VARCHAR(500);

UPDATE documents
SET input_uri = ''
WHERE input_uri IS NULL;

ALTER TABLE documents
ALTER COLUMN input_uri SET NOT NULL;
