def rule_based_hr(hr):
    if hr < 45:
        return "DANGEROUS_LOW", "Nhịp tim quá thấp"
    elif hr < 60:
        return "LOW", "Nhịp tim thấp"
    elif hr <= 100:
        return "NORMAL", "Nhịp tim bình thường"
    elif hr <= 120:
        return "HIGH", "Nhịp tim cao"
    else:
        return "DANGEROUS_HIGH", "Nhịp tim quá cao"
