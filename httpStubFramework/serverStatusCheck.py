check_server = set()


def status_check(status_set):
    while True:
        if check_server == status_set:
            break
