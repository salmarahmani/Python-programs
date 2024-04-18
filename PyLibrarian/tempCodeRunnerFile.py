    def get_borrower_id(self, borrower_name):
        self.cursor.execute('SELECT borrower_id FROM Borrowers WHERE LOWER(name) = LOWER(?)', (borrower_name,))
        result = self.cursor.fetchone()
        ret