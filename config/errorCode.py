def errors(err_code):

    err_dic = {
        0: ("OP_ERR_NONE", "정상처리"),
        10: ("OP_ERR_FAIL", "실패"),
        10: ("OP_ERR_LOGIN", "사용자정보교환실패")
    }

    result = err_dic[err_code]

    return result
