The addParagraph.py script here takes a file of lists from the Talis Aspire reports tool, and adds to the top of each list in that file a paragraph (in this instance saying 'give us some feedback', but it can be anything), providing that it does not exist already. The lists are then published.

The deleteFeedbackSection script takes a file of lists, and deletes that same paragraph from the list (if it exists). The lists are then published.

The scripts use the talis.py module that is in the main directory of this repository, and if you want to use it you should read the main README and be aware of how amateruish this scripting is, the alternatives, etc.
