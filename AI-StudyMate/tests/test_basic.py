from src.learning_analytics import readiness_score
def test_readiness(): assert readiness_score([{'topic':'A','mastery':80},{'topic':'B','mastery':60}])==70
