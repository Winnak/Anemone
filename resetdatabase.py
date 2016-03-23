""" Resets database """

import Anemone

print('Initialized the database.')
# Anemone.app.run(debug=True)
Anemone.database.init_db()
