Example
=======
.. code-block:: python

    client = trello.Client()
    boards = client.get_boards()
    gtd = boards['Getting Things Done']
    labels = gtd.get_labels()
    needs_due = labels['needs-due-date']
    for card in gtd.cards:
        print(f"Processing card {card.name}")
        if not card.due and not card.has_label(needs_due)
            card.add_label(needs_due)
        if card.due and card.has_label(needs_due)
            card.remove_label(needs_due)
