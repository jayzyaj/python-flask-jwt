from run import db

class BankAccountModel(db.Model):
    __tablename__ = 'bank_accounts'

    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    bank_account = db.Column(db.String(60), nullable = False)
    bank_account_name = db.Column(db.String(90), nullable = False)
    bank_account_number = db.Column(db.String(30), unique = True, nullable = False)
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()