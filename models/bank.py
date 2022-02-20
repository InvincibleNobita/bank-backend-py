from pydantic import BaseModel

class BankTransactionDetail(BaseModel):
    AccountNo: str
    Date: str
    TransactionDetail: str
    ValueDate: str
    WithdrawalAMT: str
    BalanceAMT: str




    