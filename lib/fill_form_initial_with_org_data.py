def fill_form_initial_with_org_data(org_instance, form):
    for element in form.fields:
        db_data = getattr(org_instance, element)
        if db_data is not None or db_data != "":
            form.fields[element].initial = db_data
    return form
