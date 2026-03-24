from lab3.log_definition import LOG_SCHEMA



def entry_to_dict(entry):
    return {
        log_field.name : value for log_field, value in zip(LOG_SCHEMA, entry)
    }

