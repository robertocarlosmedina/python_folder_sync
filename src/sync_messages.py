sync_messages: dict = {
    "create": lambda source, replica: f"[CREATE]: File '{source}' from source created into replica '{replica}'",
    "copy": lambda source, replica: f"[COPY]: Contents of file '{source}' from source copy to replica '{replica}'",
    "delete": lambda source, replica: f"[DELETE]: File deleted fom '{replica}' that doesn't exist in '{source}'"
}
