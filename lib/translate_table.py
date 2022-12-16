TranslateTable = {
    'name': '名稱',
    'type': '類型',
    'title': '標題',
    'customer': '客戶',
    'address': '地址',
    'status': '狀態',
    'note': '備註',
    'creator': '建立者',
    'owner': '負責人員',
    'editor': '編輯者',
    'start_date': '開始時間',
    'due_date': '預計完成時間',
    'update_time': '最後編輯時間',
    'cel': '手機',
    'dispatch_date': '預計派工日期'
}


def translate_field_name(fields):
    ch_change_field = []
    for field in fields:
        if TranslateTable.get(field):
            ch_change_field.append(TranslateTable.get(field))
        else:
            ch_change_field.append(field)
    return ch_change_field
