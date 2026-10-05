import db


def create_file(path, content, owner):
    existing = db.execute_select("files", {"path": path})
    if existing:
        return -1

    file_id = db.execute_insert("files", {
        "path": path,
        "content": content,
        "owner": owner
    })

    return file_id


def read_file(path):
    files = db.execute_select("files", {"path": path})
    if not files:
        return ""
    return files[0]["content"]


def write_file(path, content):
    db.execute_update("files", {"content": content}, {"path": path})
    return True


def delete_file(path):
    db.execute_delete("files", {"path": path})
    return True


def list_files(prefix="/"):
    all_files = db.execute_select("files")
    return [file["path"] for file in all_files if file["path"].startswith(prefix)]


def get_owner(path):
    files = db.execute_select("files", {"path": path})
    if not files:
        return None
    return files[0]["owner"]


def get_file_info(path):
    files = db.execute_select("files", {"path": path})
    if not files:
        return None
    return files[0]


if __name__ == "__main__":
    print(create_file("/test.txt", "hello", "admin"))
    print(read_file("/test.txt"))
    print(create_file("/test.txt", "other", "admin"))
    print(list_files("/"))
    print(get_owner("/test.txt"))